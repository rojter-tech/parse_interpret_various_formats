import os

def main():
    DATA_DIR = 'data'
    ENCODED_DOCUMENTS_DIR = 'encoded_text_data'
    ENCODED_DOCUMENTS_PATH = os.path.join(os.pardir, DATA_DIR, ENCODED_DOCUMENTS_DIR)

    encoded_files = os.listdir(ENCODED_DOCUMENTS_PATH)
    encodings = ['utf_8','cp1252','iso8859_3','iso8859_15','iso8859_10','latin_1']

    for filename in encoded_files:
        print('-------')
        filepath = os.path.join(ENCODED_DOCUMENTS_PATH, filename)
        for encoding in encodings:
            try:
                with open(filepath, 'rt', encoding=encoding) as f:
                    f.read()
                print(filename,'was read using',encoding,'encoding')
            except:
                print('•',filename,'did not read using',encoding,'encoding!','•')

if __name__ == '__main__':
    main()