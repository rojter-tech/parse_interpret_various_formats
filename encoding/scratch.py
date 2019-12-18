import os

DATA_DIR = 'data'
ENCODED_DOCUMENTS_DIR = 'diffrent_encoded_text_data'
ENCODED_DOCUMENTS_PATH = os.path.join('..',DATA_DIR, ENCODED_DOCUMENTS_DIR)

encoded_file = 'qa_unformatted-mbcs.txt'
filepath = os.path.join(ENCODED_DOCUMENTS_PATH,encoded_file)

with open(filepath, mode='rt', encoding='cp1252') as f:
    a = f.readline()
    print(repr(a))

print("Test string ...", end='\r\n')
print("Test string2 ...\r\n", end='\r\n')

print(repr("Test string2 ...\r\n"))