import xml.etree.ElementTree as ET


def main_process(data_dct_lst):
    entities = retrieve_entity(data_dct_lst)
    entities_map = mapping_entity(entities)
    property = retrieve_property(entities_map)
    events_map = retrieve_event(data_dct_lst)
    event_type = retrieve_event_type(data_dct_lst)
    event_time = retrieve_event_time(events_map)

    for e in entities:
        print(e)

    for k,e in entities_map.items():
        print(k,e)

    for p in property:
        print(p)

    for k, e in events_map.items():
        print(k, e)

    for k, et in event_type.items():
        print(k, et)

    for k, t in event_time.items():
        print(k, t)


def retrieve_entity(data_dct_lst):
    entities = []
    for sentences in data_dct_lst:
        temp = []
        for sen in sentences:
            if sen.get('PPOS') == 'NNP' or sen.get('PPOS') == 'NN':
                temp.append(sen.get('Form'))
        entities.append(temp)

    return entities


def mapping_entity(entities):
    entities_dictionary = {}
    count = 1;
    for entity in entities:
        for e in entity:
            entities_dictionary['r'+ str(count)] = e
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


def retrieve_event_type(data_dct_lst):
    event_type_dictionary = {}
    count = 1;
    for sentences in data_dct_lst:
        for sen in sentences:
            if sen.get('PPOS') == 'VBD':
                event_type_dictionary['e' + str(count)] = sen.get('vn-pb')
                count += 1

    return event_type_dictionary


def retrieve_event_time(events_map):
    event_time_dictionary = {}
    count = 0
    for event, value in events_map.items():
        event_time_dictionary[event] = count
        count += 1

    return event_time_dictionary


def retrieve_event_argument(data_dct_lst):
    event_argument_dictionary = {}

