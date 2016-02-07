import StringIO
import os
import struct
import xmlrpclib
import zipfile
import requests

from custom_exceptions import DownloadException, SubtitlesNotAvailableException


# Hash function for opensubtitles.org
def calculateHash(path_to_the_movie):

    assert path_to_the_movie is not None

    longlongformat = 'q'
    bytesize = struct.calcsize(longlongformat)

    f = open(path_to_the_movie, "rb")

    file_size = os.path.getsize(path_to_the_movie)
    file_hash = file_size

    if file_size < 65536 * 2:
        raise ValueError("File too small")

    for x in range(65536 // bytesize):
        buffer = f.read(bytesize)
        (l_value,) = struct.unpack(longlongformat, buffer)
        file_hash += l_value
        file_hash &= 0xFFFFFFFFFFFFFFFF

    f.seek(max(0, file_size - 65536), 0)
    for x in range(65536 // bytesize):
        buffer = f.read(bytesize)
        (l_value,) = struct.unpack(longlongformat, buffer)
        file_hash += l_value
        file_hash &= 0xFFFFFFFFFFFFFFFF

    f.close()
    return "%016x" % file_hash


def downloadsub(movie):
    # Make conection to opensubtitles
    connection = xmlrpclib.ServerProxy('http://api.opensubtitles.org/xml-rpc')

    # Currently using third party user agent, we are trying to get our own user agent
    try:
        login_response = connection.LogIn('', '', 'en', 'opensubtitles-download 3.2')
    except Exception:
        raise DownloadException("Unable to connect to server. Check your connection.")

    if login_response['status'] != '200 OK':
        raise DownloadException("The server refused the connection")

    hashed = calculateHash(movie)
    size = os.path.getsize(movie)
    search_struct = [{'sublanguageid': 'eng', 'moviehash': hashed, 'moviebytesize': str(size)}]

    res = connection.SearchSubtitles(login_response['token'], search_struct)

    if not res['data']:
        raise SubtitlesNotAvailableException("Subtitles not found in database")
    else:
        link = res['data'][0]['ZipDownloadLink']
        r = requests.get(link)
        z = zipfile.ZipFile(StringIO.StringIO(r.content))

        tmp = os.path.split(movie)[0]
        for mem in z.namelist():
            ext = os.path.splitext(mem)[1]
            fil = os.path.splitext(movie)[0]

            if ext in (".srt", ".sub", ".ssa", ".smi", ".sbv", ".mpl"):
                z.extract(mem, tmp)
                src = tmp + '/' + mem
                destination = fil + '2' + ext
                os.rename(src, destination)
