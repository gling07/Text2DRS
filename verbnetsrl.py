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
    # for i in m_dct_lst:
    #     print(i)
    deep_process(m_dct_lst)
    for i in m_dct_lst:
        print(i)
    # check_themeroles(m_dct_lst)


    # for item in lst:
    #     # print(item)
    #     # check whether the length of current list
    #     # in case, sometime lth output list length is 11
    #     # add missing data in index 10 (Pred)
    #     if len(item) < 12:
    #         item.insert(10,'_')
    #     tmp = {}
    #     tmp.fromkeys(['ID', 'Form', 'PLemma', 'PPOS', 'PHead', 'PDeprel', 'Pred', 'Args','vn-pb'], None)
    #
    #     tmp['ID'] = item[0]
    #     tmp['Form'] = item[1]
    #     tmp['PLemma'] = item[2]
    #     tmp['PPOS'] = item[4]
    #     tmp['PHead'] = item[8]
    #     tmp['PDeprel'] = item[9]
    #     tmp['Pred'] = item[10]
    #     tmp['Args'] = item[11].split('\n')[0]
    #
    #     # process to separate each sentence's data
    #     if int(item[0]) > count:
    #         sub_dct_lst.append(tmp)
    #         count += 1
    #     else:
    #         count = 0
    #         m_dct_lst.append(sub_dct_lst)
    #         sub_dct_lst = list()
    #         sub_dct_lst.append(tmp)
    #
    # m_dct_lst.append(sub_dct_lst)
    #
    # pre_check_args(m_dct_lst)
    # deep_process(m_dct_lst)
    # check_themeroles(m_dct_lst)


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

    noun_lst = ['NNP', 'NN']
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
                if entry.get('PPOS') in noun_lst and entry.get('Args:' + pred) == '_':
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
    verb_pos = ['VBD', 'VB']
    for sentence in dct_lst:
        # parse_result = list()
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



            # for entry in sentence:
            #     vn_themeroles = dict()
            #     vn_class = list()
            #     if entry.get('Pred') == pred and entry.get('PPOS') in verb_pos:
            #         plemma = entry.get('PLemma')
            #         # parse_result.append(vn_pb_parser(pred, plemma))
            #         vn_themeroles = vn_pb_parser(pred, plemma)
            #         vn_class = list(vn_themeroles.keys())
            #         entry[pred + ':vn'] = vn_class
            #     if len(vn_class) > 0:
            #         for entry in sentence:
            #             if entry.get('Args:' + pred) != '_':
            #                 roles = list()
            #
            #                 for vc in vn_class:
            #                     sub_dct = vn_themeroles.get(vc)
            #                     for rl in sub_dct:
            #                         if entry.get('Args:' + pred)[1:] in rl:
            #                             roles.append([vc, rl.get(entry.get('Args:' + pred)[1:])])
            #                         else:
            #
            #                             roles.append([vc, 'NONE-TMEMEROLE'])
            #
            #                 entry[pred + ':vn'] = roles
            #             else:
            #                 entry[pred + ':vn'] = ['_']


def get_themeroles(sentence, pred, verb_pos):
    vn_themeroles = dict()
    for entry in sentence:
        if entry.get('Pred') == pred and entry.get('PPOS') in verb_pos:
            plemma = entry.get('PLemma')
            vn_themeroles = vn_pb_parser(pred, plemma)
            break
    return vn_themeroles



        # for sub_dct in sentence:
        #     plemma = sub_dct.get('PLemma')
        #     if sub_dct.get('Pred') != '_' and sub_dct.get('Pred') is not None \
        #             and sub_dct.get('PDeprel') == 'ROOT':
        #         pred = sub_dct.get('Pred')
        #         parse_result = vn_pb_parser(pred, plemma)
        #     else:
        #         continue

        # key_lst = list(parse_result.keys())
        #
        # pb_arg_num = list()
        # for k in key_lst:
        #     sub_lst = parse_result.get(k)
        #     for s in sub_lst:
        #         pb_arg_num.append(list(s.keys()))
        #
        # num = [n for sub_lst in pb_arg_num for n in sub_lst]
        #
        # # process to analysis vn-pb data and add to sentence's dictionary
        # for d in sentence:
        #     if d.get('Pred') == pred:
        #         tmp2 = list()
        #         for k in key_lst:
        #             tmp2.append(['vn', k])
        #         d['vn-pb'] = tmp2
        #     elif d.get('Args') != '_':
        #         tmp3 = list()
        #         for key in key_lst:
        #             pr_lst = parse_result.get(key)
        #             for p in pr_lst:
        #                 k_lst = p.keys()
        #
        #                 for x in k_lst:
        #                     if x == d.get('Args')[1:] and d.get('Args')[1:] in num:
        #                         tmp3.append([key, p.get(x)])
        #                     elif d.get('Args')[1:] in num:
        #                         continue
        #                     elif 'vn-pb' not in d and not pb_args_checker(x, sentence):
        #                         tmp3.append('_')
        #         if len(tmp3) == 0:
        #             tmp3.append('_')
        #         d['vn-pb'] = tmp3
        #     else:
        #         d['vn-pb'] = ['_']


def check_themeroles(dct_lst):
    for sentence in dct_lst:
        predicates = list()
        for entry in sentence:
            if entry.get('Pred') != '_' and entry.get('PDeprel') == 'ROOT':
                predicates = entry.get('vn-pb')

        for entry in sentence:
            if entry.get('Args') != '_' and entry.get('vn-pb')[0] == '_':
                roles = list()
                for pred in predicates:
                    roles.append([pred[1], 'NONE-TMEMEROLE'])
                entry['vn-pb'] = roles


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
