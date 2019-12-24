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
WORDFILES = os.listdir(WORDDATADIR)
wordcontents = []
wordattributes = {}
for WORDFILE in WORDFILES:
    WORDFILEPATH = os.path.join(WORDDATADIR,WORDFILE)
    WORDDOCUMENT = Word(WORDDATADIR, WORDFILE)
    WORDCONTENT, ATTRIBUTES_DICT = WORDDOCUMENT.extract_paragraphs_content_with_attributes()
    wordcontents.append(WORDCONTENT)
    wordattributes[WORDFILE] = ATTRIBUTES_DICT


def main():
    dfs = []
    non_attribute = []
    for wordfile, wordcontent in zip(WORDFILES, wordcontents):
        qadata = try_separate_by_attribute(wordfile, wordcontent)
        if type(qadata) == str:
            print("File",qadata,"appended to non attribute separated files list")
            non_attribute.append(qadata)
            qadata = clean_qalistfile(extract_raw_text(wordcontent))
            dfs.append(qadata)
        else:
            dfs.append(qadata)
    
    n_dfs = len(dfs)
    for df1, df2 in combinations(range(n_dfs), 2):
        check_equal = (dfs[df1] == dfs[df2])
        has_false = False in check_equal.values
        if not has_false:
            print('Dataframe',df1,'and',df2,'has no element that differ')
        else:
            print('  Ops! Dataframe',df1,'and',df2,'has element that differ!')
    
    print("\nNon attribute separated files:\n",non_attribute)


if __name__ == "__main__":
    main()
