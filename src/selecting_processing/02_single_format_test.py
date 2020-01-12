import os, re
import pandas as pd
import numpy as np

from utils.raw_formats import format_three
from utils.wapi import Word

DATADIR = os.path.join(os.pardir,'data')
WORDDATADIR = os.path.join(DATADIR,'formatted_word_data')

WORDFILE = 'kundfaq_test1.docx'
WORDFILEPATH = os.path.join(WORDDATADIR,WORDFILE)
print("Testing:",WORDFILE,"\n")

wordobject = Word(WORDFILEPATH)

format_three(wordobject.raw_text)