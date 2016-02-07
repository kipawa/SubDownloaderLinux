import unittest

from subdwnld import is_filetype_supported, subdb_subtitles_exist, path_without_file_extension, opensubtitles_subs_exist


class GeneralTests(unittest.TestCase):

    def test_is_filetype_supported(self):
        self.assertTrue(is_filetype_supported("simplename.flv"))
        self.assertTrue(is_filetype_supported("/a/full/path/name.mkv"))
        self.assertFalse(is_filetype_supported(".jpg"))

    def test_subdb_subtitles_exist(self):
        self.assertTrue(subdb_subtitles_exist("dummy_test_files/aFileForWhichThereIsASubDbSubtitle.mkv"))
        self.assertFalse(subdb_subtitles_exist("dummy_test_files/aFileForWhichThereIsNoSubDbSubtitle.mkv"))

    def test_path_without_file_extension(self):
        self.assertEquals("afile", path_without_file_extension("afile.txt"))
        self.assertEquals("/a/file/with/full/path", path_without_file_extension("/a/file/with/full/path.mkv"))
        self.assertEquals( "a/file/without/extension", path_without_file_extension("a/file/without/extension"))

    def test_opensubtitles_subs_exist(self):
        self.assertTrue(opensubtitles_subs_exist("dummy_test_files/aFileForWhichThereIsOpenSubtitlesSubs.mkv"))
        self.assertFalse(opensubtitles_subs_exist("dummy_test_files/aFileForWhichThereIsNoOpenSubtitlesSubs.mkv"))