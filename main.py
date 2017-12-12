import os
import sys
import subprocess
import argparse
import verbnetsrl
import drs
import corenlp

# lth output file
output_file = None
# input file name
target_file_name = None


# The method to call and run lth tool with a input file
def process_lth(file):

    # store text2drs tool's path
    text2_drs_path = os.getcwd()

    lth_path = text2_drs_path + '/lth_srl/'

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
    # subprocess.call(cmd,shell=True)

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

    # subprocess.call(cmd2,shell=True)

    # switch back to text2drs dictionary
    os.chdir(text2_drs_path)


def start_corenlp():

    text2_drs_path = os.getcwd()
    corenlp_path = text2_drs_path + '/stanford-corenlp-full/'
    os.chdir(corenlp_path)
    port_num = 9000
    timeout = 15000
    cmd3 = 'java -mx4g -cp "*"' \
           'edu.standford.nlp.pipeline.StanfordCoreNLPServer -port {0} -timeout {1}'.format(port_num, timeout)
    # subprocess.call(cmd3, shell=True)
    os.chdir(text2_drs_path)


# process input file by running corenlp through command line
# output file format can be choose from text, xml, json
def process_corenlp(file):
    text2_drs_path = os.getcwd()
    corenlp_path = text2_drs_path + '/stanford-corenlp-full/'
    os.chdir(corenlp_path)
    output_path = text2_drs_path + '/corenlp_Outputs/'
    output_format = 'xml'
    cmd4 = 'java -cp "*" -Xmx2g edu.stanford.nlp.pipeline.StanfordCoreNLP ' \
           '-annotators tokenize,ssplit,pos,lemma,ner,parse,dcoref ' \
           '-file {0} -outputDirectory {1} -outputFormat {2}'.format(file, output_path, output_format)
    subprocess.call(cmd4, shell=True)
    os.chdir(text2_drs_path)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help='given full path of input file', type=str)
    args = parser.parse_args()
    input_file = args.input
    process_lth(input_file)

    # read lth output file and store in lth_output
    lth_output = None
    try:
        global output_file
        lth_output = open(output_file,'r')
    except IOError as e:
        print('I/O error({0}): {1}'.format(e.errno, e.strerror))
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise

    # pass lth_output to verbNetSRL for further data process
    data_dct_lst = verbnetsrl.read_data(lth_output)

    drs.main_process(data_dct_lst)

    # write verbNetSRL's outputs to a file
    orig_stdout = sys.stdout
    global target_file_name
    f = open('text2drsOutputs/' + target_file_name + '.txt','w')
    sys.stdout = f
    verbnetsrl.print_table(data_dct_lst)
    sys.stdout = orig_stdout
    f.close()

    # process_corenlp(input_file)



if __name__ == '__main__':
    main()

