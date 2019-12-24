import os, re
import pandas as pd
import numpy as np
from itertools import combinations
from utils.wapi import Word

DATADIR = os.path.join(os.pardir,'data')
WORDDATADIR = os.path.join(DATADIR,'formatted_word_data')
ATTRIBUTES = ['bval','ival','noproof',
             'color','nondefaultcolor','size',
             'lang','ascifont','ansifont']

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

for wordfile in WORDFILES:
    attributes = wordattributes[wordfile]

    bval = np.array(attributes["bval"])
    ival = np.array(attributes["ival"])
    noproof = np.array(attributes["noproof"])
    nondefaultcolor = np.array(attributes["nondefaultcolor"])

    attribute_matrix = np.array([bval, ival, noproof, nondefaultcolor], dtype=int)
    squareattribute = np.dot(attribute_matrix,attribute_matrix.transpose())
    print(wordfile)
    print(squareattribute)