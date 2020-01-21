from xml.dom.minidom import parseString

def save_xml(xml_filepath, savepath):
    with open(xml_filepath) as f:
        xml_string = f.read()
        pretty_xml = parseString(xml_string).toprettyxml(indent='   ')
        with open(savepath, mode='wt', encoding='utf-8') as w: w.write(pretty_xml)

sheet_filepath = "xlsx_example/xl/worksheets/sheet1.xml"
string_filepath = "xlsx_example/xl/sharedStrings.xml"

save_xml(sheet_filepath, "sheet.xml")
save_xml(string_filepath, "string.xml")