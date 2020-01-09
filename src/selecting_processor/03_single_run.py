import os, re
import pandas as pd
import numpy as np
from itertools import combinations
from utils.wapi import Word
from utils.attrib_separator import try_separate_by_attribute
from utils.raw_formats import format_one

DATADIR = os.path.join(os.pardir,'data')
WORDDATADIR = os.path.join(DATADIR,'formatted_word_data')


# Source files
wordfile = 'QA.docx'
wordobject = Word(os.path.join(WORDDATADIR,wordfile))

def main():
    qadata = try_separate_by_attribute(wordobject)
    if type(qadata) == str:
        qadf = format_one(wordobject.raw_text)
        print(qadf)
    else:
        print("File", qadata, " is a attribute separated file")


if __name__ == "__main__":
    main()
