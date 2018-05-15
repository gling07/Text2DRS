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


# no arg: none
# have arg but no mapping: PropBank: arg


import xml.etree.ElementTree as ET

# parse vb-pb mapping file into a element tree
pb_tree = ET.parse('semLink/vn-pb/vnpbMappings')
m_dct_lst = list()

def bias_pbTovb_mapping():
    bias_verbClass = {'go.01': '51.1',
                      'move.01': '51.3.1'}
    return bias_verbClass

# process lth outputs into a list of dictionary
# each sentence in the original input file is a dictionary
def read_data(lth_output):
    data_lst = list()
    for line in lth_output:
        sub_line = line.split('\t')
        # ingore empty line in the lth output
        if len(sub_line) < 2:
            continue
        else:
            data_lst.append(sub_line)

    form_dct(data_lst)

    return m_dct_lst


# A method to form each sentence's data into a dictionary
def form_dct(lst):

    # make sure master dictionary list is empty
    # if not, clean it's memory data
    if len(m_dct_lst) > 0:
        del m_dct_lst[:]

    sub_dct_lst = list()
    count = 0
    # lst is a list of lists

    sentences_lst = form_sentence(lst)
    for sentence in sentences_lst:

        pred_lst = list()
        for item in sentence:
            if item[10] != '_':
                pred_lst.append(item[10])

        for item in sentence:
            item_dct = dict()
            item_dct['ID'] = item[0]
            item_dct['Form'] = item[1]
            item_dct['PLemma'] = item[2]
            item_dct['PPOS'] = item[4]
            item_dct['PHead'] = item[8]
            item_dct['PDeprel'] = item[9]
            item_dct['Pred'] = item[10]

            args_len = len(pred_lst)
            idx = 11
            for pred in pred_lst:
                if idx == 10 + args_len:
                    item_dct['Args:' + pred] = item[idx].split('\n')[0]
                else:
                    item_dct['Args:' + pred] = item[idx]
                    idx += 1
            sub_dct_lst.append(item_dct)

        m_dct_lst.append(sub_dct_lst)
        sub_dct_lst = list()


    pre_check_args(m_dct_lst)
    deep_process(m_dct_lst)
    # check_themeroles(m_dct_lst)
    remove_not_vbclass(m_dct_lst)


# a method to organize sentences items into a list
def form_sentence(sentences):
    sentences_lst = list()
    sentence = list()

    for item in sentences:
        if item[0] == '1' and len(sentence) > 1:
            sentences_lst.append(sentence)
            sentence = list()
            sentence.append(item)
        elif item[0] == '1' and len(sentence) == 0:
            sentence.append(item)
        else:
            sentence.append(item)
    sentences_lst.append(sentence)

    return sentences_lst


def pre_check_args(dct_lst):
    noun_lst = ['NNP', 'NN', 'PRP']
    preposition = ['IN', 'TO']
    for sentence in dct_lst:
        pred_lst = get_predicates(sentence)
        for pred in pred_lst:
            args_count = count_args(sentence, pred)
            for entry in sentence:
                if entry.get('PPOS') in noun_lst:
                    if args_count > 0:
                        args_count -= 1
                    else:
                        entry['Args:' + pred] = 'NONE-ARGS'

            temp = list()
            for entry in sentence:
                if entry.get('PPOS') in preposition and entry.get('Args:' + pred) != '_':
                    temp.append(entry.get('Args:' + pred))
                    entry.update({'Args:' + pred : '_'})

            for entry in sentence:
                if entry.get('PPOS') in noun_lst and entry.get('Args:' + pred) == '_' and len(temp) > 0:
                    entry.update({'Args:' + pred : temp[0]})
                    del temp[0]


def count_args(sentence, pred):
    count = 0
    for entry in sentence:
        if entry.get('Args:' + pred) != '_':
            count += 1
    return count


def get_predicates(sentence):
    predicates = list()
    for entry in sentence:
        if entry.get('Pred') != '_':
            predicates.append(entry.get('Pred'))

    return predicates


# A method to process a list of dictionary and add vn-pb's values
def deep_process(dct_lst):
    verb_pos = ['VBD', 'VB', 'VBN', 'VBG']
    for sentence in dct_lst:
        pred_lst = get_predicates(sentence)
        for pred in pred_lst:
            vn_themeroles = get_themeroles(sentence, pred, verb_pos)
            vn_class = list(vn_themeroles.keys())
            if len(vn_class) > 0:
                for entry in sentence:
                    if entry.get('Pred') == pred:
                        entry[pred + ':vb-class'] = vn_class
                    elif entry.get('Args:' + pred) != '_':
                        roles = list()
                        for vc in vn_class:
                            for rd in vn_themeroles.get(vc):
                                r_num = entry.get('Args:' + pred)[1:]
                                if r_num in list(rd.keys()):
                                    roles.append([vc, rd.get(r_num)])
                                    break
                            if len(roles) == 0:
                                roles.append([vc, 'NONE-THEMEROLE'])
                        entry[pred + ':vn-class'] = roles
                    else:
                        entry[pred + ':vn-class'] = ['_']


def get_themeroles(sentence, pred, verb_pos):
    vn_themeroles = dict()
    for entry in sentence:
        if entry.get('Pred') == pred and entry.get('PPOS') in verb_pos:
            plemma = entry.get('PLemma')
            vn_themeroles = vn_pb_parser(pred, plemma)
            break
    return vn_themeroles


def check_themeroles(dct_lst):
    for sentence in dct_lst:
        predicates = get_predicates(sentence)
        for pred in predicates:
            for entry in sentence:
                if entry.get('Args:' + pred) != '_' and len(entry.get(pred + ':vn-class')) == 0:
                    entry[pred + ':vn-class'] = ['NON-THEMEROLE']


def remove_not_vbclass(dct_lst):
    verb_pos = ['VBD', 'VB', 'VBN', 'VBG']
    for sentence in dct_lst:
        predicates = get_predicates(sentence)
        remove_lst = list()
        for entry in sentence:
            pred = entry.get('Pred')
            if pred in predicates and entry.get('PPOS') not in verb_pos:
                remove_lst.append(pred)
                entry.update({'Pred':'_'})

        for p in remove_lst:
            for entry in sentence:
                del entry['Args:' + p]



# A method to check and tagging Args data
# If the Args's number is in the pb-roleset number list, return True, else return False
def pb_args_checker(num, sentence_lst):
    num_lst = list()
    for sub_dct in sentence_lst:
        if sub_dct.get('Args') != '_':
            num_lst.append(sub_dct.get('Args')[1:])

    if num in num_lst:
        return True
    else:
        return False


# A method to retrieve vn class data and args role data from vn-pb element tree
# using pred and plemma to located pb parent node in the tree,
# retrieve vn-class data and pb-roleset data from parent node to children node
def vn_pb_parser(pred, plemma):
    # bias_verbClass_mapping = bias_pbTovb_mapping()
    # bias_key_lst = list(bias_verbClass_mapping.keys())
    dct = dict()
    root = pb_tree.getroot()

    for elem in root.findall('./predicate'):
        if elem.attrib.get('lemma') == plemma:
            for argmap in elem:
                if argmap.attrib.get('pb-roleset') == pred:
                    lst = list()
                    for role in argmap:
                        sub_dct2 = dict()
                        sub_dct2[role.attrib.get('pb-arg')] = role.attrib.get('vn-theta')
                        lst.append(sub_dct2)
                    dct[argmap.attrib.get('vn-class')] = lst

    if len(dct.keys()) == 0:
        dct['NOT-FOUND-IN-SEMLINK'] = list()


    # if pred in bias_key_lst:
    #     vbClass = bias_verbClass_mapping.get(pred)
    #     remove = [k for k in dct if k != vbClass]
    #     for k in remove:
    #         del dct[k]
    return dct
