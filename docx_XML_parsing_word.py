from utils.word import Word

def main():
    DATADIR = 'data'
    DOCX_FILENAME = 'QA.docx'
    wordparser = Word(DATADIR, DOCX_FILENAME)
    paragraphs, paragraphs_bold = wordparser.parse_paragraphs_split_bold(splitbold=True)

    #print(wordparser)

    print('\n'.join(paragraphs_bold))
    print('\n'.join(paragraphs))

if __name__=="__main__":
    main()