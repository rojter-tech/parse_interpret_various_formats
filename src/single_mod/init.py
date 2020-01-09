try:
    from xml.etree.cElementTree import XML
except ImportError:
    from xml.etree.ElementTree import XML
from zipfile import ZipFile
import pandas as pd
import os, re


class Error(Exception):
   """Base class for non-rOjter exceptions >D"""
   pass


class rOjterError(Error):
   """Raised when rOjter is just too smart not to handle this"""
   pass


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


    def __init__(self, filepath):
        self.datadir = os.path.basename(os.path.dirname(filepath))
        self.filename = os.path.basename(filepath)
        self.docx_file = ZipFile(filepath)
        
        self.documentname = []
        self.xml_content = []
        self.tree = []
        self.content = []
        self.attributes_dict = []
        self.raw_text = []
        

        # Initialize Word object attributes
        self.find_docname_string()
        self.get_xml_content_tree()
        self.extract_content()
        self.extract_raw_text()


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


    def extract_content(self):
        """Simple word xml parser, collecting text data with corresponding
           text attributes, and creates a formatted string output with nested
           tagging
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

        def get_attr_val(tree_element, attribute, namespace):
            find_attribute = tree_element.find(attribute)
            if find_attribute != None:
                value = find_attribute.attrib.get(namespace)
            else:
                value = "0"
            return value

        tree = self.tree
        paragraphs = []
        attributes_dict = {}
        for paragraph in tree.iter(PARAGRAPH):
            texts = []
            for content in paragraph.iter(CONTENT):
                # Text node
                node = content.find(TEXT)
                contentstring = node.text
                # Formatting attributes
                paformat = content.find(PAFORMAT)
                if paformat:
                    # Text Attributes
                    bval     = get_attr_val(paformat, BOLD, NAMESPACEVAL)
                    ival     = get_attr_val(paformat, ITALIC, NAMESPACEVAL)
                    noproof  = get_attr_val(paformat, NOPROF, NAMESPACEVAL)
                    color    = get_attr_val(paformat, COLOR, NAMESPACEVAL)
                    if color == "000000":
                        nondefaultcolor = '0'
                    else:
                        nondefaultcolor = '1'
                    size     = get_attr_val(paformat, SIZE, NAMESPACEVAL)
                    lang     = get_attr_val(paformat, LANG, NAMESPACEVAL)
                    ascifont = get_attr_val(paformat, FONTS, ASCIIFONT)
                    ansifont = get_attr_val(paformat, FONTS, ANSIFONT)
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
        
        self.content = '\r\n'.join(paragraphs)
        self.attributes_dict = attributes_dict

    def extract_raw_text(self):
        """Tries to respresent the text content as pure as possible
           as if it were a plain text document.
        """
        paragraphs = re.findall(r'(?<=<p>).*?(?=<\\p>)', self.content)
        lines = []
        for paragraph in paragraphs:
            texts = re.findall(r'(?<=<t>).*?(?=<\\t>)', paragraph)
            line = []
            for text in texts:
                thistext = re.search(r"(?<=<text>).*?(?=<\\text>)", text).group()
                line.append(thistext)
            lines.append(''.join(line))
        
        # Adding potentially missing last linefeed
        self.raw_text = '\r\n'.join(lines)+'\r\n'


####################################################################
################### ATTRIBUTE SELECTION TOOLS ######################
####################################################################


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


######################################################################
####################### RAW FORMAT SELECTION TOOLS ###################
######################################################################


def format_one(raw_text):
    """QA separation by tag
    """
    questions = re.findall(r'(?<=Q: ).*?(?=A:)|(?<=Q: ).*?(?=\n)', raw_text)
    if len(questions) == 0:
        raise rOjterError("No way, you dont want to go there ...")
    answers =   re.findall(r'(?<=A: ).*?(?=Q:)|(?<=A: ).*?(?=\n)', raw_text)
    if (len(questions) == len(answers))and questions != []:
        Q = pd.DataFrame(questions, columns=['Q'])
        A = pd.Series(answers, name='A')
        qadf = Q.join(A)
    else:
        print('Number of questions do\'nt match up with the number of answers')
        raise rOjterError("No way, you dont want to go there ...")

    # Clean beginning and trailing whitepaces
    qalist = []
    for Q, A in zip(qadf.iloc[:,0],qadf.iloc[:,1]):
        qalist.append([Q.strip(),A.strip()])

    qadf = pd.DataFrame(qalist, columns=["Q","A"])
    print("QA tag separation suceeded.")
    return qadf


def format_two(raw_text):
    """QA separation by two line QA combination.
    """
    def process_combinations(combinations):
        qalist = []

        for combo in combinations:
            Q = combo[0].strip()
            A = combo[1].strip()
            qalist.append([Q,A])
        
        return qalist
    
    combinations = re.findall(r'(\S.*?\n)(\S.*?\n)\r\n', raw_text)
    if combinations:
        if type(combinations[0]) == tuple:
            qalist = process_combinations(combinations)
            qadf = pd.DataFrame(qalist, columns=["Q","A"])
            print("QA two line separation suceeded.")
            return qadf
        else:
            print("There is no two line combination in this file")
            raise rOjterError("No way, you dont want to go there ...")
    else:
        raise rOjterError("No way, you dont want to go there ...")


def format_ten(raw_text):
    """Raw string parser for QA pairing on same line with mixed separators.
       This format assumes that every QA pair is one the same line and that
       questions preceeds answers.
    """

    splitqa, dump = [], []
    for line in re.findall(r"\S.*\n", raw_text):
        regsplit = re.findall(r".*\?|\S.*?\.|\S.*?\n|\ .*?\n", line) # Split by pattern
        if len(regsplit) == 2:
            regsplit[0] = regsplit[0].strip()
            regsplit[1] = regsplit[1].strip()
            splitqa.append(regsplit)
        else:
            dump.append(line)
            print("Dump!")
            raise rOjterError("No way, you dont want to go there ...")
    
    if len(dump) == 0:
        print('Hurray No lines in dump list.')
        qadf = pd.DataFrame(splitqa, columns=['Q','A'])
        print("QA general text separation suceeded.")
        return qadf
    else:
        print('Dump list contains rows that dont match')
        raise rOjterError


format_functions = [format_one, format_two, format_ten]


def try_separate_by_rawtext(wordobject, format_functions):
    check = False
    for format_function in format_functions:
        try:
            qadf = format_function(wordobject.raw_text)
            if len(qadf) != 0:
                check = True
            else:
                print("DataFrame size invalid")
                raise rOjterError
            break
        except rOjterError:
            print(wordobject.filename, "format excluded.")
    
    if check:
        return qadf
    else:
        print("")
        print("***********************************************")
        print("**!!!!Format detection did not sucess!!!!**")
        print("***********************************************")
        print("")
        print("QA by " + wordobject.filename + " format could not be determined ...")
        return wordobject.filename



###############################################################
######################### MAIN LOADERS ########################
###############################################################



def load_word_object(wordfilepath):
    wordobject = Word(wordfilepath)
    return wordobject


def process_wordobject(wordobject, format_type = None):
    print("\n\nProcessing", wordobject.filename)
    print(80*"*","\nTrying:",wordobject.filename,"...")
    qadata = try_separate_by_attribute(wordobject)

    if type(qadata) == str:
        qadata = try_separate_by_rawtext(wordobject, format_functions)
    else:
        print("\nQA separation by attribute was executed for", wordobject.filename)
        format_type = "Attribute"
        return qadata, format_type

    if type(qadata) == str:
        print("\nNo separation process attempt did succeeded for", wordobject.filename, "!!")
        format_type = "UnknownFormat"
        return qadata, format_type
    else:
        print("\nQA separation by raw text format was executed for", wordobject.filename)
        format_type = "RawTextFormat"
        return qadata, format_type


def load_qa_from_docx(wordfilepath):
    """Main dataframe loader
    
    Arguments:
        wordfilepath {str} -- Absolute path to word-file
    
    Returns:
        pandas.DataFrame -- Final QA dataframe
    """
    wordobject = load_word_object(wordfilepath)
    qadf = process_wordobject(wordobject)
    return qadf

def main():
    wordfilepath = "/home/dreuter/Environments/parse_interpret_various_formats/src/data/formatted_word_data/QAb.docx"
    print(load_qa_from_docx(wordfilepath))

if __name__ == "__main__":
    main()