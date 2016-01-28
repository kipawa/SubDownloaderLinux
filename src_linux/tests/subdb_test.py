import unittest
from src_linux.providers.subdb import get_hash


class OpenSubTest(unittest.TestCase):

    def test_hashfunc(self):
        self.assertEqual(get_hash("test_media_files/dexter.mp4"), "ffd8d4aa68033dc03d1c8ef373b9028c")

if __name__ == '__main__':
    unittest.main()
