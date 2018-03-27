# Copyright [2018] [Gang Ling, Yuliya Lierler]
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


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
