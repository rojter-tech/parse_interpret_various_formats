from utils.word import Word
import pandas as pd
import numpy as np
import xml.dom.minidom as minidom
import os

def get_word_data(wordparser):
    paragraphs, paragraphs_bold = wordparser.parse_paragraphs_split_bold(splitbold=True)
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

    xml_source1 = minidom.parseString(worddocument1.xml_content).toprettyxml(indent='   ')
    to_file = open(os.path.join(DATADIR,"Word_Questions.xml"), "w")
    to_file.write(xml_source1)

    qadf1 = get_word_data(worddocument1)
    qadf2 = get_word_data(worddocument2)

    print('Number of rows:',len(qadf1))
    print(qadf1.head(20))

    print('Number of rows:',len(qadf2))
    print(qadf2.head(20))

    for row in range(len(qadf1)):
        equal = qadf1.iloc[row,0] == qadf2.iloc[row,0]
        if not equal:
            print('|',qadf1.iloc[row,0],'|', qadf2.iloc[row,0],'|')

if __name__=="__main__":
    main()
