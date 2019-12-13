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
            if re.match(r".*document.*xml.*", str(name)):
                documentname=name
                break
        self.documentname = documentname

    def get_xml_content_tree(self):
        self.xml_content = self.docx_file.read(self.documentname)
        self.docx_file.close()
        self.tree = XML(self.xml_content)

    def parse_paragraphs_split_bold(self, splitbold=True):
        """Simple word xml parser, capable of collecting bold segments
        and returning two separate lists of paragraphs containg only bold and
        non bold text, or just returning all text in all paragraphs.
        
        Returns:
            [[str],[str]] -- Paragraphs bold / non bold text in a 2D list
        """
        NAMESPACE = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
        WP = NAMESPACE + 'p'
        WR = NAMESPACE + 'r'
        TEXT = NAMESPACE + 't'
        FORMAT = NAMESPACE + 'rPr'
        BOLD = NAMESPACE + 'b'
        NON_WHITEPACE = '\S'

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
                    if splitbold:
                        if isbold and node.text:
                            texts_bold.append(node.text)
                        elif node.text:
                            texts.append(node.text)
                    else:
                        texts.append(node.text)
            bold_text = ''.join(texts_bold); matchbold = re.search(NON_WHITEPACE, bold_text)
            nonbold_text = ''.join(texts); match_non_bold = re.search(NON_WHITEPACE, nonbold_text)
            
            if matchbold: 
                paragraphs_bold.append(bold_text)
            if match_non_bold:
                paragraphs.append(nonbold_text)

        return paragraphs, paragraphs_bold