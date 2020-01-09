from utils.attrib_formats import try_separate_by_attribute
from utils.raw_formats import try_separate_by_rawtext, format_functions
from itertools import combinations

def process_wordobject(wordobject, format_type = None):
    print("Processing", wordobject.filename)
    qadata = try_separate_by_attribute(wordobject)

    if type(qadata) == str:
        qadata = try_separate_by_rawtext(wordobject, format_functions)
    else:
        format_type = "Attribute"
        return qadata, format_type

    if type(qadata) == str:
        print("No separation process attempt did succeeded for",qadata)
        format_type = "UnknownFormat"
        return qadata, format_type
    else:
        format_type = "RawTextFormat"
        return qadata, format_type

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

def multiple_object_diagnostics(wordobjects):
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
