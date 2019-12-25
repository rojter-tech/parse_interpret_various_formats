import os, sys, re
HOMEPATH = os.environ["HOME"]
GITHUBPATH = os.path.join(HOMEPATH,
                          "OneDrive",
                          "misc",
                          "parse_interpret_various_formats")
PROJECTPATH = os.path.join(HOMEPATH,
                           "Environments",
                           "parse_various_formats")
LOGS_DIR = ".logs"


def cmd_request(cmd, LOGPATH, bufflen=512):
    BUFFLEN = bufflen
    from subprocess import Popen, PIPE, STDOUT
    with Popen(cmd, shell=True, stdout=PIPE, stderr=STDOUT, bufsize=BUFFLEN) as process, \
        open(LOGPATH, 'ab', BUFFLEN) as file:
            for line in process.stdout:
                sys.stdout.buffer.write(line)
                file.flush()
                file.write(line)
                file.flush()


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
    gitflag, odflag, rsyncflag = False, False, False
    for argument in arguments:
        if argument == '--full':
            gitflag, odflag, rsyncflag = True, True, True
            break
        elif argument == '--git':
            gitflag = True
        elif argument == '--od':
            odflag = True
        elif argument == '--rsync':
            rsyncflag = True
    
    def gitpush():
        msg = input("Commit message: ")
        msg = "'" + msg + "'"
        cmd_gitpush = 'cd ' + PROJECTPATH + ';' + "git add .;git commit -m " + msg + ';' + 'git push'
        cmd_request(cmd_gitpush, os.path.join(PROJECTPATH,LOGS_DIR,'gitpush.log'))
        
    def gitpull():
        cmd_gitpull = 'cd ' + GITHUBPATH + ';' + "git pull"
        cmd_request(cmd_gitpull, os.path.join(PROJECTPATH,LOGS_DIR,'gitpull.log'))
    
    def od_upload():
        logpath = os.path.join(HOMEPATH, LOGS_DIR, "odsync.log")
        cmd_request('onedrive --synchronize --upload-only', logpath)
    
    def od_sync():
        logpath = os.path.join(HOMEPATH, LOGS_DIR, "odsync.log")
        cmd_request('onedrive --synchronize', logpath)
    
    if gitflag:
        gitpush()
        gitpull()
    if rsyncflag and gitflag:
        rsync_local(GITHUBPATH, PROJECTPATH, GITHUBPATH)
    if rsyncflag and not gitflag:
        rsync_local(PROJECTPATH, GITHUBPATH, GITHUBPATH)
    if odflag and gitflag:
        od_upload()
    if odflag and not gitflag:
        od_sync()
        rsync_local(GITHUBPATH, PROJECTPATH, GITHUBPATH)

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
        print("--rsync")
