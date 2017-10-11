import xml.etree.ElementTree as ET


pb_tree = ET.parse('semLink/vn-pb/vnpbMappings')
data_dictlist = []

def read_data(lth_output):
    data_lst =[]
    for line in lth_output:
        subline = line.split('\t')
        if(len(subline) < 2):
            continue
        else:
            data_lst.append(subline)

    form_dict(data_lst)

    return data_dictlist

def form_dict(lst):

    if len(data_dictlist) > 0:
        del data_dictlist[:]

    sub_dictlist = []
    count = 0
    for item in lst:
        dict = {}
        dict.fromkeys(['ID', 'Form', 'PLemma', 'PPOS', 'PHead', 'PDeprel', 'Pred', 'Args','vn-pb'], None)

        dict['ID'] = item[0]
        dict['Form'] = item[1]
        dict['PLemma'] = item[2]
        dict['PPOS'] = item[4]
        dict['PHead'] = item[8]
        dict['PDeprel'] = item[9]
        dict['Pred'] = item[10]
        dict['Args'] = item[11].split('\n')[0]

        if(int(item[0]) > count):
            sub_dictlist.append(dict)
            count += 1
        else:
            count = 0
            data_dictlist.append(sub_dictlist)
            sub_dictlist = []
            sub_dictlist.append(dict)


    data_dictlist.append(sub_dictlist)
    lookup_pb(data_dictlist)


def lookup_pb(dictlist):

    for lst in dictlist:
        for dict in lst:
            if dict.get('Pred') != '_' and dict.get('Pred') != None:
                pred = dict.get('Pred')
                plemma = dict.get('PLemma')
                parse_result = vn_pb_parser(pred,plemma)
            else:
                continue

def vn_pb_parser(pred, plemma):
    dict = {}
    root = pb_tree.getroot()

    for elem in root.findall('./predicate'):
        if elem.attrib.get('lemma') == plemma:
            for argmap in elem:
                if argmap.attrib.get('pb-roleset') == pred:
                    lst = []
                    for role in argmap:
                        sub_dict = {}
                        sub_dict[role.attrib.get('pb-arg')] = role.attrib.get('vn-theta')
                        lst.append(sub_dict)
                    dict[argmap.attrib.get('vn-class')] = lst

    return dict

def print_table(master_list):
    dict_keys = master_list[0][0].keys()
    for key in dict_keys:
        print("{:10s}\t".format(key), end="")
    for lst in master_list:
        print('')
        for sub_dict in lst:
            print('')
            for key in dict_keys:
                print("{:10s}\t".format(sub_dict.get(key)), end="")
