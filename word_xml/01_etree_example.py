import xml.etree.cElementTree as ET
from xml.dom.minidom import parseString
import os

# Build a basic html tree structure
root = ET.Element("html")

# From root (html tag)
head = ET.SubElement(root, "head")
title = ET.SubElement(head, "title")
title.text = "rOjters very Advanced Web Page - Be Amazed"

# From root (html tag)
body = ET.SubElement(root, "body")
body.set("bgcolor", "#ffffff")
body.text = "Hello, World!"

# Wrap it in an ElementTree instance, and save as html
tree = ET.ElementTree(root)
SAVEPATH = os.path.join("etree_html_example","page.html")
xmlout = ET.tostring(root, method="html", encoding='utf_8')
xmlout = parseString(xmlout).toprettyxml(indent='    ')
with open(SAVEPATH, 'w') as f: f.write(xmlout)

# Load previously saved html
load_tree = ET.parse(SAVEPATH)

# Compare outputs
print("Equal output:",tree.findtext("head/title") == load_tree.findtext("head/title"))