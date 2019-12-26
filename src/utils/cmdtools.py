import os, sys

def cmd_request(cmd, logpath, basedir=None, bufflen=512):
    from os.path import expanduser
    HOMEPATH = expanduser("~")
    if not basedir:
        basedir=HOMEPATH
    """Create and OS command line request
    
    Arguments:
        cmd {str} -- Full command string
        logpath {str} -- Path to stdout/stderror file
    
    Keyword Arguments:
        bufflen {int} -- [description] (default: {512})
    """
    os.chdir(basedir)
    from subprocess import Popen, PIPE, STDOUT
    with Popen(cmd, shell=True, stdout=PIPE, stderr=STDOUT, bufsize=bufflen) as process, \
        open(logpath, 'ab', bufflen) as file:
            for line in process.stdout:
                sys.stdout.buffer.write(line)
                file.flush()
                file.write(line)
                file.flush()
