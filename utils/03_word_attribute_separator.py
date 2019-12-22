import os, re
import pandas as pd
import numpy as np
from itertools import combinations
from word_api import Word

DATADIR = os.path.join(os.pardir,'data')
WORDDATADIR = os.path.join(DATADIR,'formatted_word_data')

# Source files
WORDFILES = os.listdir(WORDDATADIR)
wordcontents = []
for WORDFILE in WORDFILES:
    WORDFILEPATH = os.path.join(WORDDATADIR,WORDFILE)
    WORDDOCUMENT = Word(WORDDATADIR, WORDFILE)
    WORDCONTENT = WORDDOCUMENT.extract_paragraphs_content_with_attributes()
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


def parse_paragraph(paragraph,attron,attroff):
    """Searching and extracting information from a single paragraph
    
    Information:
    <p><\p>       - Paragraph tag
    <t><\t>       - Text snippet tag with attributes
    <text><\text> - Actual text inside the text snippet tag

    Arguments:
        paragraph {[str]} -- Paragraph content with tagged atributes information
        attron {str} -- attribute on matching string
        attroff {str} -- attribute off matching string
    
    Returns:
        {str}, {str}, {int} -- Text with attribute on, off and a int symbolizing 
        which one is used first (either -1 or 1)
    """
    texts = re.findall(r'(?<=<t>).*?(?=<\\t>)', paragraph)
    attrontext, attrofftext = [], []
    leftorright = 0
    def extract_thistext(atr, text, leftorright):
        if re.search(atr, text):
            thistext = re.search(r"(?<=<text>).*?(?=<\\text>)", text).group()
            if atr == attron:
                attrontext.append(thistext)
                if not leftorright:
                    leftorright = -1
            else:
                attrofftext.append(thistext)
                if not leftorright:
                    leftorright = 1
        return leftorright

    for text in texts:
        leftorright = extract_thistext(attron, text, leftorright)
        leftorright = extract_thistext(attroff, text, leftorright)
    return attrontext, attrofftext, leftorright


def attribute_on_off_separation(testattr, WORDCONTENT):
    paragraphs = re.findall(r'(?<=<p>).*?(?=<\\p>)', WORDCONTENT)
    sentence_onlist, sentence_offlist = [], []
    attron =  testattr+"1}"
    attroff = testattr+"0}"
    vote, count = 0, 0
    
    for paragraph in paragraphs:
        attrontext, attrofftext, leftorright = parse_paragraph(paragraph,attron,attroff)
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
    dfs = []
    for wordfile, wordcontent in zip(WORDFILES, wordcontents):
        for testattr in ATTRIBUTES:
            try:
                qadf = attribute_on_off_separation(testattr, wordcontent)
                dfs.append(qadf)
                check = 1
                break
            except AssertionError:
                pass

        if check:
            print("\nQA was successfully loaded")
        else:
            print("\nQA by " + wordfile + " may not be formatted by attribute, check other options ...")
    
    n_dfs = len(dfs)
    for df1, df2 in combinations(range(n_dfs), 2):
        check_equal = (dfs[df1] == dfs[df2])
        has_false = False in check_equal.values
        if not has_false:
            print('Dataframe',df1,'and',df2,'has no element that differ')


if __name__ == "__main__":
    main()