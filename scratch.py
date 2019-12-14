import os
DATA_DIR = 'data'
ENCODED_DOCUMENTS_DIR = 'diffrent_encoded_text_data'
ENCODED_DOCUMENTS_PATH = os.path.join(DATA_DIR, ENCODED_DOCUMENTS_DIR)

encoded_files = os.listdir(ENCODED_DOCUMENTS_PATH)
encodings = ['latin_1','iso8859_3','iso8859_10','iso8859_15','cp1252']

for file in encoded_files:
    filepath = os.path.join(ENCODED_DOCUMENTS_PATH, file)
    try:
        f = open(filepath, 'r', encoding='latin_1')
        f.read()
        f.close()
        print(file,'was okey')
    except:
        print(file,'did not work')
    