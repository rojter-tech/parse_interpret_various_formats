try:
    from xml.etree.cElementTree import XML
except ImportError:
    from xml.etree.ElementTree import XML
from zipfile import ZipFile
import os, re

class Word:
    """
    Parse and separate paragraph text from Word docx formated files.
    """
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

    def parse_paragraphs(self, splitbold=False, clean_trailing_whitespace=False):
        """Simple word xml parser, capable of collecting bold segments
        and returning two separate lists of paragraphs containg only bold and
        non bold text, or just returning all text in all paragraphs.
        
        Returns:
            [[str],[str]] -- Paragraphs bold / non bold text in a 2D list
        """
        NAMESPACE = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
        WP = NAMESPACE + r'p'
        WR = NAMESPACE + r'r'
        TEXT = NAMESPACE + r't'
        FORMAT = NAMESPACE + r'rPr'
        BOLD = NAMESPACE + r'b'
        NON_WHITEPACE = r'\S'
        WHITESPACE = r'\s'

        tree = self.tree
        paragraphs_bold, paragraphs = [], []
        for paragraph in tree.getiterator(WP):
            texts_bold, texts = [], []
            for wr in paragraph.getiterator(WR):
                for formatting in wr.getiterator(FORMAT):
                    isbold = False
                    for bold in formatting.getiterator(BOLD):
                        isbold = list(bold.attrib.values())[0]
                        isbold = bool(int(isbold))
                for node in wr.getiterator(TEXT):
                    # Either split on bold or not
                    if splitbold:
                        if isbold and node.text:
                            texts_bold.append(node.text)
                        elif node.text:
                            texts.append(node.text)
                    else:
                        texts.append(node.text)
            
            # Join paragraph text strings and check if they are
            # containing non whitespace characters
            bold_text = ''.join(texts_bold); matchbold = re.search(NON_WHITEPACE, bold_text)
            nonbold_text = ''.join(texts); match_non_bold = re.search(NON_WHITEPACE, nonbold_text)

            # Take care of beginning and trailing whitespaces
            if clean_trailing_whitespace:
                if len(bold_text) > 1:
                    while re.match(WHITESPACE,bold_text[0]):
                        bold_text = bold_text[1:]
                    while re.match(WHITESPACE,bold_text[-1]):
                        bold_text = bold_text[:-1]
                if len(nonbold_text) > 1:
                    while re.match(WHITESPACE,nonbold_text[0]):
                        nonbold_text = nonbold_text[1:]
                    while re.match(WHITESPACE,nonbold_text[-1]):
                        nonbold_text = nonbold_text[:-1]

            if matchbold: 
                paragraphs_bold.append(bold_text)
            if match_non_bold:
                paragraphs.append(nonbold_text)

        return paragraphs, paragraphs_bold