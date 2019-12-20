import os, re
from itertools import combinations
import pandas as pd

DATA_DIR = 'data'
ENCODED_DOCUMENTS_DIR = 'encoded_text_data'
ENCODED_DOCUMENTS_PATH = os.path.join(os.pardir, DATA_DIR, ENCODED_DOCUMENTS_DIR)
#encoded_files = os.listdir(ENCODED_DOCUMENTS_PATH)

encoded_files = ['qa_unformatted-iso8859_1-latin_1.txt',\
                 'qa_unformatted-iso8859_3.txt', \
                 'qa_unformatted-iso8859_10.txt',\
                 'qa_unformatted-iso8859_15.txt', \
                 'qa_unformatted-cp1252.txt', \
                 'qa_unformatted-mbcs.txt',\
                 'qa_unformatted-utf_8.txt']

print(encoded_files)
encodings = ['latin_1','iso8859_3','iso8859_10','iso8859_15','cp1252','cp1252','utf_8']

def checklength(object, n):
    if len(object)==n:
        print('Hurray! Number of rows just as expected.')
    else:
        print('Nope')

def clean_qalistfile(filename, encoding):
    with open(filename, mode='rt', encoding=encoding) as f:
        file_lines = f.readlines()
        checklength(file_lines, 315)

        splitqa, dump = [], []
        for line in file_lines:
            line = line.split('\n')[0]
            
            if not line[-1:] == '.' and len(line) == 2:
                line+='.' # Add missing last punctuation
            line+=';' # and then a semicolon marker
            
            regsplit = re.findall(r".*\?|\S.*?\.|\S.*?\;|\ .*?\;", line) # Split by pattern
            if len(regsplit) == 2:
                regsplit[1] = regsplit[1][:-1] # Remove semicolon marker
                if regsplit[1][0] == ' ':
                    regsplit[1] = regsplit[1][1:] # Remove beginning whitespace
                splitqa.append(regsplit)
            else:
                dump.append(line)
        
        if len(dump) == 0:
            print('Hurray No lines in dump list.')
        else:
            print('Nope')
            print(dump)

        qadf = pd.DataFrame(splitqa, columns=['Q','A'])
        return qadf

def main():
    dfs = []
    for filename, encoding in zip(encoded_files,encodings):
        filename = os.path.join(ENCODED_DOCUMENTS_PATH,filename)
        qadf = clean_qalistfile(filename, encoding)
        dfs.append(qadf)
    
    n_dfs = len(dfs)
    print(n_dfs)
    
    for df1, df2 in combinations(range(n_dfs), 2):
        check_equal = (dfs[df1] == dfs[df2])
        check_false = False in check_equal.values
        if not check_false:
            print('Dataframe',df1,'and',df2,'has no element that differ, corresponds to:')
            print(encoded_files[df1],'and',encoded_files[df2],'\n')
        else:
            #print('Dataframe', df1, 'and', df2, 'has at least one element that differ')
            pass
    
    print(dfs[3])

if __name__=='__main__':
    main()
