import os
from utils.format_detection_tools import load_qa_df

# Source file
DATADIR = os.path.join(os.pardir,'data')
WORDDATADIR = os.path.join(DATADIR,'formatted_word_data')
wordfile = 'QA.docx'

def main():
    wordfilepath = os.path.join(WORDDATADIR,wordfile)
    qadf = load_qa_df(wordfilepath)
    print(qadf)

if __name__ == "__main__":
    main()
