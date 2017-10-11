import xml.etree.ElementTree as ET


pb_tree = ET.parse('semLink/vn-pb/vnpbMappings')
m_dct_lst = []

def read_data(lth_output):
    data_lst =[]
    for line in lth_output:
        subline = line.split('\t')
        if(len(subline) < 2):
            continue
        else:
            data_lst.append(subline)

    form_dct(data_lst)

    return m_dct_lst

def form_dct(lst):

    if len(m_dct_lst) > 0:
        del m_dct_lst[:]

    sub_dct_lst = []
    count = 0
    for item in lst:
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

        if int(item[0]) > count:
            sub_dct_lst.append(tmp)
            count += 1
        else:
            count = 0
            m_dct_lst.append(sub_dct_lst)
            sub_dct_lst = []
            sub_dct_lst.append(tmp)


    m_dct_lst.append(sub_dct_lst)
    lookup_pb(m_dct_lst)


def lookup_pb(dct_lst):

    for lst in dct_lst:
        parse_result = {}
        pred = ''
        for sub_dct in lst:
            if sub_dct.get('Pred') != '_' and sub_dct.get('Pred') != None:
                pred = sub_dct.get('Pred')
                plemma = sub_dct.get('PLemma')
                parse_result = vn_pb_parser(pred,plemma)
            else:
                continue

        key_lst = list(parse_result.keys())

        for d in lst:
            if d.get('Pred') == pred:
                tmp2 = []
                for k in key_lst:
                    tmp2.append({'vn': k})
                d['vn-pb'] = tmp2
                # print(d.get('vn-pb'))
            # elif dict.get('Args') != '_':
            #     for key in keylist:
            #         pr_lst = parse_result.get(key)
            #         for d in pr_lst:
            #             k_lst = d.keys()
            #             for k in k_lst:
            #                 if k == dict.get('Args')[1]:

            else:
                d['vn-pb'] = [{'_':'_'}]


def vn_pb_parser(pred, plemma):
    dct = {}
    root = pb_tree.getroot()

    for elem in root.findall('./predicate'):
        if elem.attrib.get('lemma') == plemma:
            for argmap in elem:
                if argmap.attrib.get('pb-roleset') == pred:
                    lst = []
                    for role in argmap:
                        sub_dct2 = {}
                        sub_dct2[role.attrib.get('pb-arg')] = role.attrib.get('vn-theta')
                        lst.append(sub_dct2)
                    dct[argmap.attrib.get('vn-class')] = lst

    return dct

def print_table(m_lst):
    dct_keys = m_lst[0][0].keys()
    for key in dct_keys:
        print("{:10s}\t".format(key), end="")
    for lst in m_lst:
        print('')
        for sub_dct3 in lst:
            print('')
            for key in dct_keys:
                if key == 'vn-pb':
                    for item in sub_dct3.get(key):
                        if 'vn' in item.keys():
                            print('{}; '.format(item.get('vn')), end="")
                        else:
                            print('{:5s}'.format(item.get('_')), end="")
                else:
                    print("{:10s}\t".format(sub_dct3.get(key)), end="")
