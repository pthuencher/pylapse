"""
    Test Description:
        Ensure that the application is working properly with a handful basic tests
"""
import unittest

from src.helpers import parse_resize, parse_crop


class TestParser(unittest.TestCase):
    def test_valid_resize_param(self):
        """
        Test that resize parameter given on command line is parsed correctly
        """
        data = "1920x1080"
        expected = (1920,1080)

        result = parse_resize(data)
        self.assertEqual(result, expected)

    def test_invalid_resize_param(self):
        """
        Test that an invalid resize parameter given on command line is rejected correctly
        """
        data = "1920"
        expected = None

        result = parse_resize(data)
        self.assertEqual(result, expected)

    def test_invalid_resize_param_no_integer(self):
        """
        Test that an invalid resize parameter given on command line is rejected correctly
        """
        data = "AxB"
        expected = None

        result = parse_resize(data)
        self.assertEqual(result, expected)



    def test_valid_crop_param(self):
        """
        Test that crop parameter given on command line is parsed correctly
        """
        data = "0-250:112-453"
        expected = ((112, 453), (0,250))

        result = parse_crop(data)
        self.assertEqual(result, expected)

    def test_valid_crop_param(self):
        """
        Test that an invalid crop parameter given on command line is rejected correctly
        """
        data = "A-A3-B"
        expected = None

        result = parse_crop(data)
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
