from flask import Flask, request, make_response
from pyngrok import ngrok
from utils.utils import *
import utils.settings as settings

public_url = ngrok.connect(8080).public_url
app = Flask(__name__)

@app.route("/")
def hello_world():
    return "Hello world!"

@app.route("/github", methods=["POST"])
def webhook():
    if request.method == "POST":
        headers = request.headers
        data = request.json
        if headers["X-GitHub-Event"] == "push":
            try:
                clone_url, branch, repo_owner, repo_name, commit_sha = parse_json(data)
                clone_repo(clone_url, settings.repo_dir, branch)
                build_result = syntax_check(settings.repo_dir_src)
                log_entry = 'Build failed'
                commit_status = 'error'
                if build_result == "build successful":
                    test_results = run_tests(settings.repo_dir_src)
                    log_entry = 'Tests failed'
                    if test_results:
                        commit_status = 'success'
                        log_entry = 'Success'
                
                set_commit_status(repo_owner, repo_name, commit_sha, commit_status)

                create_build_log_entry(commit_sha, log_entry)

                remove_repo(settings.repo_dir)
                
                return make_response("success", 200)
            except:
                return make_response("fail", 400)
        elif headers["X-GitHub-Event"] == "ping":
            return make_response("ping", 200)

# "Build result" route
@app.route("/builds/<build_id>")
def get_build_info_html(build_id):
    try:
        log_relative_path = r"./src/build_logs/" + build_id + ".log"
        with open(log_relative_path) as log:
            log_lines = log.readlines()
            log.close()
    
        log_newline_seperated_string = "\n".join(log_lines)
        log_html_formatted = build_log_html_element(log_newline_seperated_string)

        return log_html_formatted
    except FileNotFoundError:
        return "<p>the build you are trying to access does not exist.<p>"

# "Build history list" route
@app.route("/builds/all")
def get_build_history_html():
    directory_path = "./src/build_logs/"
    try:
        if len(os.listdir(directory_path)) == 0:
            return "<p>There is currently no build history for this CI-server.</p>"
        else:  
            all_log_names = []  
            for log_filename in os.listdir(directory_path):
                log_id_no_filetype = log_filename.split('.')[0]  
                all_log_names.append(log_id_no_filetype)
            all_log_names.reverse()
            return build_log_history_html_element(all_log_names)

    except FileNotFoundError:
        return "<p>There is currently no build history for this CI-server.</p>"

if __name__ == "__main__":
    print(public_url)
    app.run(port=8080)
