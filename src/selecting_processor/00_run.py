import os, re
import pandas as pd
import numpy as np
from itertools import combinations
from utils.wapi import Word
from utils.wapi import try_separate_by_attribute
from utils.wapi import extract_raw_text
from utils.wapi import clean_qalistfile

DATADIR = os.path.join(os.pardir,'data')
WORDDATADIR = os.path.join(DATADIR,'formatted_word_data')


# Source files
WORDFILE = 'QA_mi.docx'
WORDDOCUMENT = Word(WORDDATADIR, WORDFILE)
WORDCONTENT, ATTRIBUTES_DICT = WORDDOCUMENT.extract_paragraphs_content_with_attributes()

def main():
    wordfile = WORDFILE
    wordcontent = WORDCONTENT
    qadata = try_separate_by_attribute(wordfile, wordcontent)
    if type(qadata) == str:
        file_lines = extract_raw_text(wordcontent)
        qadf = clean_qalistfile(file_lines)
        print(qadf)
    else:
        print("File", qadata, " is a attribute separated file")


if __name__ == "__main__":
    main()
