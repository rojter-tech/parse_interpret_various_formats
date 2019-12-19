import os
DATA_DIR = 'data'
ENCODED_DOCUMENTS_DIR = 'encoded_text_data'
ENCODED_DOCUMENTS_PATH = os.path.join(os.pardir, DATA_DIR, ENCODED_DOCUMENTS_DIR)
ENCODINGS = ['utf_8','cp1252','iso8859_3','iso8859_15','iso8859_10','latin_1']

def main():
    
    filename = 'qa_unformatted-utf_8.txt'
    filepath = os.path.join(ENCODED_DOCUMENTS_PATH, filename)
    working_encoding = []
    nonworking_encoding = []
    snippets = []

    for encoding in ENCODINGS:
        try:
            f = open(filepath, 'r', encoding=encoding)
            snippets.append(f.read().split('\n')[-1])
            f.close()
            
            print(filename,'was okey using',encoding,'encoding')
            working_encoding.append(encoding)

        except:
            print('  ', filename, 'did not work using', encoding, 'encoding!')
            nonworking_encoding.append(encoding)
    
    print('working encodings:',working_encoding)
    print('non working encodings:',nonworking_encoding)
    print(len(snippets))
    for i in range(len(snippets)):
        print(str(i)+':',snippets[i])

if __name__ == '__main__':
    main()
