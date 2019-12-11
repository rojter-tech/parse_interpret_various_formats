try:
    from xml.etree.cElementTree import XML
except ImportError:
    from xml.etree.ElementTree import XML
import zipfile
import os
import re

def load_docx_file(datadir, docx_filename):
    filepath = os.path.join(datadir, docx_filename)
    docx_file = zipfile.ZipFile(filepath)
    return docx_file

def find_docname_string(docx_file):
    documentname = ""
    for name in docx_file.namelist():
        if re.match(r".*document.*xml.*", str(name)):
            documentname=name
            break
    return documentname

def get_xml_content_tree(docx_file):
    documentname = find_docname_string(docx_file)
    xml_content = docx_file.read(documentname)
    docx_file.close()
    tree = XML(xml_content)
    return tree

def parse_paragraphs(docx_file):
    """Simple bold detection word xml parser
    
    Arguments:
        docx_file {[ZipFile]} -- ZipFile of Word XML data
    
    Returns:
        [str] -- [description]
    """
    WORD_NAMESPACE = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
    PARA = WORD_NAMESPACE + 'p'
    WR = WORD_NAMESPACE + 'r'
    TEXT = WORD_NAMESPACE + 't'
    FORMATTYPE = WORD_NAMESPACE + 'rsidRPr'
    tree = get_xml_content_tree(docx_file)
    paragraphs_bold, paragraphs = [], []
    for paragraph in tree.getiterator(PARA):
        texts_bold, texts = [], []
        for formatting in paragraph.getiterator(WR):
            for node in formatting.getiterator(TEXT):
                if formatting.attrib.get(FORMATTYPE) and node.text:
                    texts_bold.append(node.text)
                elif node.text:
                    texts.append(node.text)
        if texts_bold: paragraphs_bold.append(''.join(texts_bold))
        if texts: paragraphs.append(''.join(texts))

    return paragraphs_bold, paragraphs

def main():
    DATADIR = 'data'
    DOCX_FILENAME = 'Word_Questions.docx'   
    docx_file = load_docx_file(DATADIR, DOCX_FILENAME)
    paragraphs_bold, paragraphs = parse_paragraphs(docx_file)

    print('\n'.join(paragraphs_bold))
    print('\n'.join(paragraphs))

if __name__=="__main__":
    main()