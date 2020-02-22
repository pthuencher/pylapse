"""
    Test Description:
        Ensure that the application is working properly with a handful basic tests
"""
import unittest


from src.helpers import parse_resize


class TestBasic(unittest.TestCase):
    def test_resize(self):
        """
        Test that it can sum a list of integers
        """
        data = "1920x1080"
        expected = (1920,1080)


        result = parse_resize(data)
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()
