from utils.word import Word
import pandas as pd
import numpy as np

def main():
    DATADIR = 'data'
    DOCX_FILENAME = 'QA.docx'
    wordparser = Word(DATADIR, DOCX_FILENAME)
    paragraphs, paragraphs_bold = wordparser.parse_paragraphs_split_bold(splitbold=True)

    questions = np.array(paragraphs_bold, dtype=object)
    answers = np.array(paragraphs, dtype=object)
    data = np.empty((len(questions), 2), dtype=object)
    data[:,0] = questions
    data[:,1] = answers
    qadf = pd.DataFrame(data, columns=['Q','A'])
    print(qadf.tail())

if __name__=="__main__":
    main()
