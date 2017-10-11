import os
import sys
import subprocess
import argparse
import verbNetSRL

output_file = ''
target_file_name = ''

def process_lth(file):

    text2DRS = os.getcwd()

    #lth ='/home/gangling/Documents/ALM/lth_srl/'
    # lth = '/Users/gling/Documents/ALM/lth_srl/'
    lth = text2DRS + '/lth_srl/'

    os.chdir(lth)

    model = 'models/penn_00_18_split_dict.model'

    dct = 'v_n_a.txt'

    mem ='100M'

    cp ='jars/lthsrl.jar:jars/utilities.jar:jars/trove.jar:jars/seqlabeler.jar'


    global target_file_name
    target_file_name = file.split('/')[-1].split('.')[0]
    target_file = '<' + file + '>'
    output_tokens = text2DRS + '/lthOutputs/' + target_file_name +'.tokens'
    input_tokens = '<' + output_tokens + '>'
    global output_file
    output_file = text2DRS + '/lthOutputs/' + 'lth_'+ target_file_name + '.txt'


    cmd = 'java -Xmx{0} -cp {1} se.lth.cs.nlp.depsrl.Preprocessor -allLTH {2} {3} {4} {5}'.format(mem,cp,model,dct,target_file,output_tokens)

    # subprocess.call(cmd,shell=True)

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

    # subprocess.call(cmd2,shell=True)

    os.chdir(text2DRS)

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("input", help='given full path of input file', type=str)
    args = parser.parse_args()
    process_lth(args.input)

    try:
        lth_output = open(output_file,'r')
    except IOError as e:
        print ('I/O error({0}): {1}'.format(e.errno, e.strerror))
    except:
        print ("Unexpected error:", sys.exc_info()[0])
        raise

    data_dct_lst = verbNetSRL.read_data(lth_output)

    orig_stdout = sys.stdout
    f = open('text2drsOutputs/' + target_file_name + '.txt','w')
    sys.stdout = f
    verbNetSRL.print_table(data_dct_lst)
    sys.stdout = orig_stdout
    f.close()



if __name__ == '__main__':
    main()

