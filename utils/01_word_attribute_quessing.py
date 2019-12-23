import os, re
import pandas as pd
import numpy as np
from itertools import combinations
from word_api import Word

DATADIR = os.path.join(os.pardir,'data')
WORDDATADIR = os.path.join(DATADIR,'formatted_word_data')

# Source files
WORDFILES = os.listdir(WORDDATADIR)
print(WORDFILES)
wordcontents = []
wordattributes = {}
for WORDFILE in WORDFILES:
    WORDFILEPATH = os.path.join(WORDDATADIR,WORDFILE)
    WORDDOCUMENT = Word(WORDDATADIR, WORDFILE)
    WORDCONTENT, ATTRIBUTES_DICT = WORDDOCUMENT.extract_paragraphs_content_with_attributes()
    wordcontents.append(WORDCONTENT)
    wordattributes[WORDFILE] = ATTRIBUTES_DICT

BOLD = r"{bval:"
ITALIC = r"{ival:"
COLOR = r"{nondefaultcolor:"
ATTRIBUTES = [BOLD, ITALIC, COLOR]
WHITESPACE = r'\s'
NON_WHITEPACE = r'\S'


def modify_sequence(sentence_onlist, sentence_offlist, paravote, globalvote, count):
    paravote = paravote/count
    globalvote = globalvote/(count*(1/2))

    def qapair_df(L1, L2):
        Q = pd.DataFrame(L1, columns=['Q'])
        A = pd.Series(L2, name='A')
        return Q.join(A)

    def check_vote(vote):
        if abs(vote) != 1:
            print("QA pair is not comming in same order ...")
        if vote < 0:
            return [qapair_df(sentence_onlist, sentence_offlist)]
        elif vote > 0:
            return [qapair_df(sentence_offlist, sentence_onlist)]
        else:
            return None
    
    if len(sentence_onlist) == len(sentence_offlist):
        qadf = check_vote(paravote)
        if None == qadf:
            qadf = check_vote(globalvote)
        if qadf == None:
            print("Could not determine what's the question and what's the answer by vote")
            assert 1 == 0
        else:
            return qadf[0]
    else:
        print("Length of sequences dont match.")
        assert 1 == 0


def parse_paragraph_separator(paragraph, attron, attroff):
    """Searching and extracting information from a single paragraph
    
    Tags information:
        <p><\\p>       - Paragraph tag
        <t><\\t>       - Text snippet tag with attributes
        {attr:val}    - Text attribute name and its value
        <text><\\text> - Actual text inside the text snippet tag

    Arguments:
        paragraph {[str]} -- Paragraph content with tagged atributes information
        attron {str} -- attribute on matching string
        attroff {str} -- attribute off matching string
    
    Returns:
        {str}, {str}, {int} -- Text with attribute on and off, and an int symbolizing 
        which one is used first (either -1 or 1)
    """
    texts = re.findall(r'(?<=<t>).*?(?=<\\t>)', paragraph)
    attrontext, attrofftext = [], []
    onoroff_first = 0
    def search_thistext(attr, text, onoroff_first):
        if re.search(attr, text):
            thistext = re.search(r"(?<=<text>).*?(?=<\\text>)", text).group()
            if attr == attron:
                attrontext.append(thistext)
                if not onoroff_first:
                    onoroff_first = -1
            else:
                attrofftext.append(thistext)
                if not onoroff_first:
                    onoroff_first = 1
        return onoroff_first

    for text in texts:
        onoroff_first = search_thistext(attron, text, onoroff_first)
        onoroff_first = search_thistext(attroff, text, onoroff_first)
    return attrontext, attrofftext, onoroff_first


def attribute_on_off_separation(testattr, WORDCONTENT):
    """Separation of QA by attribute.
    
    Tags information:
        <p><\p>       - Paragraph tag
        <t><\t>       - Text snippet tag with attributes
        {attr:val}    - Text attribute name and its value
        <text><\text> - Actual text inside the text snippet tag

    Arguments:
        testattr {str} -- Pattern to match a specific booleanian attribute
        WORDCONTENT {str} -- extracted Word document information containing content and
                             attributes in a nested tagged structure
    
    Returns:
        [pd.DataFrame] -- DataFrame with questions and answers column
    """
    paragraphs = re.findall(r'(?<=<p>).*?(?=<\\p>)', WORDCONTENT)
    sentence_onlist, sentence_offlist = [], []
    attron =  testattr+"1}"
    attroff = testattr+"0}"
    paravote, globalvote, count  = 0, 0, 0
    firstalternate = 1
    for paragraph in paragraphs:
        attrontext, attrofftext, onoroff_first = parse_paragraph_separator(paragraph,attron,attroff)
        if onoroff_first:
            count+=1
            paravote+=onoroff_first
            if firstalternate:
                globalvote+=onoroff_first
                firstalternate = 0
            else:
                firstalternate = 1
        
        joinattrontext = ''.join(attrontext).strip()
        joinattrofftext = ''.join(attrofftext).strip()
        if joinattrontext:
            sentence_onlist.append(joinattrontext)
        if joinattrofftext:
            sentence_offlist.append(joinattrofftext)
        
        absdifflen = abs(len(sentence_onlist) - len(sentence_offlist))
        if absdifflen > 2:
            print("Sequences dont match up, trying a diffrent attribute ...")
            assert 1 == 0

    return modify_sequence(sentence_onlist, sentence_offlist, paravote, globalvote, count)


def main():
    dfs = []
    for wordfile, wordcontent in zip(WORDFILES, wordcontents):
        print("*************************","\nTrying:",wordfile,"...")
        check = 0
        for testattr in ATTRIBUTES:
            try:
                qadf = attribute_on_off_separation(testattr, wordcontent)
                dfs.append(qadf)
                check = 1
                break
            except AssertionError:
                pass

        if check:
            print(wordfile, "QA was successfully loaded\n")
        else:
            print("!!!!Attribute separation did not sucess!!!!")
            print("QA by " + wordfile + " may not be formatted by attribute, check other options ...\n")
    
    n_dfs = len(dfs)
    for df1, df2 in combinations(range(n_dfs), 2):
        check_equal = (dfs[df1] == dfs[df2])
        has_false = False in check_equal.values
        if not has_false:
            print('Dataframe',df1,'and',df2,'has no element that differ')
        else:
            print('  Ops! Dataframe',df1,'and',df2,'has element that differ!')


if __name__ == "__main__":
    main()
