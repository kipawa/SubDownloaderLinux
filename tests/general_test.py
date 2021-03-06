import os
import unittest

from subdwnld import is_filetype_supported, subdb_subtitles_exist, path_without_file_extension, opensubtitles_subs_exist, get_selected_movie_paths


class GeneralTests(unittest.TestCase):

    def test_is_filetype_supported(self):
        self.assertTrue(is_filetype_supported("simplename.flv"))
        self.assertTrue(is_filetype_supported("/a/full/path/name.mkv"))
        self.assertFalse(is_filetype_supported(".jpg"))

    def test_subdb_subtitles_exist(self):
        self.assertTrue(subdb_subtitles_exist("dummy_test_files/aFileForWhichThereIsASubDbSubtitle.mkv"))
        self.assertFalse(subdb_subtitles_exist("dummy_test_files/aFileForWhichThereIsNoSubDbSubtitle.mkv"))

    def test_path_without_file_extension(self):
        self.assertEqual("afile", path_without_file_extension("afile.txt"))
        self.assertEqual("/a/file/with/full/path", path_without_file_extension("/a/file/with/full/path.mkv"))
        self.assertEqual("a/file/without/extension", path_without_file_extension("a/file/without/extension"))

    def test_opensubtitles_subs_exist(self):
        self.assertTrue(opensubtitles_subs_exist("dummy_test_files/aFileForWhichThereIsOpenSubtitlesSubs.mkv"))
        self.assertFalse(opensubtitles_subs_exist("dummy_test_files/aFileForWhichThereIsNoOpenSubtitlesSubs.mkv"))

    def test_get_selected_movie_paths(self):

        # two files
        os.environ["NAUTILUS_SCRIPT_SELECTED_FILE_PATHS"] = "test_media_files/dexter.mp4\ntest_media_files/breakdance.avi\n"
        self.assertListEqual(["test_media_files/dexter.mp4", "test_media_files/breakdance.avi"], get_selected_movie_paths())

        # one file
        os.environ["NAUTILUS_SCRIPT_SELECTED_FILE_PATHS"] = "test_media_files/dexter.mp4\n"
        self.assertListEqual(["test_media_files/dexter.mp4"], get_selected_movie_paths())
