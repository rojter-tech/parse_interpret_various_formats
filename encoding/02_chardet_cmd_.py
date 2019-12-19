from subprocess import Popen, PIPE, STDOUT
import os, sys, re
DATA_DIR = 'data'
ENCODED_DOCUMENTS_DIR = 'encoded_text_data'

ENCODED_DOCUMENTS_PATH = os.path.join(os.pardir, DATA_DIR, ENCODED_DOCUMENTS_DIR)

LOGS_DIR = 'logs'
LOGFILE = 'encodings_test' + ".log"
LOGPATH = os.path.join(ENCODED_DOCUMENTS_PATH,LOGS_DIR,LOGFILE)
open(LOGPATH,'wb')
BUFFLEN = 512

cmdtool = 'chardet'
encoded_files = os.listdir(ENCODED_DOCUMENTS_PATH)
for filename in encoded_files:
    if re.match(r'.*txt',filename):
        filepath = os.path.join(ENCODED_DOCUMENTS_PATH, filename)
        cmd = cmdtool + ' ' + filepath
        with Popen(cmd, shell=True, stdout=PIPE, stderr=STDOUT, bufsize=BUFFLEN) as process, \
            open(LOGPATH,'ab',BUFFLEN) as file:
                for line in process.stdout:
                    sys.stdout.buffer.write(line)
                    file.flush()
                    file.write(line)
                    file.flush()
