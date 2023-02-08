from unittest import TestCase

class test_error(TestCase):

    def test_error(self):
        self.assertEqual(0, 1/0)
