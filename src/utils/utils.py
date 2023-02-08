import os
from unittest import TestLoader, TextTestRunner

from git import Repo

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
