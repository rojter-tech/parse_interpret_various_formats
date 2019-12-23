import os, re
import pandas as pd
import numpy as np
from itertools import combinations
from wapi import Word
from wapi import attribute_on_off_separation

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

BOLD = r"{bval:"
ITALIC = r"{ival:"
COLOR = r"{nondefaultcolor:"
ATTRIBUTES = [BOLD, ITALIC, COLOR]
WHITESPACE = r'\s'
NON_WHITEPACE = r'\S'

def main():
    dfs = []
    for wordfile, wordcontent in zip(WORDFILES, wordcontents):
        print("***************************************************","\nTrying:",wordfile,"...")
        check = 0
        for testattr in ATTRIBUTES:
            try:
                qadf = attribute_on_off_separation(testattr, wordcontent)
                dfs.append(qadf)
                check = 1
                break
            except AssertionError:
                pass

        if check:
            print(wordfile, "QA was successfully loaded")
        else:
            print("")
            print("***********************************************")
            print("**!!!!Attribute separation did not sucess!!!!**")
            print("***********************************************")
            print("")
            print("QA by " + wordfile + " maybe were not formatted by attribute, check other options ...")
    
    n_dfs = len(dfs)
    for df1, df2 in combinations(range(n_dfs), 2):
        check_equal = (dfs[df1] == dfs[df2])
        has_false = False in check_equal.values
        if not has_false:
            print('Dataframe',df1,'and',df2,'has no element that differ')
        else:
            print('  Ops! Dataframe',df1,'and',df2,'has element that differ!')


if __name__ == "__main__":
    main()
