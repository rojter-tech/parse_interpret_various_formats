import os, sys, re
from os.path import expanduser
from utils.cmdtools import cmd_request

HOMEPATH = expanduser("~")

ONEDRIVEPATH = os.path.join(HOMEPATH, "OneDrive")
if not os.path.isdir(ONEDRIVEPATH):
    ONEDRIVEPATH = os.path.join(HOMEPATH, "OneDrive - Atea")

ONEDRIVEGIT = os.path.join(ONEDRIVEPATH,"misc","parse_interpret_various_formats")
PROJECTPATH = os.path.join(HOMEPATH,
                           "Environments",
                           "parse_interpret_various_formats")

LOGS_DIR = os.path.join(HOMEPATH,".logs")
if not os.path.isdir(LOGS_DIR):
    os.mkdir(LOGS_DIR)

def logspath(logfile):
    logfile+=".log"
    return os.path.join(LOGS_DIR, logfile)

print("Using Github path:", ONEDRIVEGIT)
print("Using Project path:", PROJECTPATH)

def rsync_local(source, target, reference):
    with open(logspath("rsync"), 'wb') as f: pass
    cmdtool = "rsync -av"
    files = [f for f in os.listdir(reference) if os.path.isfile(f)]
    dirs = [f for f in os.listdir(reference) if os.path.isdir(f)]
    
    for filename, dirname in zip(files, dirs):
        gitfile = os.path.join(source, filename)
        profile = os.path.join(target, filename)
        gitdir = os.path.join(source, dirname, '.')
        prodir = os.path.join(target, dirname)
        rsync_file = cmdtool + ' ' + gitfile + ' ' + profile
        cmd_request(rsync_file, logspath("rsync"))
        rsync_dir = cmdtool + ' ' + gitdir + ' ' + prodir
        cmd_request(rsync_dir, logspath("rsync"))


def main(arguments):
    git, onedrive, sync = False, False, False
    for argument in arguments:
        if argument == '--full':
            git, onedrive = True, True
            break
        elif argument == '--git':
            git = True
        elif argument == '--od':
            onedrive = True
        elif argument == "--sync":
            sync = True


    def gitpush(basedir):
        with open(logspath("gitpush"), 'wb') as f: f.close()
        msg = input("Commit message: ")
        msg = '"' + msg + '"'
        cmd_git = "git add ."
        cmd_request(cmd_git, logspath("gitpush"), basedir=basedir)
        cmd_git = "git commit -m " + msg
        cmd_request(cmd_git, logspath("gitpush"), basedir=basedir)
        cmd_git = "git push"
        cmd_request(cmd_git, logspath("gitpush"), basedir=basedir)


    def gitpull(basedir):
        with open(logspath("gitpull"), 'wb') as f: f.close()
        cmd_git = "git add ."
        cmd_request(cmd_git, logspath("gitpull"), basedir=basedir)
        cmd_git = "git pull"
        cmd_request(cmd_git, logspath("gitpull"), basedir=basedir)


    def od_upload():
        with open(logspath("odsync"), 'wb') as f: f.close()
        cmd = "onedrive --synchronize --upload-only"
        cmd_request(cmd, logspath("odsync"), basedir=ONEDRIVEPATH)


    def od_download():
        with open(logspath("odsync"), 'wb') as f: f.close()
        cmd = "onedrive --synchronize --download-only"
        cmd_request(cmd, logspath("odsync"), basedir=ONEDRIVEPATH)


    def od_sync():
        with open(logspath("odsync"), 'wb') as f: f.close()
        cmd = "onedrive --synchronize"
        cmd_request(cmd, logspath("odsync"), basedir=ONEDRIVEPATH)


    if git:
        gitpull(PROJECTPATH)
        gitpush(PROJECTPATH)
        gitpull(ONEDRIVEGIT)

    if onedrive and git:
        od_upload()
    elif onedrive and not git:
        od_download()
        rsync_local(ONEDRIVEGIT, PROJECTPATH, ONEDRIVEGIT)

    if sync and not git and not onedrive:
        od_sync()


if __name__ == "__main__":
    try:
        arguments = sys.argv[1:]
        main(arguments)
    except IndexError:
        print("No argument given!")
        print("Use either:")
        print("--full")
        print("--git")
        print("--od")
        print("--sync")
