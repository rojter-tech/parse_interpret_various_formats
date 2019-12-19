"""Extracting some html data and saving as ; separated csv and gzip compressed pickle"""
import os, re, json
from numpy import array, savetxt
import pandas as pd

DATADIR = os.path.join(os.pardir,'data')
HTMLDATADIR = os.path.join(DATADIR,'html_data')

# Source file
HTMLFILE = 'trivial.html'; HTMLFILEPATH = os.path.join(HTMLDATADIR,HTMLFILE)

# Varous file format, representaion files
CSVFILE = 'qa.csv';     CSVSAVEPATH = os.path.join(DATADIR,CSVFILE)
PICKLEFILE = 'qa.gzip'; PICKLESAVEPATH = os.path.join(DATADIR,PICKLEFILE)
JSONFILE = 'qa.json';   JSONFILESAVEPATH = os.path.join(DATADIR, JSONFILE)

def parse_json(qadf):
    qa_dict = {}
    for q, a in zip(qadf.iloc[:,0], qadf.iloc[:,1]):
        # Add ending dot if not present
        if not a[-1] == '.':
            a+='.'
        qa_dict[q] = a
    json_dict = json.dumps(qa_dict, ensure_ascii=False, indent=4)
    return json_dict

def save_df_as_various_fileformats(qadf):
    # Semicolon separated CSV
    savetxt(CSVSAVEPATH, array(qadf, dtype=object), 
        header='Q;A', delimiter=';', fmt="%s", comments='')
    # GZip compressed pickle
    qadf.to_pickle(PICKLESAVEPATH, compression="gzip", protocol=4)
    # Indented readable JSON
    with open(JSONFILESAVEPATH, 'wt', encoding="utf_8") as f:
        f.write(parse_json(qadf))

def main():
    qalist = []
    with open(HTMLFILEPATH) as htmlfile:
        for line in htmlfile:
            questiontag = re.findall(r'<h3.*?>.*?</h3>', line)
            if questiontag:
                question = re.findall(r'(?<=>).*(?=<span)', questiontag[0])
                answer = re.findall(r'(?<=<p>).*?(?=</p>)', line)
                if answer:
                    question=str(question[0])
                    answer=str(answer[0])
                    if not answer[-1] == '.':
                        answer+='.'
                    qalist.append([question,answer])
                else:
                    print(question[0],' : ' , 'has multiple answers!')
    
    qadf = pd.DataFrame(qalist, columns=['Q','A'])
    # Make sure that any semicolon is not present in the data
    qadf.replace(';', ':', inplace=True, regex=True)
    qadf.replace(r'Answer:.*?(?=\S)', '', inplace=True, regex=True)

    save_df_as_various_fileformats(qadf)

if __name__ == "__main__":
    main()