import os, re
import pandas as pd
import numpy as np

from utils.wapi import Word
from utils.format_detection_tools import multiple_object_diagnostics

DATADIR = os.path.join(os.pardir,'data')
WORDDATADIR = os.path.join(DATADIR,'formatted_word_data')
# Source files
WORDFILES = os.listdir(WORDDATADIR)
wordcontents = []
wordattributes = {}
wordobjects = []

for WORDFILE in WORDFILES:
    WORDFILEPATH = os.path.join(WORDDATADIR,WORDFILE)
    print(WORDFILE)
    WORDDOCUMENT = Word(WORDFILEPATH)
    wordobjects.append(WORDDOCUMENT)

def main():
    multiple_object_diagnostics(wordobjects)


if __name__ == "__main__":
    main()
