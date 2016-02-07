#!/usr/bin/env python2

import Tkinter
import os
import sys
import threading
import tkMessageBox
import ttk

from custom_exceptions import SubtitlesNotAvailableException, DownloadException
from providers import opensub, subdb


def prog_bar(root):
    fram = ttk.Frame()
    fram.pack(expand=True, fill=Tkinter.BOTH, side=Tkinter.TOP)
    lab = Tkinter.Label(fram, text="Please Wait ! We are processing your request...", height=2, font=1)
    lab.pack()
    pb = ttk.Progressbar(fram, orient='horizontal', length=500, mode='indeterminate')
    pb.pack()
    pb.start(50)
    root.mainloop()


def is_filetype_supported(path_to_file):
    extension = os.path.splitext(path_to_file)[1]
    return extension in ['.webm', '.mkv', '.flv', '.vob', '.ogg', '.drc', '.mng', '.avi', '.mov', '.qt', '.wmv', '.net',
                   '.yuv', '.rm', '.rmvb', '.asf', '.m4p', '.m4v', '.mp4', '.mpeg', '.mpg', '.mpv', '.mp2', '.m2v',
                   '.m4v', '.svi', '.3gp', '.3g2', '.mxf', '.roq', '.nsv']


def downloadsub(path_to_the_movie, root_window):

    if not is_filetype_supported(path_to_the_movie):
        tkMessageBox.showerror("Kipawa Sub Downloader", "This is not a supported movie file")
    else:

        try:
            if subdb_subtitles_exist(path_to_the_movie):
                try:
                    subdb.downloadsub(path_to_the_movie)
                    tkMessageBox.showinfo("Kipawa Sub Downloader", "Subtitles downloaded successfully!")
                except SubtitlesNotAvailableException:
                    tkMessageBox.showinfo("Kipawa Sub Downloader", "Sorry ! Better subtitles not found")

            elif opensubtitles_subs_exist(path_to_the_movie):
                try:
                    opensub.downloadsub(path_to_the_movie)
                    tkMessageBox.showinfo("Kipawa Sub Downloader", "Subtitles downloaded succesdfully!")
                except SubtitlesNotAvailableException:
                    tkMessageBox.showinfo("Kipawa Sub Downloader", "Sorry ! Better subtitles not found")
            else:
                try:
                    download_default_subtitles(path_to_the_movie)
                    tkMessageBox.showinfo("Kipawa Sub Downloader", "Subtitles downloaded succesdfully!")
                except SubtitlesNotAvailableException:
                    tkMessageBox.showinfo("Kipawa Sub Downloader", "Sorry, no subtitles were found")

        except DownloadException as e:
            tkMessageBox.showinfo("Kipawa Sub Downloader", "Error downloading subtitles: " + e.message)


    root_window.quit()


def subdb_subtitles_exist(path_to_the_movie):
    path_without_extension = path_without_file_extension(path_to_the_movie)
    for subtitle_extension in {'.srt', '.sub', '.ssa', '.smi', '.sbv', '.mpl'}:
        subtitle_path = path_without_extension + "1" + subtitle_extension
        if os.path.exists(subtitle_path):
            return True

    return False


def path_without_file_extension(path_to_a_file):
    return os.path.splitext(path_to_a_file)[0]


def opensubtitles_subs_exist(path_to_the_movie):
    path_without_extension = path_without_file_extension(path_to_the_movie)
    for subtitle_extension in {'.srt', '.sub', '.ssa', '.smi', '.sbv', '.mpl'}:
        subtitle_path = path_without_extension + "2" + subtitle_extension
        if os.path.exists(subtitle_path):
            return True

    return False


def download_default_subtitles(path_to_the_movie):
    try:
        subdb.downloadsub(path_to_the_movie)
    except Exception:
        opensub.downloadsub(path_to_the_movie)


if __name__ == "__main__":
    root_window = Tkinter.Tk()
    root_window.wm_title("Kipawa Sub Downloader")
    root_window.geometry('{}x{}'.format(400, 63))
    path_to_the_movie = sys.argv[1]
    t1 = threading.Thread(target=downloadsub, args=(path_to_the_movie, root_window,))
    t1.start()
    prog_bar(root_window)
    t1.join()


