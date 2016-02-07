import unittest

from providers.opensub import calculateHash


class OpenSubTest(unittest.TestCase):

    def test_hashfunc(self):
        self.assertEqual(calculateHash("test_media_files/breakdance.avi"), "8e245d9679d31e12")

if __name__ == '__main__':
    unittest.main()
