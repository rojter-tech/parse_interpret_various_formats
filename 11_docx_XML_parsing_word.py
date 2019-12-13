from utils.word import Word
import pandas as pd
import numpy as np

def main():
    DATADIR = 'data'
    FILENAME = 'Word_Questions'
    #FILENAME = 'Word_Questions2'
    #FILENAME = 'QA'
    EXTENSION = '.docx'
    wordparser = Word(DATADIR, FILENAME + EXTENSION)
    paragraphs, paragraphs_bold = wordparser.parse_paragraphs_split_bold(splitbold=True)

    n_min = np.min([len(paragraphs),len(paragraphs_bold)])
    
    questions = np.array(paragraphs_bold, dtype=object)
    answers = np.array(paragraphs, dtype=object)
    data = np.empty((n_min, 2), dtype=object)
    data[:,0] = questions[:n_min]
    data[:,1] = answers[:n_min]
    qadf = pd.DataFrame(data, columns=['Q','A'])
    print(qadf)

if __name__=="__main__":
    main()
