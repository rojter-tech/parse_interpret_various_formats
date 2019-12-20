import os, re
import pandas as pd
from word_api import Word
WHITESPACE = r'\s'
NON_WHITEPACE = r'\S'

DATADIR = os.path.join(os.pardir,'data')
WORDDATADIR = os.path.join(DATADIR,'word_data')

# Source file
WORDFILE = 'QA.docx'
WORDFILEPATH = os.path.join(WORDDATADIR,WORDFILE)

BOLD = r"{bval:"
ITALIC = r"{ival:"
NOPROOF = r"{noproof:"

testattr = BOLD


worddocument = Word(WORDDATADIR, WORDFILE)
wordcontent = worddocument.parse_paragraphs_texts()
paragraphs = re.findall(r'(?<=<p>).*?(?=<\\p>)', wordcontent)
sentence_list, sentence_antilist = [], []
reg = testattr+"1}"
ant = testattr+"0}"
for paragraph in paragraphs:
    texts = re.findall(r'(?<=<t>).*?(?=<\\t>)', paragraph)
    regtext, antitext = [], []
    for text in texts:
        # Search text
        if re.search(reg, text):
            thistext = re.search(r'(?<={text:).*?(?=})', text).group()
            regtext.append(thistext)
        # Search anti version of text
        if re.search(ant, text):
            thistext = re.search(r'(?<={text:).*?(?=})', text).group()
            antitext.append(thistext)
    
    jointext = ''.join(regtext).strip()
    joinantitext = ''.join(antitext).strip()
    if jointext:
        sentence_list.append(jointext)
    if joinantitext:
        sentence_antilist.append(joinantitext)

Q = pd.DataFrame(sentence_list, columns=['Q'])
A = pd.Series(sentence_antilist, name='A')

print(Q.join(A))

