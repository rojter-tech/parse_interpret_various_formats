from utils.word import Word
import pandas as pd
import numpy as np
from xml.dom.minidom import parseString
import os

def get_word_data(worddocument):
    paragraphs, paragraphs_bold = worddocument.parse_paragraphs(splitbold=True,
                                                                clean_trailing_whitespace=True)
    n_min = np.min([len(paragraphs),len(paragraphs_bold)])
    questions = np.array(paragraphs_bold, dtype=object)
    answers = np.array(paragraphs, dtype=object)
    data = np.empty((n_min, 2), dtype=object)
    data[:,0] = questions[:n_min]
    data[:,1] = answers[:n_min]
    qadf = pd.DataFrame(data, columns=['Q','A'])
    return qadf

def main():
    DATADIR = 'data'
    EXTENSION = '.docx'
    FILENAME1 = 'QA'
    FILENAME2 = 'Mixed_Word_QA'
    worddocument1 = Word(DATADIR, FILENAME1 + EXTENSION)
    worddocument2 = Word(DATADIR, FILENAME2 + EXTENSION)

    # Save XML source to file
    xml_source1 = parseString(worddocument1.xml_content).toprettyxml(indent='   ')
    to_file1 = open(os.path.join(DATADIR,"qa.xml"), "w")
    to_file1.write(xml_source1)

    xml_source2 = parseString(worddocument2.xml_content).toprettyxml(indent='   ')
    to_file2 = open(os.path.join(DATADIR,"mixed_word_qa.xml"), "w")
    to_file2.write(xml_source2)

    qadf1 = get_word_data(worddocument1)
    qadf2 = get_word_data(worddocument2)

    for element in worddocument1.docx_file.namelist():
        print(element)
    print('')

    print('Number of rows:',len(qadf1))
    print(qadf1.head())

    print('Number of rows:',len(qadf2))
    print(qadf2.head())

    print('')
    # Check if both file output is equal
    check = True
    for row in range(len(qadf1)):
        equal = qadf1.iloc[row,0] == qadf2.iloc[row,0]
        if not equal:
            check = False
            print('|',qadf1.iloc[row,0],'|', qadf2.iloc[row,0],'|')
    if check:
        print('File outputs are identical!')
    else:
        print('Too bad, file outputs are not identical.')

if __name__=="__main__":
    main()
