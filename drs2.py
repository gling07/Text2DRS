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

import verbnetsrl
drs_dict = dict()


def drs_generator(data_dct_lst, coref_dictionary):

    omit_list = get_omit_entities(coref_dictionary)
    entities = get_all_entities(data_dct_lst, omit_list)
    entities_map = mapping_entity(entities)
    property = retrieve_property(entities_map)
    events_map = retrieve_event(data_dct_lst)
    event_type = retrieve_event_type(data_dct_lst)
    event_time = retrieve_event_time(events_map)
    event_argument = retrieve_event_argument(data_dct_lst, property, event_type)

    drs_dict['entity'] = [k for k in entities_map.keys()]
    drs_dict['property'] = property
    drs_dict['event'] = [k for k in events_map.keys()]
    drs_dict['eventType'] = event_type
    drs_dict['eventTime'] = event_time
    drs_dict['eventArgument'] = event_argument

    return drs_dict


def get_omit_entities(coref_dictionary):

    omit_list = list()
    for key, value in coref_dictionary.items():
        if ' ' in key:
            entity = key.split(' ')[-1]
            for v in value[1:]:
                omit_list.append((entity, v))
        else:
            for v in value[1:]:
                omit_list.append((key, v))
    return omit_list


def get_all_entities(data_dct_lst, omit_list):
    entities = list()
    num = 0
    noun = ['PPOS', 'NN', 'PRP']
    for sentences in data_dct_lst:
        num += 1
        for sen in sentences:
            if sen.get('PPOS') in noun:
                tmp = (sen.get('Form'), num)
                if tmp not in omit_list:
                    entities.append(sen.get('Form'))

    return entities


def mapping_entity(entities):
    entities_dictionary = dict()
    count = 1
    for entity in entities:
        entities_dictionary['r'+ str(count)] = entity
        count += 1

    return entities_dictionary


def retrieve_property(entities_map):
    properties = list()
    for key, entity in entities_map.items():
        temp = (key, entity)
        properties.append(temp)

    return properties


def retrieve_event(data_dct_lst):
    events_dictionary = dict()
    count = 1
    for sentences in data_dct_lst:
        for sen in sentences:
            if sen.get('PPOS') == 'VBD' or sen.get('PPOS') == 'VB':
                events_dictionary['e' + str(count)] = sen.get('PLemma')
                count += 1

    return events_dictionary


# include picking first vn-class if multiple returns
def retrieve_event_type(data_dct_lst):
    ppos = ['VBD', 'VB']
    pdeprel = ['ROOT', 'CONJ']
    event_type_dictionary = dict()
    count = 1
    for sentence in data_dct_lst:
        for item in sentence:
            if item.get('PPOS') in ppos and item.get('PDeprel') in pdeprel:
                pred = item.get('Pred')
                event_type_dictionary['e' + str(count)] = item.get(pred + ':vb-class')[0]
                count += 1

    event_type_list = [(k, v) for k, v in event_type_dictionary.items()]
    return event_type_list


def retrieve_event_time(events_map):
    event_time_dictionary = dict()
    count = 0
    for event, value in events_map.items():
        event_time_dictionary[event] = count
        count += 1

    event_time_list = [(k, v) for k, v in event_time_dictionary.items()]
    return event_time_list


def retrieve_event_argument(data_dct_lst, property, event_type):

    event_argument_list = list()
    event_argument_dict = dict()
    index = 1
    for event, sentence in zip(event_type, data_dct_lst):
        arguments_list = list()
        args_to_vn = list()
        event_ref = event[0]
        for sent in sentence:
            if sent.get('Args') != '_' and sent.get('vn-pb')[0] != '_':
                # use first verb class as vn class
                vn_role = sent.get('vn-pb')[0][1]
                args_to_vn.append(vn_role)

        sub_index = 0
        for item in sentence:
            tmp = list()
            if item.get('PPOS') == 'NNP' or item.get('PPOS') == 'NN':
                tmp.append(event_ref)
                print(args_to_vn[sub_index])
                tmp.append(args_to_vn[sub_index])
                sub_index += 1
                entity = item.get('Form')
                for (ref, ent) in property:
                    if entity == ent:
                        tmp.append(ref)
                        break
                arguments_list.append(tmp)
        event_argument_dict[index] = arguments_list
        index += 1

    for value in event_argument_dict.values():
        for v in value:
            event_argument_list.append(v)

    return event_argument_list
