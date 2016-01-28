import hashlib
import os
import requests


#Hash function for Subdb
def get_hash(file_path):
    read_size = 64 * 1024
    with open(file_path, 'rb') as f:
        data = f.read(read_size)
        f.seek(-read_size, os.SEEK_END)
        data += f.read(read_size)
    return hashlib.md5(data).hexdigest()


def downloadsub(movie):
    ua = {'User-Agent' : 'SubDB/1.0 (SubDownloader/1.0; http://github.com/kipawa/Sub_Downloader_V1.0)'}

    hashed = get_hash(movie)

    url = "http://api.thesubdb.com/?action=download&hash=" + hashed + "&language=en"

    req = requests.get(url, headers = ua)

    if req.status_code == 200:
        fil = os.path.splitext(movie)[0]
        subs = req.text
        subs = subs.encode('utf-8')
        with open(fil + "1.srt", "wb") as subtitle:
            subtitle.write(subs)
        return 'Success'
    else:
        return 'Failed'