import os
from utils.format_detection_tools import load_qa_df, load_word_object

# Source file
DATADIR = os.path.join(os.pardir,'data')
WORDDATADIR = os.path.join(DATADIR,'formatted_word_data')
wordfile = 'QATable.docx'

def main():
    wordfilepath = os.path.join(WORDDATADIR,wordfile)
    #qadf = load_qa_df(wordfilepath)
    #print(qadf)
    wordobject = load_word_object(wordfilepath)
    print(wordobject.raw_text)
    #wordobject.save_as_xml("kundfaq_test1.xml")


if __name__ == "__main__":
    main()
