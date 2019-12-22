import os, re
import pandas as pd
import numpy as np
from word_api import Word

DATADIR = os.path.join(os.pardir,'data')
WORDDATADIR = os.path.join(DATADIR,'formatted_word_data')

# Source files
WORDFILES = os.listdir(WORDDATADIR)
wordcontents = []
for WORDFILE in WORDFILES:
    WORDFILEPATH = os.path.join(WORDDATADIR,WORDFILE)
    WORDDOCUMENT = Word(WORDDATADIR, WORDFILE)
    WORDCONTENT = WORDDOCUMENT.parse_paragraphs_texts()
    wordcontents.append(WORDCONTENT)

BOLD = r"{bval:"
ITALIC = r"{ival:"
COLOR = r"{defaultcolor:"
ATTRIBUTES = [BOLD, ITALIC, COLOR]
WHITESPACE = r'\s'
NON_WHITEPACE = r'\S'

def modified_sequence(sentence_onlist, sentence_offlist, vote, count):
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
        if abs(vote) != 1:
            print("QA pair is not comming in same order ...\n")
        
        return Q.join(A)
    else:
        print("Length of sequences dont match.")
        assert 1 == 0


def search_paragraph(paragraph,attron,attroff):
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
    return attrontext, attrofftext, leftorright


def attribute_on_off_separation(testattr, WORDCONTENT):
    paragraphs = re.findall(r'(?<=<p>).*?(?=<\\p>)', WORDCONTENT)
    sentence_onlist, sentence_offlist = [], []
    attron =  testattr+"1}"
    attroff = testattr+"0}"
    vote, count = 0, 0

    for paragraph in paragraphs:
        attrontext, attrofftext, leftorright = search_paragraph(paragraph,attron,attroff)
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
            print("Sequences dont match up, trying a diffrent attribute ...\n")
            assert 1 == 0
    
    return modified_sequence(sentence_onlist, sentence_offlist, vote, count)


def main():
    check = 0
    for wordcontent in wordcontents:
        for testattr in ATTRIBUTES:
            try:
                qadf = attribute_on_off_separation(testattr, wordcontent)
                print(qadf)
                check = 1
                break
            except AssertionError:
                pass

        if check:
            print("\nQA was successfully loaded")
        else:
            print("\nQA may not be formatted by attribute, check other options ...")

if __name__ == "__main__":
    main()