import os

def main():
    DATA_DIR = 'data'
    ENCODED_DOCUMENTS_DIR = 'diffrent_encoded_text_data'
    ENCODED_DOCUMENTS_PATH = os.path.join('..',DATA_DIR, ENCODED_DOCUMENTS_DIR)

    encoded_files = os.listdir(ENCODED_DOCUMENTS_PATH)
    encodings = ['utf_8','cp1252','iso8859_3','iso8859_15','iso8859_10','latin_1']

    for filename in encoded_files:
        filepath = os.path.join(ENCODED_DOCUMENTS_PATH, filename)
        for encoding in encodings:
            try:
                f = open(filepath, 'r', encoding=encoding)
                f.read()
                f.close()
                print(filename,'was okey using',encoding,'encoding')
                break
            except:
                print('          .')
                print(filename,'did not work using',encoding,'encoding!')
                print('          .')

if __name__ == '__main__':
    main()