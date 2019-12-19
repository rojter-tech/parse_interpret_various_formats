import os, re
from zipfile import ZipFile
from xml.dom.minidom import parseString

DATADIR = os.path.join(os.pardir, 'data', 'word_data')
FILENAME = 'Word_Questions'
EXTENSION = '.docx'
FILEPATH = os.path.join(DATADIR, FILENAME + EXTENSION)

def find_docname_string(docx_file, documentname=None):
    for name in docx_file.namelist():
        if re.match(r".*document.*xml", str(name)):
            documentname=name
            break
    return documentname

def main():
    print("Word Document Parsing\n")
    docx_file = ZipFile(FILEPATH)
    documentname = find_docname_string(docx_file)
    wordXml = parseString(docx_file.read(documentname)).toprettyxml(indent='   ')

    print(wordXml)

if __name__=="__main__":
    main()