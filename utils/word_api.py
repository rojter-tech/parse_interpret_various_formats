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
                    bval      = paformat.find(BOLD).attrib.get(NAMESPACE+"val")
                    ival      = paformat.find(ITALIC).attrib.get(NAMESPACE+"val")
                    noproof   = paformat.find(NOPROF).attrib.get(NAMESPACE+"val")
                    color     = paformat.find(COLOR).attrib.get(NAMESPACE+"val")
                    if color == "000000":
                        defaultcolor = '1'
                    else:
                        defaultcolor = '0'
                    size      = paformat.find(SIZE).attrib.get(NAMESPACE+"val")
                    lang      = paformat.find(LANG).attrib.get(NAMESPACE+"val")
                    ascifont  = paformat.find(FONTS).attrib.get(NAMESPACE+"ascii")
                    ansifont  = paformat.find(FONTS).attrib.get(NAMESPACE+"hAnsi")
                    attr = ['bval','ival','noproof','color','defaultcolor','size','lang','ascifont','ansifont']
                    attrval = [bval,ival,noproof,color,defaultcolor,size,lang,ascifont,ansifont]
                    
                    pastring = '<t>{text:' + pastring + '}'
                    for t,v in zip(attr, attrval):
                        pastring+='{'+t+':'+v+'}' 
                    texts.append(pastring + '<\\t>')
            
            # Join paragraph texts strings and append to paragraphs
            jointexts = ''.join(texts)
            paragraphs.append('<p>' + jointexts + '<\\p>')       

        return '\r\n'.join(paragraphs)