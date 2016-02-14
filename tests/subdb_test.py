import unittest

from providers.subdb import calculate_hash


class OpenSubTest(unittest.TestCase):

    def test_hashfunc(self):
        self.assertEqual(calculate_hash("test_media_files/dexter.mp4"), "ffd8d4aa68033dc03d1c8ef373b9028c")
        self.assertRaises(ValueError, calculate_hash, ("test_media_files/averysmallfile.mp4"))
