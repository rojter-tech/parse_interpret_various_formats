import pandas as pd
import re
from utils.errors import Error, rOjterError

def modified_sequence(sentence_onlist, sentence_offlist, paravote, globalvote, count):
    """On basis of some hyperparameters the final dataframe 
       will be created in a particular order
    
    Arguments:
        sentence_onlist {[str]} -- Texts with the specific attribute state 1
        sentence_offlist {[str]} -- Texts with the specific attribute state 0
        paravote {int} -- Internal voting hyperparameter indicating which state
                             that was used first in the parameter sequence
        globalvote {int} -- Global voting hyperparameter indicating wich state
                               that was used first between parameter sequences
        count {[type]} -- Total number of block seqences of texts
    
    Returns:
        [pd.DataFrame] -- DataFrame with QA separated columns
    """
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
            return qapair_df(sentence_onlist, sentence_offlist)
        elif vote > 0:
            return qapair_df(sentence_offlist, sentence_onlist)
        else:
            return ""
    
    # Systematic check if and in what order DataFrames should be initialized
    if len(sentence_onlist) == len(sentence_offlist):
        qadf = check_vote(paravote)
        if type(qadf) == str:
            qadf = check_vote(globalvote)
        if type(qadf) == str:
            print("Could not determine what's the question and what's the answer by vote")
            raise rOjterError
        else:
            return qadf
    else:
        print("Length of sequences dont match.")
        raise rOjterError


def paragraph_attribute_separator(paragraph, attron, attroff):
    """Searching and highlighting boolean attributed content from a single paragraph
    
    Tags information:
        <p><\\p>       - Paragraph tag
        <t><\\t>       - Texts snippets tag with attributes
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

    def search_thistext(text, onoroff_first):
        """Appending text with diffrent attribute state in separate lists
        
        Arguments:
            text {str} -- Outer text string with attributes
            onoroff_first {int} -- keeps track of which attribute state was 
                                   detected before the other sequentially
        
        Returns:
            [type] -- [description]
        """
        thistext = re.search(r"(?<=<text>).*?(?=<\\text>)", text).group()
        if re.search(attron, text):
            attrontext.append(thistext)
            if not onoroff_first:
                onoroff_first = -1
        else:
            attrofftext.append(thistext)
            if not onoroff_first:
                onoroff_first = 1

        return onoroff_first

    for text in texts:
        onoroff_first = search_thistext(text, onoroff_first)

    return attrontext, attrofftext, onoroff_first


def attribute_on_off_separation(testattr, content):
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
    paragraphs = re.findall(r'(?<=<p>).*?(?=<\\p>)', content)
    sentence_onlist, sentence_offlist = [], []
    attron =  testattr+"1}"
    attroff = testattr+"0}"
    paravote, globalvote, count  = 0, 0, 0
    firstalternate = 1
    for paragraph in paragraphs:
        attrontext, attrofftext, onoroff_first = paragraph_attribute_separator(paragraph,attron,attroff)
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
            raise rOjterError

    return modified_sequence(sentence_onlist, sentence_offlist, paravote, globalvote, count)


def try_separate_by_attribute(wordobject):
    """Trying separation of Word-document QA content that can be distinguished by attribute.
    
    Arguments:
        wordobject {Word} -- Word object
    
    Returns:
        Pandas.DataFrame -- [description]
    """
    BOLD = r"{bval:"
    ITALIC = r"{ival:"
    COLOR = r"{nondefaultcolor:"
    ATTRIBUTES = [BOLD, ITALIC, COLOR]
    print(60*"*","\nTrying:",wordobject.filename,"...")
    check = False
    for testattr in ATTRIBUTES:
        try:
            qadf = attribute_on_off_separation(testattr, wordobject.content)
            print(wordobject.filename, "QA was successfully loaded")
            check = True
            break
        except rOjterError:
            print("This bullshit attribute is shit ..")
            pass
    
    if check:
        return qadf
    else:
        print("")
        print("***********************************************")
        print("**!!!!Attribute separation did not sucess!!!!**")
        print("***********************************************")
        print("")
        print("QA by " + wordobject.filename + " maybe were not formatted by attribute, check other options ...")
        return wordobject.filename