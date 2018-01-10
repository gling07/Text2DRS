
def coreference(xml):
    coref_dictionary = {}
    root = xml.getroot()
    for elem in root.findall('./document/coreference/coreference/'):
        entity = elem.find('text').text
        print(entity)

def read_xml(xml_tree):
    corenlp_xml = xml_tree
    coreference(corenlp_xml)