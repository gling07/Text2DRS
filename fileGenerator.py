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


# print drs in asp format


def drs_to_asp(drs_dict):
    print('%', end=' ')
    print(', '.join(drs_dict['entity']), end=', ')
    print(', '.join(drs_dict['event']))

    print('%', end=' ')
    print('=='*30)
    count = 0
    key_list = [k for k in drs_dict.keys()]
    for key in key_list:
        items = drs_dict[key]
        if key == 'entity' or key == 'event':
            print('\n')
            for i in items:
                print(key, end='')
                print('(', end='')
                print(i, end='')
                print(').', end=' ')
                count += 1
                if count == 4:
                    print()
                    count = 0
        elif key == 'eventArgument':
            print('\n')
            count = 0
            for (e, t, r) in items:
                print(key, end='')
                print('(', end='')
                print(e, end=', ')
                print('\"' + t + '\"', end=', ')
                print(r, end='')
                print(').', end=' ')
                count += 1
                if count == 3:
                    print()
                    count = 0
        elif key == 'eventTime':
            print('\n')
            count = 0
            for (e, t) in items:
                print(key, end='')
                print('(', end='')
                print(e, end=', ')
                print(t, end='')
                print(').', end=' ')
                count += 1
                if count == 5:
                    print()
                    count = 0
        else:
            print('\n')
            count = 0
            for (e, v) in items:
                print(key, end='')
                print('(', end='')
                print(e, end=', ')
                print('\"' + v + '\"', end='')
                print(').', end=' ')
                count += 1
                if count == 4:
                    print()
                    count = 0

# print verbnet srl table
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

