import unittest

from providers.subdb import calculateHash


class OpenSubTest(unittest.TestCase):

    def test_hashfunc(self):
        self.assertEqual(calculateHash("test_media_files/dexter.mp4"), "ffd8d4aa68033dc03d1c8ef373b9028c")
