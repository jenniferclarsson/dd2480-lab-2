from unittest import main, TestCase
from utils.utils import *
import json
from pathlib import Path
import shutil

class parse_json_test(TestCase):

    def setUp(self):
        self.expected_clone_url = "https://github.com/jenniferclarsson/test-repo.git"
        self.expected_branch = "main"

    def test_valid_json(self):
        with open('test_data/valid_input.json') as json_file:
            valid_input = json.load(json_file)
        clone_url, branch = parse_json(valid_input)
        self.assertEqual(clone_url, self.expected_clone_url)
        self.assertEqual(branch, self.expected_branch)
    
    def test_invalid_json(self):
        with open('test_data/invalid_input_no_url.json') as json_file:
            invalid_input = json.load(json_file)
        self.assertEqual(parse_json(invalid_input), "invalid json")  


# --------------- GIT CLONE TEST -----------------
class GitCloneTest(TestCase):

    def setUp(self):
        self.git_url = 'git@github.com:edbag22/clone-repo-test.git'
        self.broken_git_url = 'git@github.com:edbag22/clon-repo-test.git'
        self.repo_dir = Path('/tmp/clone-repo-test/')

    def test_should_succeed_when_given_correct_link_and_branch(self):
        res = clone_repo(self.git_url, self.repo_dir, 'main')
        self.assertEqual(res, 'clone succeded')

        #Remove clone if succeded
        if (res == 'clone succeded'):
            shutil.rmtree(self.repo_dir)

    def test_should_fail_when_given_broken_link_but_correct_branch(self):
        res = clone_repo(self.broken_git_url, self.repo_dir, 'main')
        self.assertEqual(res, 'clone failed')

    def test_should_fail_when_given_correct_link_but_unexisting_branch(self):
        res = clone_repo(self.git_url, self.repo_dir, 'branch_that_doesnt_exist')
        self.assertEqual(res, 'clone failed')              

if __name__ == "__main__":
    main()