import xmlrpclib
import struct, os, sys
import requests
import zipfile
import StringIO
import tkMessageBox
import threading


#Hash function for opensubtitles.org
def hashfunc(movie):
    try:
        longlongformat = 'q'
        bytesize = struct.calcsize(longlongformat)

        f = open(movie, "rb")

        filesize = os.path.getsize(movie)
        hash = filesize

        if filesize < 65536 * 2:
            return "SizeError"

        for x in range(65536//bytesize):
            buffer = f.read(bytesize)
            (l_value,)= struct.unpack(longlongformat, buffer)
            hash += l_value
            hash = hash & 0xFFFFFFFFFFFFFFFF

        f.seek(max(0,filesize-65536),0)
        for x in range(65536//bytesize):
            buffer = f.read(bytesize)
            (l_value,)= struct.unpack(longlongformat, buffer)
            hash += l_value
            hash = hash & 0xFFFFFFFFFFFFFFFF

        f.close()
        returnedhash =  "%016x" % hash
        return returnedhash
    except(IOError):
        return "IOError"


def downloadsub(movie):
    #Make conection to opensubtitles
    resp = xmlrpclib.ServerProxy('http://api.opensubtitles.org/xml-rpc')


    #Currently using third party user agent, we are trying to get our own user agent
    try:
        log_resp = resp.LogIn('','','en','opensubtitles-download 3.2')
    except Exception:
        tkMessageBox.showerror("Kipawa Sub Downloader", "Cannot connect to server! Check your connection")
        sys.exit(1)

    if log_resp['status'] != '200 OK':
        tkMessageBox.showerror("Kipawa Sub Downloader", "Server refused the connection")
        sys.exit(1)

    hashed = hashfunc(movie)
    size = os.path.getsize(movie)
    search_struct = []
    search_struct.append({'sublanguageid' : 'eng', 'moviehash' : hashed, 'moviebytesize' : str(size)})

    res = resp.SearchSubtitles(log_resp['token'], search_struct)

    if res['data'] == False:
        tkMessageBox.showinfo("Kipawa Sub Downloader", "Subtitles not found in database")
    else:
        link = res['data'][0]['ZipDownloadLink']
        r = requests.get(link)
        z = zipfile.ZipFile(StringIO.StringIO(r.content))
        flag = 0

        tmp = os.path.split(movie)[0]
        for mem in z.namelist():
            ext = os.path.splitext(mem)[1]
            fil = os.path.splitext(movie)[0]
            if ext == '.srt' or ext == '.sub' or ext == '.ssa' or ext == '.smi' or ext == '.sbv' or ext == '.mpl':
                z.extract(mem, tmp)
                src = tmp+'/'+mem
                dest = fil + '2' + ext
                os.rename(src, dest)
                flag = 1

        tkMessageBox.showinfo("Kipawa Sub Downloader", "Subtitles Downloaded Successfully")
