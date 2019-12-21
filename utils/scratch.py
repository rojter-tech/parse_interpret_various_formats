import os, re
import pandas as pd
import numpy as np
from word_api import Word
WHITESPACE = r'\s'
NON_WHITEPACE = r'\S'

DATADIR = os.path.join(os.pardir,'data')
WORDDATADIR = os.path.join(DATADIR,'formatted_word_data')

# Source file
WORDFILE = 'QAi.docx'
WORDFILEPATH = os.path.join(WORDDATADIR,WORDFILE)

BOLD = r"{bval:"
ITALIC = r"{ival:"

ATTRIBUTES = [BOLD, ITALIC]

def attribute_on_off_separation(testattr):
    worddocument = Word(WORDDATADIR, WORDFILE)
    wordcontent = worddocument.parse_paragraphs_texts()
    paragraphs = re.findall(r'(?<=<p>).*?(?=<\\p>)', wordcontent)
    sentence_onlist, sentence_offlist = [], []
    attron =  testattr+"1}"
    attroff = testattr+"0}"
    vote, count = 0, 0

    for paragraph in paragraphs:
        texts = re.findall(r'(?<=<t>).*?(?=<\\t>)', paragraph)
        attrontext, attrofftext = [], []
        leftorright = 0
        for text in texts:
            # Search text with attribute on
            if re.search(attron, text):
                thistext = re.search(r'(?<={text:).*?(?=})', text).group()
                attrontext.append(thistext)
                if not leftorright:
                    leftorright = -1
            # Search text with attribute off
            if re.search(attroff, text):
                thistext = re.search(r'(?<={text:).*?(?=})', text).group()
                attrofftext.append(thistext)
                if not leftorright:
                    leftorright = 1
        if leftorright:
            count+=1
            vote+=leftorright
        
        joinattrontext = ''.join(attrontext).strip()
        joinattrofftext = ''.join(attrofftext).strip()
        if joinattrontext:
            sentence_onlist.append(joinattrontext)
        if joinattrofftext:
            sentence_offlist.append(joinattrofftext)
        
        absdifflen = abs(len(sentence_onlist) - len(sentence_offlist))
        if absdifflen > 2:
            print("Sequences dont match up, trying a diffrent attribute.")
            assert 1 == 0

    #print(sentence_list)
    #print(sentence_antilist)
    
    vote = vote/count
    if len(sentence_onlist) == len(sentence_offlist):
        if vote < 0:
            Q = pd.DataFrame(sentence_onlist, columns=['Q'])
            A = pd.Series(sentence_offlist, name='A')
        elif vote > 0:
            Q = pd.DataFrame(sentence_offlist, columns=['Q'])
            A = pd.Series(sentence_onlist, name='A')
        else:
            print("Could not determine what's the question and what's the answer")
        print(Q.join(A))
    else:
        print("Length of sequences dont match.")
        assert 1 == 0

for testattr in ATTRIBUTES:
    try:
        attribute_on_off_separation(testattr)
    except AssertionError:
        pass
