import unittest
from src_linux.providers.opensub import hashfunc


class OpenSubTest(unittest.TestCase):

    def test_hashfunc(self):
        self.assertEqual(hashfunc("test_media_files/breakdance.avi"), "8e245d9679d31e12")

if __name__ == '__main__':
    unittest.main()
