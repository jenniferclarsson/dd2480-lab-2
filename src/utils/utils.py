import os
from unittest import TestLoader, TextTestRunner

from git import Repo
from pylint import lint
from datetime import datetime
from pylint.reporters import text
from io import StringIO
import shutil
import requests
import utils.settings as settings
import subprocess

# Finds and runs the tests in test_folder if they match pattern test_file_patterns
# And logs it to test_output_file
# The function uses the settings file for parameters who are None
# return false on failed tests and true on no failed test
def run_tests(test_folder=None, test_file_pattern=None, test_output_file=None):

    test_folder = settings.test_folder if test_folder is None else test_folder
    test_file_pattern = settings.test_file_pattern if test_file_pattern is None else test_file_pattern
    test_output_file = settings.test_output_file if test_output_file is None else test_output_file
    test_folder = test_folder.replace(" ", "\ ")

    sep = os.path.sep
    curdir = os.path.dirname(__file__).split(sep)
    test_folder = sep.join(curdir + test_folder.split(sep)) if not os.path.isabs(test_folder) else test_folder
    test_output_file = sep.join(curdir + test_output_file.split(sep)) if not os.path.isabs(test_output_file) else test_output_file

    with open(test_output_file, "w") as f:
        # bashCommand = ['bash', '-c', f'cd {test_folder} && python -m unittest -v unit_tests.py']
        bashCommand = ['bash', '-c', f'cd {test_folder} && python -m unittest -v {test_file_pattern}']
        process = subprocess.Popen(bashCommand, stdout=subprocess.PIPE)
        output, error = process.communicate()
        # print(output)
        f.write(str(output))
    return not bool(process.returncode)

# Parses the json data received from the github webhook and retrieves
# the fields we are interested in, which is currently clone_url, branch,
# repo_owner, repo_name and commit_sha
# returns clone_url, branch, repo_owner, repo_name, commit_sha
# on success and the string "invalid json" on fail
def parse_json(data):
    try:
        clone_url = data["repository"]["clone_url"]
        branch = data["ref"].replace("refs/heads/", "")
        repo_owner = data["repository"]["owner"]["name"]
        repo_name = data["repository"]["name"]
        commit_sha = data["after"]
        return clone_url, branch, repo_owner, repo_name, commit_sha
    except:
        return "invalid json"

# Clones the directory hosted at git_url into the path specified by repo_dir
# And checkouts the branch specified by the branch parameter
# Returns the string "clone succeeded" on success and the string
# "clone failed" on failure
def clone_repo(git_url, repo_dir, branch):
    try:
        repo = Repo.clone_from(git_url, repo_dir, branch=branch)
        return 'clone succeeded'
    except:
        return 'clone failed'

# Removes the repository at path repo_dir
# Returns the string "Repo succeeded" on success
# and the string "Invalid path" on fail
def remove_repo(repo_dir):
    try:
        shutil.rmtree(repo_dir)
        return 'Repo deleted'
    except:
        return 'Invalid path'
    
# Performs a syntax check on the repository specified by path
# using Pylint. Only checks for fatal errors
# Returns "build successful" if no errors were detected
# and "build failed" if there was errors detected
def syntax_check(path):
    try: 
        args = ["--disable=W,R,C,undefined-variable,import-error", str(path)]
        pylint_output = StringIO()
        reporter = text.ColorizedTextReporter(pylint_output)
        run = lint.Run(args, reporter=reporter, exit=False)
        stats= run.linter.stats
        if stats.error != 0 or stats.fatal != 0:
            return "build failed"
        return "build successful"
    except:
        return "build failed"

# -- CREATE A LOG HTML ELEMENT --
# Wraps build log information in HTML tags for better presentation in browser
def build_log_html_element(log_newline_seperated_string):
    if log_newline_seperated_string == "":
        return "<p>Error: This build log is empty.</p>"
    else:
        log_br_seperated = log_newline_seperated_string.replace("\n","<br>")
        log_html_element = "<div><span style='font-weight:bold'>" + log_br_seperated + "</span></div>"
        return log_html_element

# -- CREATE A LOG HISTORY HTML ELEMENT --
# Wraps all log names in HTML tags for better presentation in browser
def build_log_history_html_element(log_filename_list):
    if len(log_filename_list) == 0:
        return "<p>There is currently no build history for this CI-server.</p>"
    else:
        log_html_elements = []
        for filename in log_filename_list:
            log_html_elements.append("<a href='/builds/" + filename + "'>" + filename + "</a>")
        log_history_br_seperated = "<br>".join(log_html_elements)
        list_first_line = "<span style='font-weight:bold'>List of all CI-server builds:</span><br>"
        log_history_html_element = "<div>" + list_first_line + log_history_br_seperated + "</div>"
        return log_history_html_element

# -- CREATE A .LOG BUILD FILE --
# Creates a .log file containing information on the build and its result
# Commit_id = String (from Github JSON object)
# build_result = build failed, test failed, success 
def create_build_log_entry(commit_id, build_result):
    try:
        time_now = datetime.now()
        build_id = "bid" + time_now.strftime("%Y%m%d%H%M%S")
        build_time = time_now.strftime("%Y-%m-%d %H:%M:%S")
        log_message = "build-id: " + str(build_id) + "\ncommit-id:" + commit_id + "\nbuild_time:" + build_time + "\nbuild_result:" + build_result
        if not os.path.exists("./src/build_logs"):
            os.makedirs("./src/build_logs")
        f = open("./src/build_logs/" + build_id + ".log", "x")
        f.write(log_message)
        f.close()
        return build_id
    except FileExistsError:
        return "logging failed: Log already exists"
    


# -- SET STATUS OF COMMIT --
# owner = owner of the repo
# repo = name of the repo
# sha = sha hash of the commit
# state = error | failure | pending | success
def set_commit_status(owner, repo, sha, state):
    api_url = f'https://api.github.com/repos/{owner}/{repo}/statuses/{sha}'
    response = requests.post(api_url, auth=(settings.GIT_USER, settings.GIT_TOKEN), json={'state':state})
    if response.status_code < 300:
        return 'commit status succeeded'
    return 'commit status failed'
