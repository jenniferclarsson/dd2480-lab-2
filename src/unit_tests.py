from unittest import main, TestCase
import sys
from utils.utils import *
import utils.settings as settings
import json
from pathlib import Path
import shutil
import os

ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), ".."))

# --------------- PARSE JSON TEST -----------------
# Tests for the function parse_json(data).
class parse_json_test(TestCase):

    def setUp(self):
        self.expected_clone_url = "https://github.com/jenniferclarsson/test-repo.git"
        self.expected_branch = "main"
        self.expected_repo_owner = "jenniferclarsson"
        self.expected_repo_name = "test-repo"
        self.expected_commit_sha = "f17b9496a4600bdb21171c331e5e88688936be35"

    # parse_json should return the expected clone_url, branch, repo_owner, 
    # repo_name and commit_sha when the json data is correctly formatted.
    def test_valid_json(self): 
        with open(os.path.join(ROOT_DIR, "src/test_data/valid_input.json")) as json_file:
            valid_input = json.load(json_file)
        clone_url, branch, repo_owner, repo_name, commit_sha = parse_json(valid_input)
        self.assertEqual(clone_url, self.expected_clone_url)
        self.assertEqual(branch, self.expected_branch)
        self.assertEqual(repo_owner, self.expected_repo_owner)
        self.assertEqual(repo_name, self.expected_repo_name)
        self.assertEqual(commit_sha, self.expected_commit_sha)
    
    # parse_json should return "invalid json" when the json data is not correctly
    # formatted, in this case missing clone_url.
    def test_invalid_json(self):
        with open(os.path.join(ROOT_DIR, "src/test_data/invalid_input_no_url.json")) as json_file:
            invalid_input = json.load(json_file)
        self.assertEqual(parse_json(invalid_input), "invalid json")  

# --------------- GIT CLONE TEST -----------------
# Tests for the function clone_repo(git_url, repo_dir, branch).
class git_clone_test(TestCase):

    def setUp(self):
        self.git_url = 'git@github.com:edbag22/clone-repo-test.git'
        self.broken_git_url = 'git@github.com:edbag22/clon-repo-test.git'
        self.repo_dir = Path('/tmp/clone-repo-test/')

    # clone_repo should return "clone succeeded" given correct git_url and branch.
    def test_should_succeed_when_given_correct_link_and_branch(self):
        res = clone_repo(self.git_url, self.repo_dir, 'main')
        self.assertEqual(res, 'clone succeeded')

        # Remove clone if clone succeeded
        if (res == 'clone succeeded'):
            remove_repo(self.repo_dir)

    # clone_repo should return "clone failed" if given broken link and correct branch.
    def test_should_fail_when_given_broken_link_but_correct_branch(self):
        res = clone_repo(self.broken_git_url, self.repo_dir, 'main')
        self.assertEqual(res, 'clone failed')

    # clone_repo should return "clone failed" if given correct link and nonexisting branch.
    def test_should_fail_when_given_correct_link_but_unexisting_branch(self):
        res = clone_repo(self.git_url, self.repo_dir, 'branch_that_doesnt_exist')
        self.assertEqual(res, 'clone failed')  

# --------------- REMOVE REPO TEST -----------------
# Tests for the function remove_repo(repo_dir).
class remove_repo_test(TestCase):

    def setUp(self):
        self.repo_dir = Path('/tmp/repo-dir-to-be-deleted/')

    # remove_repo should return "Repo deleted" if the repo directory exists. 
    def test_should_succeed_when_dir_exists(self):
        os.mkdir(self.repo_dir)
        res = remove_repo(self.repo_dir)
        self.assertEqual(res, 'Repo deleted')

    # remove_repo should return "Invalid path" if the repo directory does not exist.
    def test_should_fail_when_dir_does_not_exist(self):
        res = remove_repo(self.repo_dir)
        self.assertEqual(res, 'Invalid path')       

# --------------- TEST RUNNER TEST -----------------
# Tests for the function run_tests(test_folder, test_file_pattern, test_output_file). 
class test_runner_test(TestCase):

    def setUp(self):
        # settings.test_folder = "/test_data/dummy_tests"
        settings.test_folder = os.path.join(ROOT_DIR, "src/test_data/dummy_tests")
        settings.test_output_file = "/tmp/garbage.log"
        self.current_modules = list(sys.modules.keys())

    def tearDown(self):
        for newly_imported_module in filter(lambda module: module not in self.current_modules, list(sys.modules.keys())):
            del sys.modules[newly_imported_module]

        os.remove(settings.test_output_file)

    # run_tests should return True when all tests pass.
    def test_should_succed_when_test_passes(self):
        self.assertFalse(run_tests(test_file_pattern="should_succeed_tests.py"))

    # run_tests should return False when at least one test fails.
    def test_should_fail_when_test_fails(self):
        self.assertFalse(run_tests(test_file_pattern="should_fail_tests.py"))

    # run_tests should return False when the test file contains errors.
    def test_should_fail_when_test_errors(self):
        self.assertFalse(run_tests(test_file_pattern="should_error_tests.py"))

    # run_tests should return True when the repo is faultless and all tests pass.
    def test_should_succeed_when_repo_is_test_project_faultless(self):
        self.assertTrue(run_tests(test_folder=os.path.join(ROOT_DIR, "test_project_faultless/src"), test_file_pattern="test_main.py"))

    # run_tests should return False when repo contains at least one failing test.
    def test_should_fail_when_repo_is_test_project_failing_tests(self):
        self.assertFalse(run_tests(test_folder=os.path.join(ROOT_DIR, "test_project_failing_tests/src"), test_file_pattern="test_main.py"))

        
# --------------- BUILD TEST -----------------
# Tests for the function syntax_check(path).
class build_test(TestCase):

    # syntax_check should return "build successful" when repo is faultless.
    def test_build_success_when_faultless_project(self):
        res = syntax_check(os.path.join(ROOT_DIR, "test_project_faultless/src"))
        self.assertEqual(res, "build successful")

    # syntax_check should return "build failed" when repo contains errors.
    def test_build_fail_when_faulty_project(self):
        res = syntax_check(os.path.join(ROOT_DIR, "test_project_error/src"))
        self.assertEqual(res, "build failed")

    # syntax_check should return "build failed" when repo does not exist.
    def test_build_fail_when_invalid_path(self):
        res = syntax_check(os.path.join(ROOT_DIR, "invalid_path_to_project/src"))
        self.assertEqual(res, "build failed")

# --------------- GIT COMMIT STATUS TEST -----------------
# Tests for the function set_commit_status(owner, repo, sha, state).
class git_commit_status_test(TestCase):

    def setUp(self):
        self.git_user = settings.GIT_USER
        self.git_token = settings.GIT_TOKEN
        self.git_repo = settings.GIT_REPO
        self.git_repo_owner = settings.GIT_REPO_OWNER
        self.git_sha = settings.GIT_SHA
        self.git_broken_sha = settings.GIT_BROKEN_SHA

    # set_commit_status should return "commit status succeeded" when given correct
    # owner, repo and sha, and valid state.
    def test_should_succeed_when_given_correct_info(self):
        res = set_commit_status(self.git_repo_owner, self.git_repo, self.git_sha, 'success')
        self.assertEqual(res, 'commit status succeeded')

    # set_commit_status should return "commit status failed" when given correct
    # owner and repo, valid state, but incorrect sha.
    def test_should_fail_when_given_broken_sha(self):
        res = set_commit_status(self.git_repo_owner, self.git_repo, self.git_broken_sha, 'success')
        self.assertEqual(res, 'commit status failed')

    # set_commit_status should return "commit status failed" when given correct
    # owner, repo and sha, but invalid state.
    def test_should_fail_when_given_invalid_state(self):
        res = set_commit_status(self.git_repo_owner, self.git_repo, self.git_sha, 'succes')
        self.assertEqual(res, 'commit status failed')  

# --------------- CREATE BUILD LOG ENTRY -----------------
# Tests for the function create_build_log_entry(commit_id, build_result).
class create_build_log_check(TestCase):

    def tearDown(self):
        try:
            os.remove("./src/build_logs/" + self.created_log + ".log")
        except FileNotFoundError:
            print("A log file was not created or could not be found.")

    # create_build_log should return correct build_id when build log is created.
    def test_should_succeed_when_log_is_created(self):
        log_created = False
        build_id = create_build_log_entry("123", "success")
        self.created_log = build_id
        try:
            log_relative_path = r"./src/build_logs/" + build_id + ".log"
            # Try opening the file to see that it was created
            log = open(log_relative_path)
            log.close()
            log_created = True
        except FileNotFoundError:
            pass
        self.assertEqual(log_created, True)

    # create_build_log should return correct build_id and create build_logs directory
    # if it does not already exist.
    def test_should_succeed_when_log_directory_is_created(self):
        log_directory_created = False
        build_id = create_build_log_entry("123", "success")
        self.created_log = build_id
        if os.path.exists("./src/build_logs"):
            log_directory_created = True 
        self.assertEqual(log_directory_created, True)


# --------------- BUILD LOG HTML ELEMENT TEST -----------------
# Tests for the function build_log_html_element(log_newline_seperated_string).
class log_html_element_check(TestCase):
    
    # build_log_html_element should return correct HTML element given
    # correctly formatted input string.
    def test_should_succeed_when_input_is_correctly_formatted(self):
        res = build_log_html_element("text\nto\nHTML\nformat\ncorrectly")
        self.assertEqual(res, "<div><span style='font-weight:bold'>text<br>to<br>HTML<br>format<br>correctly</span></div>")

    # build_log_entry_element should return "<p>Error: This build log is empty.</p>"
    # given an empty input string.
    def test_should_fail_when_input_string_is_empty(self):
        res = build_log_html_element("")
        self.assertEqual(res, "<p>Error: This build log is empty.</p>")

# --------------- BUILD LOG HISTORY HTML ELEMENT TEST -----------------
# Tests for the function build_log_history_html_element(log_filename_list).
class log_history_html_element_check(TestCase):
    
    # build_log_history_html_element should return correct HTML element given
    # a correctly formatted input string.
    def test_should_succeed_when_input_is_correctly_formatted(self):
        res = build_log_history_html_element(["bid2000","bid1000"])
        self.assertEqual(res, "<div><span style='font-weight:bold'>List of all CI-server builds:</span><br><a href='/builds/bid2000'>bid2000</a><br><a href='/builds/bid1000'>bid1000</a></div>")

    # build_log_history_html_element should return "<p>There is currently no build history for this CI-server.</p>"
    # given an empty input string.
    def test_should_fail_when_input_string_is_empty(self):
        res = build_log_history_html_element([])
        self.assertEqual(res, "<p>There is currently no build history for this CI-server.</p>")

if __name__ == "__main__":
    main()
