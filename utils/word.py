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
        filepath = os.path.join(datadir, filename)
        docx_file = ZipFile(filepath)
        self.datadir = datadir
        self.filename = filename
        self.docx_file = docx_file
    
    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)
    
    def find_docname_string(self):
        documentname = ""
        for name in self.docx_file.namelist():
            if re.match(r".*document.*xml.*", str(name)):
                documentname=name
                break
        return documentname

    def get_xml_content_tree(self):
        documentname = self.find_docname_string()
        xml_content = self.docx_file.read(documentname)
        self.docx_file.close()
        tree = XML(xml_content)
        return tree

    def parse_paragraphs_split_bold(self, splitbold=False):
        """Simple word xml parser, capable of collecting bold segments
        and returning two separate lists of paragraphs containg only bold and
        non bold text, or just returning all text in all paragraphs.
        
        Returns:
            ([str],[str]) -- Paragraphs text in a tuple of lists
        """
        WORD_NAMESPACE = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
        WP = WORD_NAMESPACE + 'p'
        WR = WORD_NAMESPACE + 'r'
        TEXT = WORD_NAMESPACE + 't'
        BOLD = WORD_NAMESPACE + 'rsidRPr'
        tree = self.get_xml_content_tree()
        paragraphs_bold, paragraphs = [], []
        for paragraph in tree.getiterator(WP):
            texts_bold, texts = [], []
            for formatting in paragraph.getiterator(WR):
                for node in formatting.getiterator(TEXT):
                    if splitbold:
                        if formatting.attrib.get(BOLD) and node.text:
                            texts_bold.append(node.text)
                        elif node.text:
                            texts.append(node.text)
                    else:
                        texts.append(node.text)
            if texts_bold: paragraphs_bold.append(' '.join(texts_bold))
            if texts: paragraphs.append(''.join(texts))

        return paragraphs, paragraphs_bold