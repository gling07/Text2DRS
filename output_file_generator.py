def print_drs(drs_dict):
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
                            print('{};'.format(item.get('vn')), end="")
                        elif '_' not in item.keys():
                            for k,v in item.items():
                                print('{}:{};'.format(k,v), end="")
                        else:
                            print('{:5s}'.format(item.get('_')), end="")
                else:
                    print("{:10s}\t".format(sub_dct3.get(key)), end="")

