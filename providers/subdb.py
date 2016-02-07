import hashlib
import os

import requests

from src_linux.subdwnld import DownloadException


# Hash function for Subdb

def calculateHash(file_path):

    assert file_path is not None

    read_size = 64 * 1024
    with open(file_path, 'rb') as f:
        data = f.read(read_size)
        f.seek(-read_size, os.SEEK_END)
        data += f.read(read_size)
    return hashlib.md5(data).hexdigest()


def downloadsub(movie):

    user_agent_string = {'User-Agent' : 'SubDB/1.0 (SubDownloader/1.0; http://github.com/kipawa/Sub_Downloader_V1.0)'}
    url = "http://api.thesubdb.com/?action=download&hash=" + calculateHash(movie) + "&language=en"
    req = requests.get(url, headers = user_agent_string)

    if req.status_code == 200:
        fil = os.path.splitext(movie)[0]
        subs = req.text
        subs = subs.encode('utf-8')
        with open(fil + "1.srt", "wb") as subtitle:
            subtitle.write(subs)
    else:
        raise DownloadException("HTTP Status: " + req.status_code)