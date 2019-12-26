import os, sys, re
from os.path import expanduser
from utils.cmdtools import cmd_request
HOMEPATH = expanduser("~")
GITHUBPATH = os.path.join(HOMEPATH,
                          "OneDrive",
                          "misc",
                          "parse_interpret_various_formats")
if not os.path.isdir(GITHUBPATH):
    GITHUBPATH = os.path.join(HOMEPATH,
                          "OneDrive - Atea",
                          "misc",
                          "parse_interpret_various_formats")

PROJECTPATH = os.path.join(HOMEPATH,
                           "Environments",
                           "parse_interpret_various_formats")

LOGS_DIR = os.path.join(HOMEPATH,".logs")
if not os.path.isdir(LOGS_DIR):
    os.mkdir(LOGS_DIR)

print("Using Github path:", GITHUBPATH)
print("Using Project path:", PROJECTPATH)

def rsync_local(source, target, reference):
    logspath = os.path.join(LOGS_DIR, "rsync.log")
    with open(logspath, 'wb') as f: pass
    cmdtool = "rsync -av"
    files = [f for f in os.listdir(reference) if os.path.isfile(f)]
    dirs = [f for f in os.listdir(reference) if os.path.isdir(f)]
    
    for filename, dirname in zip(files, dirs):
        gitfile = os.path.join(source, filename)
        profile = os.path.join(target, filename)
        gitdir = os.path.join(source, dirname, '.')
        prodir = os.path.join(target, dirname)
        rsync_file = cmdtool + ' ' + gitfile + ' ' + profile
        cmd_request(rsync_file, logspath)
        rsync_dir = cmdtool + ' ' + gitdir + ' ' + prodir
        cmd_request(rsync_dir, logspath)

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


    def gitpush():
        logspath = os.path.join(LOGS_DIR, "gitpush.log")
        with open(logspath, 'wb') as f: f.close()
        msg = input("Commit message: ")
        msg = '"' + msg + '"'
        cmd_git = "git add ."
        cmd_request(cmd_git, logspath, basedir=PROJECTPATH)
        cmd_git = "git commit -m " + msg
        cmd_request(cmd_git, logspath, basedir=PROJECTPATH)
        cmd_git = "git push"
        cmd_request(cmd_git, logspath, basedir=PROJECTPATH)


    def gitpull():
        logspath = os.path.join(LOGS_DIR, "gitpull.log")
        with open(logspath, 'wb') as f: f.close()
        cmd_git = "git add ."
        cmd_request(cmd_git, logspath, basedir=GITHUBPATH)
        cmd_git = "git pull"
        cmd_request(cmd_git, logspath, basedir=GITHUBPATH)


    def od_upload():
        logspath = os.path.join(LOGS_DIR, "odsync.log")
        with open(logspath, 'wb') as f: f.close()
        cmd_request('onedrive --synchronize --upload-only', logspath)


    def od_download():
        logspath = os.path.join(LOGS_DIR, "odsync.log")
        with open(logspath, 'wb') as f: f.close()
        cmd_request('onedrive --synchronize --download-only', logspath)


    def od_sync():
        logspath = os.path.join(LOGS_DIR, "odsync.log")
        with open(logspath, 'wb') as f: f.close()
        cmd_request('onedrive --synchronize', logspath)


    if git:
        gitpush()
        gitpull()

    if onedrive and git:
        rsync_local(PROJECTPATH, GITHUBPATH, GITHUBPATH)
        rsync_local(GITHUBPATH, PROJECTPATH, GITHUBPATH)
        od_upload()
    elif onedrive and not git:
        od_download()
        rsync_local(GITHUBPATH, PROJECTPATH, GITHUBPATH)

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
