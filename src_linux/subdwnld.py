import Tkinter
import os
import sys
import threading
import tkMessageBox
import ttk
from src_linux.providers import opensub, subdb


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
    ext = os.path.splitext(path_to_file)[1]
    return ext in ['.webm', '.mkv', '.flv', '.vob', '.ogg', '.drc', '.mng', '.avi', '.mov', '.qt', '.wmv', '.net',
                   '.yuv', '.rm', '.rmvb', '.asf', '.m4p', '.m4v', '.mp4', '.mpeg', '.mpg', '.mpv', '.mp2', '.m2v',
                   '.m4v', '.svi', '.3gp', '.3g2', '.mxf', '.roq', '.nsv']


def downloadsub(movie, root):
    if is_filetype_supported(movie):

        fil, ex = os.path.splitext(movie)
        fil += '1'
        exists = 0

        for ext in {'.srt', '.sub', '.ssa', '.smi', '.sbv', '.mpl'}:
            sub = fil + ext
            if os.path.exists(sub):
                exists = 1
                break

        if exists == 0:
            fil, ex = os.path.splitext(movie)
            fil += '2'
            for ext in {'.srt', '.sub', '.ssa', '.smi', '.sbv', '.mpl'}:
                sub = fil + ext
                if os.path.exists(sub):
                    exists = 2
                    break

            res = subdb.downloadsub(movie)

            if res == 'Success' and exists != 2:
                tkMessageBox.showinfo("Kipawa Sub Downloader", "Subtitle Downloaded Successfully")
            elif res == 'Success' and exists == 2:
                tkMessageBox.showinfo("Kipawa Sub Downloader", "Subtitle Downloaded Successfully")
                os.remove(sub)
            elif res == 'Failed' and exists == 2:
                tkMessageBox.showinfo("Kipawa Sub Downloader", "Sorry ! Better subtitle not found")
            else:
                res2 = opensub.downloadsub(movie)

        else:
            res2 = opensub.downloadsub(movie)
            os.remove(sub)
    else:
        tkMessageBox.showerror("Kipawa Sub Downloader", "This is not a supported movie file")

    root.quit()


if __name__ == "__main__":
    root = Tkinter.Tk()
    root.wm_title("Kipawa Sub Downloader")
    root.geometry('{}x{}'.format(400, 63))
    path_to_the_movie = sys.argv[1]
    t1 = threading.Thread(target=downloadsub, args=(path_to_the_movie, root,))
    t1.start()
    prog_bar(root)
    t1.join()
