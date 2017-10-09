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

    print (data_lst)