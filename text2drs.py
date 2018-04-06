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

import os
import sys
import subprocess
import argparse
import verbnetsrl
import drs
import xml.etree.ElementTree as ET
import corenlp
import drs2
import fileGenerator
import configparser

# lth output file
output_file = None
# input file name
target_file_name = None


# The method to call and run lth tool with a input file
def process_lth(file, lth_path):

    # store text2drs tool's path
    text2_drs_path = os.getcwd()

    # switch current dictionary to lth folder
    os.chdir(lth_path)

    # below is pre-process input file and generate token outputs in lth
    model = 'models/penn_00_18_split_dict.model'
    dct = 'v_n_a.txt'
    mem ='100M'
    cp ='jars/lthsrl.jar:jars/utilities.jar:jars/trove.jar:jars/seqlabeler.jar'

    # setup input and output files' paths
    global target_file_name
    target_file_name = file.split('/')[-1].split('.')[0]
    target_file = '<' + file + '>'
    output_tokens = text2_drs_path + '/lthOutputs/' + target_file_name +'.tokens'
    input_tokens = '<' + output_tokens + '>'
    global output_file
    output_file = text2_drs_path + '/lthOutputs/' + 'lth_'+ target_file_name + '.txt'

    cmd = 'java -Xmx{0} -cp {1} se.lth.cs.nlp.depsrl.Preprocessor -allLTH {2} {3} {4} {5}'.format(mem,cp,model,dct,
                                                                                                  target_file,
                                                                                                  output_tokens)

    # call and run lth's token processor
    subprocess.call(cmd,shell=True)

    # below is setting up system variables of lth tool in fully function mode
    synmodel = 'models/train_at_pp_more2nd.model'
    LM = 'models/lm_080602_uknpreds.model'
    GM_CD = 'models/global_partcq_mc_cd_2o_ukp.model'
    GM_CL = 'models/part12345_cq_mc_2o_ukp.sv.model'
    CP= 'jars/lthsrl.jar:jars/utilities.jar:jars/trove.jar'
    MEM= '2600M'
    NSYN = '4'
    NSEM = '4'
    SYNW = '25'
    GMW = '3'
    FORCE_VARGS = 'false'

    cmd2 = 'java -Xmx{0} -cp {1} se.lth.cs.nlp.depsrl.Main -runFull ' \
           '{2} {3} {4} {5} pb_frames nb_frames {6} {7} {8} {9} ' \
           'false false ' \
           '{10} {11} {12}'.format(MEM,CP,LM,GM_CD,GM_CL,synmodel,NSYN,
                                   NSEM,SYNW,GMW,FORCE_VARGS,input_tokens,output_file)

    subprocess.call(cmd2,shell=True)

    # switch back to text2drs dictionary
    os.chdir(text2_drs_path)


# process input file by running corenlp through command line
# output file format can be choose from text, xml, json
def process_corenlp(file, corenlp_path):
    text2_drs_path = os.getcwd()
    os.chdir(corenlp_path)
    output_path = text2_drs_path + '/corenlp_Outputs/'
    output_format = 'xml'
    cmd3 = 'java -Xmx5g -cp stanford-corenlp-3.7.0.jar:stanford-corenlp-models-3.7.0.jar:* '\
           'edu.stanford.nlp.pipeline.StanfordCoreNLP -annotators '\
           'tokenize,ssplit,pos,lemma,ner,parse,mention,coref -coref.algorithm neural '\
           '-file {0} -outputDirectory {1} -outputFormat {2}'.format(file, output_path, output_format)

    subprocess.call(cmd3, shell=True)
    file_name = file.split("/")[-1]
    corenlp_output_path = output_path + file_name + ".xml"
    os.chdir(text2_drs_path)
    return corenlp_output_path


def main():
    config = configparser.RawConfigParser()

    parser = argparse.ArgumentParser()
    parser.add_argument("config", help='given full path of config file', type=str)
    parser.add_argument("input", help='given full path of input file', type=str)
    args = parser.parse_args()

    if os.path.isfile(args.config):
        config.read(args.config)
    else:
        print('Could not find CONFIG file')
        sys.exit()

    if os.path.isfile(args.input):
        input_file = args.input
    else:
        print("Could not find the txt file")
        sys.exit()

    lth_path = config.get("LTH", "Path")
    if os.path.exists(lth_path):
        pass
    else:
        print('LTH path is invalid')
        sys.exit()

    corenlp_path = config.get('CoreNLP', 'Path')
    if os.path.exists(corenlp_path):
        pass
    else:
        print('Core-NLP path invalid')
        sys.exit()

    process_lth(input_file, lth_path)
    # read lth output file and store in lth_output
    lth_output = None
    try:
        global output_file
        lth_output = open(output_file,'r')
    except IOError as e:
        print(f"I/O error({e.errno}): {e.strerror}")
    except:
        print('Unexpected error:', sys.exc_info()[0])
        raise

    # pass lth_output to verbNetSRL for further data process
    data_dct_lst = verbnetsrl.read_data(lth_output)

    # write verbNetSRL's outputs to a file
    orig_stdout = sys.stdout
    global target_file_name
    f = open('text2drsOutputs/' + target_file_name + '_verbNetsrl.txt','w')
    sys.stdout = f
    fileGenerator.print_table(data_dct_lst)
    sys.stdout = orig_stdout
    f.close()

    corenlp_output_path = process_corenlp(input_file, corenlp_path)
    corenlp_output = None
    try:
        corenlp_output = ET.parse(corenlp_output_path)
    except IOError as e:
        print('I/O error({0}: {1}'.format(e.errno, e.strerror))
    except:
        print('Unexpected error:', sys.exc_info()[0])
        raise

    coref_dictionary = corenlp.prcoess_xml(corenlp_output)

    # drs_dict = drs.main_process(data_dct_lst)
    drs_dict = drs2.drs_generator(data_dct_lst, coref_dictionary)

    orig_stdout = sys.stdout
    # global target_file_name
    f = open('text2drsOutputs/' + target_file_name + '_drs.txt','w')
    sys.stdout = f
    fileGenerator.drs_to_asp(drs_dict)
    sys.stdout = orig_stdout
    f.close()


if __name__ == "__main__":
    main()

