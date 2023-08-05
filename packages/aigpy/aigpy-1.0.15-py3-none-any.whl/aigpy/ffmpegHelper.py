import subprocess
import os

def mergerByM3u8(url, filepath, showshell=False):
    try:
        cmd = "ffmpeg -safe 0 -i " + url + " -c copy -bsf:a aac_adtstoasc \"" + filepath + "\""
        res = subprocess.call(cmd, shell=showshell)
        if res != 0:
            return False
        return True
    except:
        return False

def mergerByFiles(srcfilepaths, filepath, showshell=False):
    result = True
    tmpfile = filepath + "TMP.txt"
    try:
        with open(tmpfile, 'w') as fd:
            for item in srcfilepaths:
                fd.write('file \'' + item + '\'')

        cmd = "ffmpeg -f concat -safe 0 -i \"" + tmpfile + "\" -c copy \"" + filepath + "\""
        res = subprocess.call(cmd, shell=showshell)
        if res != 0:
            result = False
    except:
        result = False

    if os.access(tmpfile):
        os.remove(tmpfile)
    return result
