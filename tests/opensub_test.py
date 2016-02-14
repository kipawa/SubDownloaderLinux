import unittest

from providers.opensub import calculate_hash


class OpenSubTest(unittest.TestCase):

    def test_hashfunc(self):
        self.assertEqual(calculate_hash("test_media_files/breakdance.avi"), "8e245d9679d31e12")
        self.assertRaises(ValueError, calculate_hash, "test_media_files/averysmallfile.mp4")

