import subprocess

def mergerByM3u8(url, filepath, showshell=False):
    try:
        cmd = "ffmpeg -i " + url + " -c copy -bsf:a aac_adtstoasc \"" + filepath + "\""
        res = subprocess.call(cmd, shell=showshell)
        if res != 0:
            return False
        return True
    except:
        return False

def mergerByFiles(srcfilepaths, filepath, showshell=False):
    try:
        tmpfile = filepath + "TMP.txt"
        with open(tmpfile, 'w') as fd:
            for item in srcfilepaths:
                fd.write('file \'' + item + '\'')

        cmd = "ffmpeg -f concat - i \"" + tmpfile + "\" -c copy \"" + filepath + "\""
        res = subprocess.call(cmd, shell=showshell)
        if res != 0:
            return False
        return True
    except:
        return False
    
