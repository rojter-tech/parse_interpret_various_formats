from docx import Document

f = open('data/Word_Questions.docx', 'rb')
document = Document(f)
f.close()

fullText = []
for p in document.paragraphs:
    print(p.text)
