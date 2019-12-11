from utils.word import Word

def main():
    DATADIR = 'data'
    DOCX_FILENAME1 = 'Word_Questions1.docx'
    DOCX_FILENAME2 = 'Word_Questions2.docx'
    wordparser1 = Word(DATADIR, DOCX_FILENAME1)
    wordparser2 = Word(DATADIR, DOCX_FILENAME2)
    paragraphs1, paragraphs_bold1 = wordparser1.parse_paragraphs_split_bold(splitbold=True)
    paragraphs2, paragraphs_bold2 = wordparser2.parse_paragraphs_split_bold(splitbold=True)

    print(wordparser1)

    print('\n'.join(paragraphs_bold1))
    print('\n'.join(paragraphs1))

    print('\n'.join(paragraphs_bold2))
    print('\n'.join(paragraphs2))

if __name__=="__main__":
    main()