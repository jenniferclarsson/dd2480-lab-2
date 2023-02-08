'''
FAULTLESS TEST CASES 
'''
from unittest import main, TestCase

from main import *

# Tests goes here, see https://docs.python.org/3/library/unittest.html

# This test-suite contains two test, for which one should fail
class FailingTest(TestCase):

    def test_should_fail_with_expected_result(self):
        # The "faulty addition" function will add one extra after addition, 
        # meaning that test should fail
        self.assertEqual(10, addition_function_to_fail_unit_test(5,5))
    
    def test_should_fail_when_expected_result_incremented(self):
        # The "faulty addition" function will add one extra after addition, 
        # meaning that test should succeed if expected result is incremented by one
        self.assertEqual(11, addition_function_to_fail_unit_test(5,5))

if __name__ == "__main__":
    main()
