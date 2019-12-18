import os, zipfile, re
from xml.dom.minidom import parseString

DATADIR = os.path.join('..','data','word_data')
FILENAME = 'QA'
EXTENSION = '.docx'
FILEPATH = os.path.join(DATADIR, FILENAME + EXTENSION)

def main():
    print("Word Document Parser")
    docx_file = zipfile.ZipFile(FILEPATH)
    documentname = ""
    for name in docx_file.namelist():
        if re.match(r".*document.*xml", str(name)):
            documentname=name
            break

    wordXml = parseString(docx_file.read(documentname)).toprettyxml(indent='   ')

    print(wordXml)

if __name__=="__main__":
    main()