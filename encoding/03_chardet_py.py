import os, re
from chardet.universaldetector import UniversalDetector

def main():
    DATA_DIR = 'data'
    ENCODED_DOCUMENTS_DIR = 'encoded_text_data'
    ENCODED_DOCUMENTS_PATH = os.path.join(os.pardir, DATA_DIR, ENCODED_DOCUMENTS_DIR)
    encoded_files = os.listdir(ENCODED_DOCUMENTS_PATH)

    detector = UniversalDetector()
    for filename in encoded_files:
        if re.match(r'.*txt',filename):
            filepath = os.path.join(ENCODED_DOCUMENTS_PATH, filename)
            print(filepath.ljust(60))
            detector.reset()
            for line in open(filepath, 'rb'):
                detector.feed(line)
                if detector.done: break
            detector.close()
            print(detector.result)

if __name__=='__main__':
    main()