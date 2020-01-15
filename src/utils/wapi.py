try:
    from xml.etree.cElementTree import XML
except ImportError:
    from xml.etree.ElementTree import XML
from zipfile import ZipFile, BadZipFile
from utils.errors import Error, rOjterError
import pandas as pd
import os, re

# Dev
from xml.dom.minidom import parseString


class Word:
    """
    Parsing word file API.
    """
    # Word namespace tag
    NAMESPACE = r'{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
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

    ################################### Dev #####################################
    def show_xml(self):                                                         #
        print(parseString(self.xml_content).toprettyxml(indent='    '))         #
    ################################### Dev #####################################                                                                    #
    def save_as_xml(self,filepath):                                             #
        with open(filepath, mode='wt', encoding='utf_8') as f:                  #
            f.write(parseString(self.xml_content).toprettyxml(indent='    '))   #
    ################################### Dev #####################################

    def __init__(self, filepath):
        self.datadir = os.path.basename(os.path.dirname(filepath))
        self.filename = os.path.basename(filepath)
        try:
            self.docx_file = ZipFile(filepath)
        except BadZipFile:
            print(self.filename, "is not a docx file")
            raise rOjterError("Bad docx document: " + self.filename)
        
        # Main structure
        self.tree = []

        # Main attributes
        self.documentname = []
        self.xml_content = []
        self.content = []
        self.raw_text = []

        # Statistics attributes
        self.n_raw_text_lines = 0
        self.n_non_empty_lines = 0
        self.attributes_dict = []
        self.sentence_per_paragraph = 0

        # Initialize Word object
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

        def _get_attr_val(tree_element, attribute, namespace):
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
                    bval     = _get_attr_val(paformat, BOLD, NAMESPACEVAL)
                    ival     = _get_attr_val(paformat, ITALIC, NAMESPACEVAL)
                    noproof  = _get_attr_val(paformat, NOPROF, NAMESPACEVAL)
                    color    = _get_attr_val(paformat, COLOR, NAMESPACEVAL)
                    if color == "000000":
                        nondefaultcolor = '0'
                    else:
                        nondefaultcolor = '1'
                    size     = _get_attr_val(paformat, SIZE, NAMESPACEVAL)
                    lang     = _get_attr_val(paformat, LANG, NAMESPACEVAL)
                    ascifont = _get_attr_val(paformat, FONTS, ASCIIFONT)
                    ansifont = _get_attr_val(paformat, FONTS, ANSIFONT)
                    attributevalues = [bval,ival,noproof,
                                       color,nondefaultcolor,size,
                                       lang,ascifont,ansifont]
                    if not attributes_dict:
                        for a in ATTRIBUTES:
                            attributes_dict[a] = []
                    # Concat text content with attribute tags
                    contentstring = r"<t><text>" + contentstring + r"<\text>"
                    for a, av in zip(ATTRIBUTES, attributevalues):
                        if av:
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
        def _count_sentences(line):
            n_questions = line.count('?')
            n_standards = line.count('.')
            n_exclamaitions = line.count('!')
            n_sentence = n_questions + n_standards + n_exclamaitions
            return n_sentence

        paragraphs = re.findall(r'(?<=<p>).*?(?=<\\p>)', self.content)
        lines = []
        n_raw_text_lines = 0
        n_non_empty_lines = 0
        n_sentences = 0
        for paragraph in paragraphs:
            texts = re.findall(r'(?<=<t>).*?(?=<\\t>)', paragraph)
            line = []
            for text in texts:
                thistext = re.search(r"(?<=<text>).*?(?=<\\text>)", text).group()
                line.append(thistext)
            thisline = ''.join(line)

            lines.append(thisline)
            n_raw_text_lines+=1

            if re.search(r'\S', thisline):
                n_non_empty_lines+=1
                n_sentences+=_count_sentences(thisline)

        if n_non_empty_lines != 0:
            self.sentence_per_paragraph = n_sentences/n_non_empty_lines
        
        
        self.raw_text = '\r\n'.join(lines)+'\r\n' # Adding potentially missing last linefeed
        # Statistics
        self.n_raw_text_lines = n_raw_text_lines
        self.n_non_empty_lines = n_non_empty_lines

