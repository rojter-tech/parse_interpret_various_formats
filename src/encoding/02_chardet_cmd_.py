import os, sys, re
from utils.cmdtools import cmd_request
DATA_DIR = 'data'
ENCODED_DOCUMENTS_DIR = 'encoded_text_data'
ENCODED_DOCUMENTS_PATH = os.path.join(os.pardir, DATA_DIR, ENCODED_DOCUMENTS_DIR)

LOGS_DIR = 'logs'
LOGFILE = 'encodings_test' + ".log"
LOGPATH = os.path.join(ENCODED_DOCUMENTS_PATH,LOGS_DIR,LOGFILE)
f = open(LOGPATH,'wb');f.cloese()

cmdtool = 'chardet'
encoded_files = os.listdir(ENCODED_DOCUMENTS_PATH)
for filename in encoded_files:
    if re.match(r'.*txt',filename):
        filepath = os.path.join(ENCODED_DOCUMENTS_PATH, filename)
        cmd = cmdtool + ' ' + filepath
        cmd_request(cmd, LOGPATH)
