'''
FAULTLESS TEST CASES 
'''
from src.main import *

from pathlib import Path
from unittest import main, TestCase


# Tests goes here, see https://docs.python.org/3/library/unittest.html

# This test-suite contains one test, which should pass
class SuccedingTest(TestCase):

    def test_should_succeed_with_expected_result(self):
        # The addition function will add the two numbers, meaning that test should pass
        self.assertEqual(10, addition_function_to_pass_unit_test(5,5))

if __name__ == "__main__":
    main()
