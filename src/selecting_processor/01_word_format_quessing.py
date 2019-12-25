import os, re
import pandas as pd
import numpy as np

from itertools import combinations
from utils.wapi import Word
from utils.errors import Error, rOjterError
from utils.attrib_separator import try_separate_by_attribute
from utils.raw_formats import format_one

DATADIR = os.path.join(os.pardir,'data')
WORDDATADIR = os.path.join(DATADIR,'formatted_word_data')
# Source files
WORDFILES = os.listdir(WORDDATADIR)
wordcontents = []
wordattributes = {}
wordobjects = []

for WORDFILE in WORDFILES:
    WORDFILEPATH = os.path.join(WORDDATADIR,WORDFILE)
    WORDDOCUMENT = Word(WORDFILEPATH)
    wordobjects.append(WORDDOCUMENT)


def main():
    dfs = []
    non_attribute = []
    unknown_format = []
    for wordobject in wordobjects:
        qadata = try_separate_by_attribute(wordobject)
        if type(qadata) == str:
            print("File",qadata,"appended to non attribute separated files list")
            non_attribute.append(qadata)
            try:
                qadf = format_one(wordobject.raw_text)
                if len(qadf) != 0:
                    dfs.append(qadf)
            except rOjterError:
                print(wordobject.filename, "have unknown format.")
                unknown_format.append(wordobject.filename)
                pass  
        else:
            dfs.append(qadata)
    
    n_dfs = len(dfs)
    print()
    for df1, df2 in combinations(range(n_dfs), 2):
        check_equal = (dfs[df1] == dfs[df2])
        has_false = False in check_equal.values
        if not has_false:
            print('Dataframe',df1,'and',df2,'has no element that differ')
        else:
            print('  Ops! Dataframe',df1,'and',df2,'has element that differ!')
    
    print("\nNon attribute separated files:\n",non_attribute)
    print("\nUnknown format files:\n",unknown_format)


if __name__ == "__main__":
    main()
