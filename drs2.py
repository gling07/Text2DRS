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
import pprint
drs_dict = dict()
verb_pos = ['VBD', 'VB', 'VBN', 'VBG', 'VBP']
noun_lst = ['NNP', 'NN', 'PRP', 'NNS']


def drs_generator(data_dct_lst, coref_dictionary):

    omit_list = get_omit_entities(coref_dictionary)
    entities = get_all_entities(data_dct_lst, omit_list)
    entities_map = mapping_entity(entities)
    property = retrieve_property(entities_map)
    (events_map, event_property) = retrieve_event(data_dct_lst)
    event_type = retrieve_event_type(data_dct_lst)
    event_time = retrieve_event_time(events_map)
    event_argument = retrieve_event_argument(data_dct_lst, property, event_type, event_property)

    drs_dict['entity'] = [k for k in entities_map.keys()]
    drs_dict['property'] = property
    drs_dict['event'] = [k for k in events_map.keys()]
    drs_dict['eventType'] = event_type
    drs_dict['eventTime'] = event_time
    drs_dict['eventArgument'] = event_argument

    return drs_dict


def get_omit_entities(coref_dictionary):
    special = "'"+'s'
    omit_list = list()
    for key, value in coref_dictionary.items():
        if ' ' in key and special not in key:
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
    for sentences in data_dct_lst:
        num += 1
        for sen in sentences:
            if sen.get('PPOS') in noun_lst:
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
    events_property = dict()
    count = 1
    sentence_id = 1
    for sentences in data_dct_lst:
        verb = list()
        for sen in sentences:
            if sen.get('Pred') != '_' and sen.get('PPOS') in verb_pos:
                events_dictionary['e' + str(count)] = sen.get('PLemma')
                verb.append((sen.get('PLemma'), 'e' + str(count)))
                count += 1
        events_property[sentence_id] = verb
        sentence_id += 1
    return (events_dictionary, events_property)


# include picking first vn-class if multiple returns
def retrieve_event_type(data_dct_lst):
    event_type_dictionary = dict()
    count = 1
    for sentence in data_dct_lst:
        for item in sentence:
            if item.get('PPOS') in verb_pos:
                pred = item.get('Pred')
                if item.get(pred + ':vb-class') is not None:
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


def retrieve_event_argument(data_dct_lst, property, event_type, event_property):
    event_argument_list = list()
    sentence_id = 1
    for sentence in data_dct_lst:
        predicates = verbnetsrl.get_predicates(sentence)
        events = event_type[0:len(predicates)]
        event_type = event_type[len(predicates):]
        for (pred, event) in zip(predicates, events):
            event_ref = event[0]
            for sent in sentence:
                if sent.get('Args:' + pred) != '_':
                    # use first verb class as vn class
                    vn_role = sent.get(pred + ':vn-class')[0][1]
                    if sent.get('PPOS') in noun_lst:
                        for (ref, ent) in property:
                            if ent == sent.get('Form'):
                                event_argument_list.append((event_ref, vn_role, ref))
                                break
                    elif sent.get('PPOS') in verb_pos:
                        verb_property = event_property.get(sentence_id)
                        for (plemma, eref) in verb_property:
                            if sent.get('PLemma') == plemma:
                                event_argument_list.append((event_ref, vn_role, eref))

        sentence_id += 1

    return event_argument_list
