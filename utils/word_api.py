try:
    from xml.etree.cElementTree import XML
except ImportError:
    from xml.etree.ElementTree import XML
from zipfile import ZipFile
import os, re

class Word:
    """
    Parsing word file API.
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
    
    def parse_paragraphs_texts(self, splitbold=False):
        """Simple word xml parser, collecting text data.
        
        Returns:
            [str] -- Paragraphs texts
        """
        NAMESPACE = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'

        PARAGRAPH = NAMESPACE + r'p'
        
        PACONTENT = NAMESPACE + r'r'
        PAFORMAT = NAMESPACE + r'rPr'
        BOLD = NAMESPACE + r'b'
        ITALIC = NAMESPACE + r'i'
        NOPROF = NAMESPACE + r'noProof'
        COLOR = NAMESPACE + r'color'
        SIZE = NAMESPACE + r'sz'
        LANG = NAMESPACE + r'lang'
        FONTS = NAMESPACE + r'rFonts'
        
        TEXT = NAMESPACE + r't'

        tree = self.tree
        paragraphs = []
        for paragraph in tree.iter(PARAGRAPH):
            texts = []
            for pacontent in paragraph.findall(PACONTENT):
                paformat = pacontent.find(PAFORMAT)
                if paformat:
                    # Text node
                    node = pacontent.find(TEXT)
                    pastring = node.text
                    # Text Attributes
                    bval = list(paformat.find(BOLD).attrib.values())[0]
                    ival = list(paformat.find(ITALIC).attrib.values())[0]
                    noproof = list(paformat.find(NOPROF).attrib.values())[0]
                    color = list(paformat.find(COLOR).attrib.values())[0]
                    size = list(paformat.find(SIZE).attrib.values())[0]
                    lang = list(paformat.find(LANG).attrib.values())[0]
                    fontval = list(paformat.find(FONTS).attrib.values())[0]
                    attr = ['bval','ival','noproof','color','size','lang','fontval']
                    attrval = [bval,ival,noproof,color,size,lang,fontval]
                    
                    pastring = '<t>{text:' + pastring + '}'
                    for t,v in zip(attr, attrval):
                        pastring+='{'+t+':'+v+'}' 
                    texts.append(pastring + '<\\t>')
            
            # Join paragraph texts strings and append to paragraphs
            jointexts = ''.join(texts)
            paragraphs.append('<p>' + jointexts + '<\\p>')       

        return '\r\n'.join(paragraphs)