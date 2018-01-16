
def coreference(xml):
    coref_dictionary = {}
    root = xml.getroot()
    for elem in root.findall('./document/coreference/coreference/'):
        # entity = elem.find('mention')
        # print(entity)
        # print (elem.attrib.get('representative'))
        is_mention = elem.attrib.get('representative')
        if is_mention == 'true':
            word = elem.find('text').text
            sentence_id = elem.find('sentence').text
            # print(word, sentence_id)
            if word not in coref_dictionary:
                coref_dictionary[word] = [sentence_id]
            else:
                id_list = coref_dictionary.get(word)
                id_list.insert(0, sentence_id)
                coref_dictionary[word] = id_list
        else:
            word = elem.find('text').text
            sentence_id = elem.find('sentence').text
            # print(word, sentence_id)
            if word in coref_dictionary:
                id_list = coref_dictionary.get(word)
                id_list.append(sentence_id)
                coref_dictionary[word] = id_list
            else:
                id_list = [sentence_id]
                coref_dictionary[word] = id_list

    for item in coref_dictionary.items():
        print(item)


def read_xml(xml_tree):
    corenlp_xml = xml_tree
    coreference(corenlp_xml)