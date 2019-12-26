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

print(os.path.isdir(GITHUBPATH))

PROJECTPATH = os.path.join(HOMEPATH,
                           "Environments",
                           "parse_interpret_various_formats")
LOGS_DIR = "logs"
print("Using Github path:", GITHUBPATH)
print("Using Project path:", PROJECTPATH)

def rsync_local(source, target, reference):
    logs_dir = LOGS_DIR
    logfile = "rsync" + ".log"
    logpath = os.path.join(reference,logs_dir,logfile)
    f = open(logpath,'wb'); f.close()
    cmdtool = "rsync -av"
    files = [f for f in os.listdir(reference) if os.path.isfile(f)]
    dirs = [f for f in os.listdir(reference) if os.path.isdir(f)]
    
    for filename, dirname in zip(files, dirs):
        gitfile = os.path.join(source, filename)
        profile = os.path.join(target, filename)
        gitdir = os.path.join(source, dirname, '.')
        prodir = os.path.join(target, dirname)
        rsync_file = cmdtool + ' ' + gitfile + ' ' + profile
        cmd_request(rsync_file, logpath)
        rsync_dir = cmdtool + ' ' + gitdir + ' ' + prodir
        cmd_request(rsync_dir, logpath)

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
        logpath = os.path.join(PROJECTPATH,LOGS_DIR,'gitpush.log')
        with open(logpath, 'wb') as f: pass
        msg = input("Commit message: ")
        msg = "'" + msg + "'"
        cmd_git = "git add ."
        cmd_request(cmd_git, logpath, basedir=PROJECTPATH)
        cmd_git = "git commit -m " + msg
        cmd_request(cmd_git, logpath, basedir=PROJECTPATH)
        cmd_git = "git push"
        cmd_request(cmd_git, logpath, basedir=PROJECTPATH)
    
    def gitpull():
        logpath = os.path.join(PROJECTPATH,LOGS_DIR,'gitpush.log')
        with open(logpath, 'wb') as f: pass
        cmd_git = "git add ."
        cmd_request(cmd_git, logpath, basedir=GITHUBPATH)
        cmd_git = "git pull"
        cmd_request(cmd_git, logpath, basedir=GITHUBPATH)
    
    def od_upload():
        logpath = os.path.join(HOMEPATH, LOGS_DIR, "odsync.log")
        cmd_request('onedrive --synchronize --upload-only', logpath)
    
    def od_download():
        logpath = os.path.join(HOMEPATH, LOGS_DIR, "odsync.log")
        cmd_request('onedrive --synchronize --download-only', logpath)
    
    def od_sync():
        logpath = os.path.join(HOMEPATH, LOGS_DIR, "odsync.log")
        cmd_request('onedrive --synchronize', logpath)
    
    if git:
        gitpush()
        gitpull()
    if onedrive and not git:
        od_download()
        rsync_local(GITHUBPATH, PROJECTPATH, GITHUBPATH)
    elif onedrive and git:
        rsync_local(PROJECTPATH, GITHUBPATH, GITHUBPATH)
        rsync_local(GITHUBPATH, PROJECTPATH, GITHUBPATH)
        od_upload()
    if sync and not git and not onedrive:
        od_sync()
    

if __name__ == "__main__":
    try:
        arguments = sys.argv[1:]
        arguments = ['--git']
        main(arguments)
    except IndexError:
        print("No argument given!")
        print("Use either:")
        print("--full")
        print("--git")
        print("--od")
        print("--sync")
