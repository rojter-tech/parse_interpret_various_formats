import os, re
import pandas as pd
import numpy as np

from itertools import combinations
from utils.wapi import Word
from utils.errors import Error, rOjterError
from utils.attrib_formats import try_separate_by_attribute
from utils.raw_formats import try_separate_by_rawtext

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


def try_separate_by_rawtext(wordobject, format_functions):
    check = False
    for format_function in format_functions:
        try:
            qadf = format_function(wordobject.raw_text)
            if len(qadf) != 0:
                check = True
            else:
                print("DataFrame size invalid")
                raise rOjterError
            break
        except rOjterError:
            print(wordobject.filename, "format excluded.")
    
    if check:
        return qadf
    else:
        print("")
        print("***********************************************")
        print("**!!!!Format detection did not sucess!!!!**")
        print("***********************************************")
        print("")
        print("QA by " + wordobject.filename + " format could not be determined ...")
        return wordobject.filename


def test_summary(dfs, attribute_files, raw_text_files, unknown_format):
    dfs_files = list(dfs.keys()); n_dfs = len(dfs)
    checkcompare = True
    for df1, df2 in combinations(range(n_dfs), 2):
        check_equal = (dfs[dfs_files[df1]] == dfs[dfs_files[df2]])
        has_false = False in check_equal.values
        if has_false:
            checkcompare = False
            print('  Ops! Dataframe',dfs_files[df1],'and',dfs_files[df2],'has element that differ!')
    

    print("\nAttribute separated files:\n",attribute_files)
    print("\nRaw separated files:\n",raw_text_files)
    print("\nUnknown format files:\n",unknown_format)
    if checkcompare:
        print("\nAll processed dataframes is equal! Yey!")
    else:
        print("  Watch out! There is dataframes that are inequal")
    print("Number of files checked:",len(dfs_files))

def main():
    dfs = {}
    attribute_files = []
    raw_text_files = []
    unknown_format = []

    for wordobject in wordobjects:
        qadata, format_type = process_wordobject(wordobject, format_type = None)

        if format_type == "Attribute":
            attribute_files.append(wordobject.filename)
            dfs[wordobject.filename] = qadata
        elif format_type == "RawTextFormat":
            raw_text_files.append(wordobject.filename)
            dfs[wordobject.filename] = qadata
        else:
            unknown_format.append(wordobject.filename)
    
    test_summary(dfs, attribute_files, raw_text_files, unknown_format)





if __name__ == "__main__":
    main()
