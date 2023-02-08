import os
from unittest import TestLoader, TextTestRunner

from git import Repo
from pylint import lint
from datetime import datetime
from pylint.reporters import text
from io import StringIO

import requests
import utils.settings as settings

def run_tests():
    sep = os.path.sep
    curdir = os.path.dirname(__file__).split(sep)
    test_folder = sep.join(curdir + settings.test_folder.split(sep)) if not os.path.isabs(settings.test_folder) else settings.test_folder
    test_output_file = sep.join(curdir + settings.test_output_file.split(sep)) if not os.path.isabs(settings.test_output_file) else settings.test_output_file

    testloader = TestLoader()
    tests = testloader.discover(test_folder, settings.test_file_pattern)
    with open(test_output_file, "w") as f:
        testrunner = TextTestRunner(f)
        run = testrunner.run(tests)
    return not bool(run.errors + run.failures)

def parse_json(data):
    try:
        clone_url = data["repository"]["clone_url"]
        branch = data["ref"].replace("refs/heads/", "")
        return clone_url, branch
    except:
        return "invalid json"

def clone_repo(git_url, repo_dir, branch):
    try:
        repo = Repo.clone_from(git_url, repo_dir, branch=branch)
        return 'clone succeded'
    except:
        return 'clone failed'
    
def syntax_check(path):
    try: 
        args = ["--disable=W,R,C,undefined-variable", path + "/src"]
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
    log_br_seperated = log_newline_seperated_string.replace("\n","<br>")
    log_html_element = "<div><span style='font-weight:bold'>" + log_br_seperated + "</span></div>"
    return log_html_element

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
        return 'commit status succeded'
    return 'commit status failed'
