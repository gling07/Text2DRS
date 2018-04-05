# MIT License
#
# Copyright (c) [2018] [Gang Ling (gling@unomaha.edu),
#                      Yuliya Lierler (ylierler@unomaha.edu)]
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


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

    return coref_dictionary


def prcoess_xml(xml_tree):
    corenlp_xml = xml_tree
    coref_dictionary = coreference(corenlp_xml)
    return coref_dictionary
