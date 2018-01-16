
def coreference(xml):
    coref_dictionary = {}
    root = xml.getroot()
    for elem in root.findall('./document/coreference/coreference/'):
        is_mention = elem.attrib.get('representative')
        if is_mention == 'true':
            word = elem.find('text').text
            sentence_id = int(elem.find('sentence').text)

            if word not in coref_dictionary:
                coref_dictionary[word] = [sentence_id]
            else:
                id_list = coref_dictionary.get(word)
                id_list.insert(0, sentence_id)
                coref_dictionary[word] = id_list
        else:
            word = elem.find('text').text
            sentence_id = int(elem.find('sentence').text)

            if word in coref_dictionary:
                id_list = coref_dictionary.get(word)
                id_list.append(sentence_id)
                coref_dictionary[word] = id_list
            else:
                id_list = [sentence_id]
                coref_dictionary[word] = id_list

    # for item in coref_dictionary.items():
    #     print(item)
    return coref_dictionary

def prcoess_xml(xml_tree):
    corenlp_xml = xml_tree
    coref_dictionary = coreference(corenlp_xml)
    return coref_dictionary
