import os, re
import pandas as pd
import numpy as np

from itertools import combinations
from utils.wapi import Word
from utils.errors import Error, rOjterError
from utils.attrib_formats import try_separate_by_attribute
from utils.raw_formats import format_functions

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

def print_summary(attribute_files, non_attribute_files, unknown_format):
    print("\nAttribute separated files:\n",attribute_files)
    print("\nNon attribute separated files:\n",non_attribute_files)
    print("\nUnknown format files:\n",unknown_format)


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


def try_wordfile(wordobject, format_type = None):
    print("Processing", wordobject.filename)
    qadata = try_separate_by_attribute(wordobject)

    if type(qadata) == str:
        qadata = try_separate_by_rawtext(wordobject, format_functions)
    else:
        format_type = "Attribute"
        return qadata, format_type

    if type(qadata) == str:
        print("No separation process attempt did succeeded for",qadata)
        return qadata
    else:
        format_type = "RawTextFormat"
        return qadata, format_type

def main():
    dfs = {}
    attribute_files = []
    non_attribute_files = []
    unknown_format = []
    for wordobject in wordobjects:
        print("Processing", wordobject.filename)

        qadata = try_separate_by_attribute(wordobject)
        once_unknown, once_attribute  = True, True
        if type(qadata) == str:
            print("File", qadata, "appended to non attribute separated files list")
            for format_function in format_functions:
                try:
                    qadf = format_function(wordobject.raw_text)
                    if len(qadf) != 0:
                        dfs[wordobject.filename] = qadf
                    if once_attribute and once_unknown:
                        non_attribute_files.append(wordobject.filename)
                        once_attribute = False
                    break
                except rOjterError:
                    
                    print(wordobject.filename, "format excluded.")
            if once_unknown and once_attribute:
                unknown_format.append(wordobject.filename)
                once_unknown = False
        else:
            dfs[wordobject.filename] = qadata
            attribute_files.append(wordobject.filename)

    dfs_files = list(dfs.keys()); n_dfs = len(dfs)
    checkcompare = True
    for df1, df2 in combinations(range(n_dfs), 2):
        check_equal = (dfs[dfs_files[df1]] == dfs[dfs_files[df2]])
        has_false = False in check_equal.values
        if has_false:
            checkcompare = False
            print('  Ops! Dataframe',dfs_files[df1],'and',dfs_files[df2],'has element that differ!')
    
    print_summary(attribute_files, non_attribute_files, unknown_format)
    if checkcompare:
        print("\nAll processed dataframes is equal! Yey!")
    else:
        print("  Watch out! There is dataframes that are inequal")
    print("Number of files checked:",len(dfs_files))


if __name__ == "__main__":
    main()
