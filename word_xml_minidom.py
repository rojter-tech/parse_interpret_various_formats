import os
import zipfile
import re
import xml.dom.minidom
print("Word Document Parser")
docx_file = zipfile.ZipFile('data/Word_Questions.docx')

documentname = ""
for name in docx_file.namelist():
    if re.match(r".*document.*", str(name)):
        documentname=name
        break

wordXml = xml.dom.minidom.parseString(docx_file.read(documentname)).toprettyxml(indent='   ')
#wordXml = xml.dom.minidom.parseString(docx_file.read(documentname)).toxml()
#docx_file.read(documentname)

print(wordXml)