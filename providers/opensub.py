import StringIO
import os
import struct
import xmlrpclib
import zipfile

import requests

from custom_exceptions import DownloadException, SubtitlesNotAvailableException

# Hash function for opensubtitles.org
def calculateHash(movie):

    assert movie is not None

    longlongformat = 'q'
    bytesize = struct.calcsize(longlongformat)

    f = open(movie, "rb")

    filesize = os.path.getsize(movie)
    hash = filesize

    if filesize < 65536 * 2:
        raise ValueError("File too small")

    for x in range(65536 // bytesize):
        buffer = f.read(bytesize)
        (l_value,) = struct.unpack(longlongformat, buffer)
        hash += l_value
        hash = hash & 0xFFFFFFFFFFFFFFFF

    f.seek(max(0, filesize - 65536), 0)
    for x in range(65536 // bytesize):
        buffer = f.read(bytesize)
        (l_value,) = struct.unpack(longlongformat, buffer)
        hash += l_value
        hash = hash & 0xFFFFFFFFFFFFFFFF

    f.close()
    returnedhash = "%016x" % hash
    return returnedhash


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
            if ext == '.srt' or ext == '.sub' or ext == '.ssa' or ext == '.smi' or ext == '.sbv' or ext == '.mpl':
                z.extract(mem, tmp)
                src = tmp + '/' + mem
                dest = fil + '2' + ext
                os.rename(src, dest)
