from unittest import main, TestCase
from utils.utils import *
import json

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

if __name__ == "__main__":
    main()