import os, zipfile, re
import xml.dom.minidom as minidom
def main():
    print("Word Document Parser")
    DATADIR = 'data'
    DOCX_FILENAME = 'QA.docx'
    FILEPATH = os.path.join(DATADIR, DOCX_FILENAME)
    docx_file = zipfile.ZipFile(FILEPATH)

    documentname = ""
    for name in docx_file.namelist():
        if re.match(r".*document.*", str(name)):
            documentname=name
            break

    wordXml = minidom.parseString(docx_file.read(documentname)).toprettyxml(indent='   ')

    print(wordXml)

if __name__=="__main__":
    main()