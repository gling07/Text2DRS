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

import xml.etree.ElementTree as ET

# parse vb-pb mapping file into a element tree
pb_tree = ET.parse('semLink/vn-pb/vnpbMappings')
m_dct_lst = list()
# pb_verbs = propbank.verbs()

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
    for item in lst:
        # check whether the length of current list
        # in case, sometime lth output list length is 11
        # add missing data in index 10 (Pred)
        if len(item) < 12:
            item.insert(10,'_')
        tmp = {}
        tmp.fromkeys(['ID', 'Form', 'PLemma', 'PPOS', 'PHead', 'PDeprel', 'Pred', 'Args','vn-pb'], None)

        tmp['ID'] = item[0]
        tmp['Form'] = item[1]
        tmp['PLemma'] = item[2]
        tmp['PPOS'] = item[4]
        tmp['PHead'] = item[8]
        tmp['PDeprel'] = item[9]
        tmp['Pred'] = item[10]
        tmp['Args'] = item[11].split('\n')[0]

        # process to separate each sentence's data
        if int(item[0]) > count:
            sub_dct_lst.append(tmp)
            count += 1
        else:
            count = 0
            m_dct_lst.append(sub_dct_lst)
            sub_dct_lst = list()
            sub_dct_lst.append(tmp)
    m_dct_lst.append(sub_dct_lst)

    deep_process(m_dct_lst)


# A method to process a list of dictionary and add vn-pb's values
def deep_process(dct_lst):

    for lst in dct_lst:
        parse_result = dict()
        pred = ''
        for sub_dct in lst:
            # pred = sub_dct.get('Pred')
            plemma = sub_dct.get('PLemma')
            if sub_dct.get('Pred') != '_' and sub_dct.get('Pred') is not None \
                    and sub_dct.get('PDeprel') == 'ROOT':
                pred = sub_dct.get('Pred')
                parse_result = vn_pb_parser(pred, plemma)
            else:
                continue

        key_lst = list(parse_result.keys())
        # print(parse_result)

        pb_arg_num = list()
        for k in key_lst:
            sub_lst = parse_result.get(k)
            for s in sub_lst:
                pb_arg_num.append(list(s.keys()))

        num = [n for sub_lst in pb_arg_num for n in sub_lst]

        # process to analysis vn-pb data and add to sentence's dictionary
        for d in lst:
            if d.get('Pred') == pred:
                tmp2 = list()
                for k in key_lst:
                    tmp2.append(['vn', k])
                d['vn-pb'] = tmp2
            elif d.get('Args') != '_':
                tmp3 = list()
                for key in key_lst:
                    pr_lst = parse_result.get(key)
                    for p in pr_lst:
                        k_lst = p.keys()

                        for x in k_lst:
                            if x == d.get('Args')[1:] and d.get('Args')[1:] in num:
                                tmp3.append([key, p.get(x)])
                            elif d.get('Args')[1:] in num:
                                continue
                            elif not pb_args_checker(x, lst):
                                tmp3.append('_')
                if len(tmp3) == 0:
                    tmp3.append('_')
                d['vn-pb'] = tmp3
            else:
                d['vn-pb'] = ['_']


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
    bias_verbClass_mapping = bias_pbTovb_mapping()
    bias_key_lst = list(bias_verbClass_mapping.keys())
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

    if pred in bias_key_lst:
        vbClass = bias_verbClass_mapping.get(pred)
        remove = [k for k in dct if k != vbClass]
        for k in remove:
            del dct[k]
    return dct
