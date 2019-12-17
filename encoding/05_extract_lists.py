import os, re
import pandas as pd

DATA_DIR = 'data'
ENCODED_DOCUMENTS_DIR = 'diffrent_encoded_text_data'
ENCODED_DOCUMENTS_PATH = os.path.join('..',DATA_DIR, ENCODED_DOCUMENTS_DIR)
encoded_files = os.listdir(ENCODED_DOCUMENTS_PATH)
encodings = ['iso8859_15','latin_1','cp1252','cp1252','utf_8','iso8859_3','iso8859_10']

def checklength(object, n):
    if len(object)==n:
        print('Hurray')
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
            print('Hurray')
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
        print('')
        print(encoding)
        print(qadf.tail(50))

if __name__=='__main__':
    main()