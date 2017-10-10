import xml.etree.ElementTree as ET

pb_tree = ET.parse('semLink/vn-pb/vnpbMappings')

def read_data(lth_output):
    data_lst =[]
    for line in lth_output:
        subline = line.split('\t')
        if(len(subline) < 2):
            continue
        else:
            data_lst.append(subline)

    form_dict(data_lst)


def form_dict(lst):

    data_dictlist = []

    for item in lst:
        dict = {}
        dict.fromkeys(['ID', 'Form', 'PLemma', 'PPOS', 'PHead', 'PDeprel', 'Pred', 'Args'], None)

        dict['ID'] = item[0]
        dict['Form'] = item[1]
        dict['PLemma'] = item[2]
        dict['PPOS'] = item[4]
        dict['PHead'] = item[8]
        dict['PDeprel'] = item[9]
        dict['Pred'] = item[10]
        dict['Args'] = item[11].split('\n')[0]

        data_dictlist.append(dict)

    lookup_pb(data_dictlist)


    for item in data_dictlist:
        print (item)


def lookup_pb(dictlist):

    for dict in dictlist:
        if dict.get('Pred') != '_' and dict.get('Pred') != None:
            pred = dict.get('Pred')
            plemma = dict.get('PLemma')
            vn_pb_parser(pred,plemma)
            # print (pred,plemma)
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

    for item in dict.items():
        print (item)

