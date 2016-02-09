import hashlib
import os
import requests

from custom_exceptions import DownloadException


# Hash function for Subdb
def calculate_hash(file_path) -> str:

    assert file_path is not None

    read_size = 64 * 1024
    with open(file_path, 'rb') as f:
        data = f.read(read_size)
        f.seek(-read_size, os.SEEK_END)
        data += f.read(read_size)
    return hashlib.md5(data).hexdigest()


def download_subtitles(movie) -> None:

    user_agent_string = {'User-Agent': 'SubDB/1.0 (SubDownloader/1.0; http://github.com/kipawa/Sub_Downloader_V1.0)'}
    url = "http://api.thesubdb.com/?action=download&hash=" + calculate_hash(movie) + "&language=en"
    request_result = requests.get(url, headers=user_agent_string)

    if request_result.status_code == 200:
        fil = os.path.splitext(movie)[0]
        subs = request_result.text
        subs = subs.encode('utf-8')
        with open(fil + "1.srt", "wb") as subtitle:
            subtitle.write(subs)
    else:
        raise DownloadException("HTTP Status: " + str(request_result.status_code))


