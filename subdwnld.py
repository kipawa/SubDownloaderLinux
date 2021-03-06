#!/usr/bin/env python3

import tkinter
import os
import threading
import tkinter.messagebox
import tkinter.ttk

from custom_exceptions import SubtitlesNotAvailableException, DownloadException
from providers import opensub, subdb


def prog_bar(root_window: tkinter.Tk) -> None:
    fram = tkinter.ttk.Frame()
    fram.pack(expand=True, fill=tkinter.BOTH, side=tkinter.TOP)
    processing_label = tkinter.Label(fram, text="Please Wait ! We are processing your request...", height=2, font=1)
    processing_label.pack()
    progress_bar = tkinter.ttk.Progressbar(fram, orient='horizontal', length=500, mode='indeterminate')
    progress_bar.pack()
    progress_bar.start(50)
    root_window.mainloop()


def is_filetype_supported(path_to_file: str) -> bool:
    extension = os.path.splitext(path_to_file)[1]
    return extension in ['.webm', '.mkv', '.flv', '.vob', '.ogg', '.drc', '.mng', '.avi', '.mov', '.qt', '.wmv', '.net',
                         '.yuv', '.rm', '.rmvb', '.asf', '.m4p', '.m4v', '.mp4', '.mpeg', '.mpg', '.mpv', '.mp2',
                         '.m2v', '.m4v', '.svi', '.3gp', '.3g2', '.mxf', '.roq', '.nsv']


def downloadsub(root_window: tkinter.Tk) -> None:

    for current_path in get_selected_movie_paths():

        if not is_filetype_supported(current_path):
            tkinter.messagebox.showerror("Kipawa Sub Downloader", "This is not a supported movie file")
        else:

            try:
                if subdb_subtitles_exist(current_path):
                    try:
                        subdb.download_subtitles(current_path)
                        tkinter.messagebox.showinfo("Kipawa Sub Downloader", "Subtitles downloaded successfully!")
                    except SubtitlesNotAvailableException:
                        tkinter.messagebox.showinfo("Kipawa Sub Downloader", "Sorry ! Better subtitles not found")

                elif opensubtitles_subs_exist(current_path):
                    try:
                        opensub.downloadsub(current_path)
                        tkinter.messagebox.showinfo("Kipawa Sub Downloader", "Subtitles downloaded succesdfully!")
                    except SubtitlesNotAvailableException:
                        tkinter.messagebox.showinfo("Kipawa Sub Downloader", "Sorry ! Better subtitles not found")
                else:
                    try:
                        download_default_subtitles(current_path)
                        tkinter.messagebox.showinfo("Kipawa Sub Downloader", "Subtitles downloaded succesdfully!")
                    except SubtitlesNotAvailableException:
                        tkinter.messagebox.showinfo("Kipawa Sub Downloader", "Sorry, no subtitles were found")

            except DownloadException as e:
                tkinter.messagebox.showinfo("Kipawa Sub Downloader", "Error downloading subtitles: " + str(e))
            except ValueError as e:
                tkinter.messagebox.showinfo("Kipawa Sub Downloader", "There is a problem with this file: " + str(e))

    root_window.quit()


def subdb_subtitles_exist(path_to_the_movie: str) -> bool:
    path_without_extension = path_without_file_extension(path_to_the_movie)
    for subtitle_extension in {'.srt', '.sub', '.ssa', '.smi', '.sbv', '.mpl'}:
        subtitle_path = path_without_extension + "1" + subtitle_extension
        if os.path.exists(subtitle_path):
            return True

    return False

def get_selected_movie_paths():
    #there is a empty string after the last line break
    return os.environ["NAUTILUS_SCRIPT_SELECTED_FILE_PATHS"].split("\n")[:-1]


def path_without_file_extension(path_to_a_file: str) -> str:
    return os.path.splitext(path_to_a_file)[0]


def opensubtitles_subs_exist(path_to_the_movie: str) -> bool:
    path_without_extension = path_without_file_extension(path_to_the_movie)
    for subtitle_extension in {'.srt', '.sub', '.ssa', '.smi', '.sbv', '.mpl'}:
        subtitle_path = path_without_extension + "2" + subtitle_extension
        if os.path.exists(subtitle_path):
            return True

    return False


def download_default_subtitles(path_to_the_movie: str) -> None:
    try:
        subdb.download_subtitles(path_to_the_movie)
    except (DownloadException, SubtitlesNotAvailableException):
        opensub.downloadsub(path_to_the_movie)

def main():
    root_window = tkinter.Tk()
    root_window.wm_title("Kipawa Sub Downloader")
    root_window.geometry('{}x{}'.format(400, 63))
    t1 = threading.Thread(target=downloadsub, args=(root_window,))
    t1.start()
    prog_bar(root_window)
    t1.join()

if __name__ == "__main__":
    main()
