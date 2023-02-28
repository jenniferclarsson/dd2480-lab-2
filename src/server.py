from flask import Flask, request, make_response
from pyngrok import ngrok
from utils.utils import *
import utils.settings as settings
from pathlib import Path

public_url = ngrok.connect(8080).public_url
app = Flask(__name__)

# Default server route
# Used to verify URL and that server is up and running
@app.route("/")
def hello_world():
    return "Hello world!"

# Github webhook route
# Server recieves HTTP requests on this route when commits are made to target repository 
@app.route("/github", methods=["POST"])
def webhook():
    if request.method == "POST":
        headers = request.headers
        data = request.json
        # Only run build and test on push events
        if headers["X-GitHub-Event"] == "push":
            try:
                # read data from JSON-object
                clone_url, branch, repo_owner, repo_name, commit_sha = parse_json(data)
                # Clone repo for running local build and test
                clone_repo(clone_url, f'{settings.repo_dir}-{commit_sha}', branch)
                repo_dir_src = Path(f'{settings.repo_dir}-{commit_sha}/src')
                # Syntax analysis using Pylint
                build_result = syntax_check(repo_dir_src)
                log_entry = 'Build failed'
                commit_status = 'error'
                if build_result == "build successful":
                    # Run projects own unit tests
                    test_results = run_tests(repo_dir_src)
                    log_entry = 'Tests failed'
                    if test_results:
                        commit_status = 'success'
                        log_entry = 'Success'
                
                # Set the "commit status" of the remote repository, depending on build results
                set_commit_status(repo_owner, repo_name, commit_sha, commit_status)

                # Create a log entry so that build information and history can be viewed in browser 
                create_build_log_entry(commit_sha, log_entry)

                # Clean-up, remove copied repository 
                remove_repo(settings.repo_dir)
                
                return make_response("success", 200)
            except Exception as e: 
                print(e)
                return make_response("fail", 400)
        elif headers["X-GitHub-Event"] == "ping":
            # Used for troubleshooting
            return make_response("ping", 200)

# "Build result" route
# Information regarding specific builds are available through this route
@app.route("/builds/<build_id>")
# Extract build_id from URL
def get_build_info_html(build_id):
    # Try to find specific build log in build_logs repo
    try:
        log_relative_path = r"./src/build_logs/" + build_id + ".log"
        with open(log_relative_path) as log:
            log_lines = log.readlines()
            log.close()

        # Format log information in a simple HTML element
        log_newline_seperated_string = "\n".join(log_lines)
        log_html_formatted = build_log_html_element(log_newline_seperated_string)

        # Serve the HTML to the browser
        return log_html_formatted
    except FileNotFoundError:
        return "<p>the build you are trying to access does not exist.<p>"

# "Build history list" route
# A history of each build, along with links to more information, is available through this route
@app.route("/builds/all")
def get_build_history_html():
    directory_path = "./src/build_logs/"
    # Try to access logs inside /build_logs repo
    try:
        if len(os.listdir(directory_path)) == 0:
            return "<p>There is currently no build history for this CI-server.</p>"
        else:  
            all_log_names = []  
            # Get filenames of all available logs
            # This is all thats needed to create links to each build
            for log_filename in os.listdir(directory_path):
                log_id_no_filetype = log_filename.split('.')[0]  
                all_log_names.append(log_id_no_filetype)
            all_log_names.reverse()
            # Format log history in a simple HTML element
            return build_log_history_html_element(all_log_names)

    # /build_logs folder does not exist
    except FileNotFoundError:
        return "<p>There is currently no build history for this CI-server.</p>"

if __name__ == "__main__":
    print(public_url)
    app.run(port=8080)
