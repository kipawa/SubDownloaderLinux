import unittest
from src_linux.subdwnld import is_filetype_supported

class GeneralTests(unittest.TestCase):

    def test_is_filetype_supported(self):
        self.assertTrue(is_filetype_supported("simplename.flv"))
        self.assertTrue(is_filetype_supported("/a/full/path/name.mkv"))
        self.assertFalse(is_filetype_supported(".jpg"))