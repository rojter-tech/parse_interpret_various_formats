try:
    from xml.etree.cElementTree import XML
except ImportError:
    from xml.etree.ElementTree import XML
from zipfile import ZipFile
from xml.dom.minidom import parseString
import os, re


class Word:
    """
    Parsing word file API.
    """
    # Word namespace tag
    NAMESPACE = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
    # Word paragraph tag
    PARAGRAPH = NAMESPACE + r'p'
    # Word content tag within paragraph
    CONTENT = NAMESPACE + r'r' # ----------------
    #           |                            #    |
    #           v                            #    |
    # Word text attributes tags within content    |
    PAFORMAT = NAMESPACE + r'rPr'            #    |
    BOLD = NAMESPACE + r'b'                  #    |
    ITALIC = NAMESPACE + r'i'                #    |
    NOPROF = NAMESPACE + r'noProof'          #    |
    COLOR = NAMESPACE + r'color'             #    |
    SIZE = NAMESPACE + r'sz'                 #    |
    LANG = NAMESPACE + r'lang'               #    |
    FONTS = NAMESPACE + r'rFonts'            #    |
    # Word text tag within content           #    |
    TEXT = NAMESPACE + r't' # <--------------------
    ##########################################
    ATTRIBUTES = ['bval','ival','noproof',
                'color','nondefaultcolor','size',
                'lang','ascifont','ansifont']


    def __init__(self, datadir, filename):
        self.datadir = datadir
        self.filename = filename
        self.docx_file = ZipFile(os.path.join(datadir, filename))
        
        self.documentname = []
        self.xml_content = []
        self.tree = []

        # Initialize document attribute
        self.find_docname_string()
        self.get_xml_content_tree()
    

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)
    

    def find_docname_string(self):
        documentname = ""
        for name in self.docx_file.namelist():
            if re.match(r".*document.*xml", str(name)):
                documentname=name
                break
        self.documentname = documentname
    

    def get_xml_content_tree(self):
        self.xml_content = self.docx_file.read(self.documentname)
        self.docx_file.close()
        self.tree = XML(self.xml_content)
    

    def show_xml(self):
        print(parseString(self.xml_content).toprettyxml(indent='    '))


    def save_as_xml(self,filepath):
        with open(filepath, mode='wt', encoding='utf_8') as f:
            f.write(parseString(self.xml_content).toprettyxml(indent='    '))


    def extract_paragraphs_content_with_attributes(self):
        """Simple word xml parser, collecting text data with attributes.
        Tags information:
            <p><\p>       - Paragraph tag
            <t><\t>       - Text snippet tag with attributes
            {attr:val}    - Text attribute name and its value
            <text><\text> - Actual text inside the texts snippets tag

        Returns:
            [str] -- Paragraphs texts with tagged attributes
        """
        NAMESPACE    = Word.NAMESPACE
        PARAGRAPH    = Word.PARAGRAPH
        CONTENT      = Word.CONTENT
        PAFORMAT     = Word.PAFORMAT
        TEXT         = Word.TEXT
        BOLD         = Word.BOLD
        ITALIC       = Word.ITALIC
        NOPROF       = Word.NOPROF
        COLOR        = Word.COLOR
        SIZE         = Word.SIZE
        LANG         = Word.LANG
        FONTS        = Word.FONTS
        ATTRIBUTES   = Word.ATTRIBUTES
        NAMESPACEVAL = NAMESPACE+"val"
        ASCIIFONT = NAMESPACE+"ascii"
        ANSIFONT = NAMESPACE+"hAnsi"

        tree = self.tree
        paragraphs = []
        attributes_dict = {}
        for paragraph in tree.iter(PARAGRAPH):
            texts = []
            for content in paragraph.iter(CONTENT):
                paformat = content.find(PAFORMAT)
                if paformat:
                    # Text node
                    node = content.find(TEXT)
                    contentstring = node.text
                    # Text Attributes
                    bval      = paformat.find(BOLD).attrib.get(NAMESPACEVAL)
                    ival      = paformat.find(ITALIC).attrib.get(NAMESPACEVAL)
                    noproof   = paformat.find(NOPROF).attrib.get(NAMESPACEVAL)
                    color     = paformat.find(COLOR).attrib.get(NAMESPACEVAL)
                    if color == "000000":
                        nondefaultcolor = '0'
                    else:
                        nondefaultcolor = '1'
                    size      = paformat.find(SIZE).attrib.get(NAMESPACEVAL)
                    lang      = paformat.find(LANG).attrib.get(NAMESPACEVAL)
                    ascifont  = paformat.find(FONTS).attrib.get(ASCIIFONT)
                    ansifont  = paformat.find(FONTS).attrib.get(ANSIFONT)
                    attributevalues = [bval,ival,noproof,
                                       color,nondefaultcolor,size,
                                       lang,ascifont,ansifont]
                    if not attributes_dict:
                        for a in ATTRIBUTES:
                            attributes_dict[a] = []
                    # Concat text content with attribute tags
                    contentstring = r"<t><text>" + contentstring + r"<\text>"
                    for a, av in zip(ATTRIBUTES, attributevalues):
                        contentstring+=r'{' + a + r':' + av + r'}'
                        attributes_dict[a].append(av)
                    texts.append(contentstring + r"<\t>")
            
            # Join paragraph texts strings and append to paragraphs
            jointexts = ''.join(texts)
            paragraphs.append(r"<p>" + jointexts + r"<\p>")
        
        return '\r\n'.join(paragraphs), attributes_dict


def modify_sequence(sentence_onlist, sentence_offlist, paravote, globalvote, count):
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
        [type] -- [description]
    """
    import pandas as pd
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
    
    # Systematic chech if and in what order DataFrames should be initialized
    if len(sentence_onlist) == len(sentence_offlist):
        qadf = check_vote(paravote)
        if qadf == None:
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