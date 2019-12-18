from subprocess import Popen, PIPE, STDOUT
import os, sys
DATA_DIR = 'data'
ENCODED_DOCUMENTS_DIR = 'diffrent_encoded_text_data'
ENCODED_DOCUMENTS_PATH = os.path.join('..',DATA_DIR, ENCODED_DOCUMENTS_DIR)
LOGFILE = 'encodings_test' + ".log"
LOGPATH = os.path.join(ENCODED_DOCUMENTS_PATH,LOGFILE)
BUFFLEN = 512

cmdtool = 'chardet'
encoded_files = os.listdir(ENCODED_DOCUMENTS_PATH)
for filename in encoded_files:
    filepath = os.path.join(ENCODED_DOCUMENTS_PATH,filename)
    cmd = cmdtool + ' ' + filepath
    with Popen(cmd, shell=True, stdout=PIPE, stderr=STDOUT, bufsize=BUFFLEN) as process, \
        open(LOGPATH, 'ab',BUFFLEN) as file:
        for line in process.stdout:
            sys.stdout.buffer.write(line)
            file.flush()
            file.write(line)
            file.flush()
