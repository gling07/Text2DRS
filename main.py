import os
import sys
import subprocess
import argparse
import verbNetSRL

# lth output file
output_file = ''
# input file name
target_file_name = ''


# The method to call and run lth tool with a input file
def process_lth(file):

    # store text2drs tool's path
    text2DRS = os.getcwd()

    lth = text2DRS + '/lth_srl/'

    # switch current dictionary to lth folder
    os.chdir(lth)

    # below is pre-process input file and generate token outputs in lth
    model = 'models/penn_00_18_split_dict.model'
    dct = 'v_n_a.txt'
    mem ='100M'
    cp ='jars/lthsrl.jar:jars/utilities.jar:jars/trove.jar:jars/seqlabeler.jar'

    # setup input and output files' paths
    global target_file_name
    target_file_name = file.split('/')[-1].split('.')[0]
    target_file = '<' + file + '>'
    output_tokens = text2DRS + '/lthOutputs/' + target_file_name +'.tokens'
    input_tokens = '<' + output_tokens + '>'
    global output_file
    output_file = text2DRS + '/lthOutputs/' + 'lth_'+ target_file_name + '.txt'

    cmd = 'java -Xmx{0} -cp {1} se.lth.cs.nlp.depsrl.Preprocessor -allLTH {2} {3} {4} {5}'.format(mem,cp,model,dct,target_file,output_tokens)

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
           '{10} {11} {12}'.format(MEM,CP,LM,GM_CD,GM_CL,synmodel,NSYN,NSEM,SYNW,GMW,FORCE_VARGS,input_tokens,output_file)

    subprocess.call(cmd2,shell=True)

    # switch back to text2drs dictionary
    os.chdir(text2DRS)


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("input", help='given full path of input file', type=str)
    args = parser.parse_args()
    process_lth(args.input)

    # read lth output file and store in lth_output
    lth_output = None
    try:
        lth_output = open(output_file,'r')
    except IOError as e:
        print('I/O error({0}): {1}'.format(e.errno, e.strerror))
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise

    # pass lth_output to verbNetSRL for further data process
    data_dct_lst = verbNetSRL.read_data(lth_output)

    # write verbNetSRL's outputs to a file
    orig_stdout = sys.stdout
    f = open('text2drsOutputs/' + target_file_name + '.txt','w')
    sys.stdout = f
    verbNetSRL.print_table(data_dct_lst)
    sys.stdout = orig_stdout
    f.close()


if __name__ == '__main__':
    main()

