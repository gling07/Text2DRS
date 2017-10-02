import subprocess
import os

Text2DRS = os.getcwd()

#lth ='/home/gangling/Documents/ALM/lth_srl/'
lth = '/Users/gling/Documents/ALM/lth_srl/'

os.chdir(lth)

model = 'models/penn_00_18_split_dict.model'

dict = 'v_n_a.txt'

mem ='100M'

cp ='jars/lthsrl.jar:jars/utilities.jar:jars/trove.jar:jars/seqlabeler.jar'

targetFile = '<TestPool/SingleSupportingFact.txt>'
outputTokens = 'TestOutput/SingleSupportingFact.tokens'
inputTokens = '<' + outputTokens + '>'
outputFile = Text2DRS + '/lthOutputs/SingleSupportingFact.txt'


cmd = 'java -Xmx{0} -cp {1} se.lth.cs.nlp.depsrl.Preprocessor -allLTH {2} {3} {4} {5}'.format(mem,cp,model,dict,targetFile,outputTokens)

subprocess.call(cmd,shell=True)

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
       '{10} {11} {12}'.format(MEM,CP,LM,GM_CD,GM_CL,synmodel,NSYN,NSEM,SYNW,GMW,FORCE_VARGS,inputTokens,outputFile)

subprocess.call(cmd2,shell=True)

os.chdir(Text2DRS)

