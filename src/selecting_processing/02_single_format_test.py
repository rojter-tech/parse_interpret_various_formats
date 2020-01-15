import os, re
import pandas as pd
import numpy as np

from utils.raw_formats import format_two
from utils.wapi import Word

DATADIR = os.path.join(os.pardir,'data')
WORDDATADIR = os.path.join(DATADIR,'formatted_word_data')

WORDFILE = 'QA_line_segment.docx'
WORDFILEPATH = os.path.join(WORDDATADIR,WORDFILE)
print("Testing:",WORDFILE,"\n")

wordobject = Word(WORDFILEPATH)

format_two(wordobject)