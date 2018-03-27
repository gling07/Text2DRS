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

drs_dict = dict()

def main_process(data_dct_lst, coref_dictionary):
    entities = retrieve_entity(data_dct_lst)
    entities_map = mapping_entity(entities)
    property = retrieve_property(entities_map)
    events_map = retrieve_event(data_dct_lst)
    event_type = retrieve_event_type(data_dct_lst)
    event_time = retrieve_event_time(events_map)
    event_argument = retrieve_event_argument(data_dct_lst, property, event_type)

    # drs_dict = dict()
    drs_dict['entity'] = [k for k in entities_map.keys()]
    drs_dict['property'] = property
    drs_dict['event'] = [k for k in events_map.keys()]
    drs_dict['eventType'] = event_type
    drs_dict['eventTime'] = event_time
    drs_dict['eventArgument'] = event_argument

    # print('drs dict:')
    # for k, v in drs_dict.items():
    #     print(k, v)


def retrieve_entity(data_dct_lst):
    entities = []
    for sentences in data_dct_lst:
        temp = []
        for sen in sentences:
            if sen.get('PPOS') == 'NNP' or sen.get('PPOS') == 'NN':
                temp.append(sen.get('Form'))
        for entity in temp:
            if entity not in entities:
                entities.append(entity)

    return entities


def mapping_entity(entities):
    entities_dictionary = {}
    count = 1;
    for entity in entities:
        entities_dictionary['r'+ str(count)] = entity
        count += 1

    return entities_dictionary


def retrieve_property(entities_map):
    properties = []
    for key, entity in entities_map.items():
        temp = (key, entity)
        properties.append(temp)

    return properties


def retrieve_event(data_dct_lst):
    events_dictionary = {}
    count = 1;
    for sentences in data_dct_lst:
        for sen in sentences:
            if sen.get('PPOS') == 'VBD':
                events_dictionary['e' + str(count)] = sen.get('PLemma')
                count += 1

    return events_dictionary


# include picking first vn-class if multiple returns
def retrieve_event_type(data_dct_lst):
    event_type_dictionary = dict()
    count = 1;
    for sentence in data_dct_lst:
        for item in sentence:
            if item.get('PPOS') == 'VBD':
                event_type_dictionary['e' + str(count)] = item.get('vn-pb')[0]['vn']
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


def retrieve_event_argument(data_dct_lst, property, eventType):
    event_argument_list = list()
    sentence_property = list()
    sentence_rolesets = list()
    for et, sentence in zip(eventType, data_dct_lst):
        vn = et[1]
        for item in sentence:
            tmp = list()
            if item.get('PPOS') == 'NNP' or item.get('PPOS') == 'NN':
                sentence_property.append(item.get('Form'))
            tmp += item.get('vn-pb')
            for i in tmp:
                k_list = [k for k in i.keys()]
                for k in k_list:
                    if k == vn:
                        sentence_rolesets.append(i[k])

    index = 0
    count = 0
    for p, r in zip(sentence_property, sentence_rolesets):
        entity = ''
        for i in property:
            if i[1] == p:
                entity = i[0]
        event_argument_list.append((eventType[index][0], r, entity))
        count += 1
        if count == 2:
            index += 1
            count = 0

    return event_argument_list


def print_drs():
    print('DRS Table')
    print(', '.join(drs_dict['entity']), end=', ')
    print(', '.join(drs_dict['event']))
    print('=='*30)
    count = 0
    keys = [k for k in drs_dict.keys()]
    for k in keys:
        l = drs_dict[k]
        for i in l:
            print(k, end=' ')
            print(i, end=' ')
            count += 1
            if count == 3:
                print('')
                count = 0

        print('\n')
