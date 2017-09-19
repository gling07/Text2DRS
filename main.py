import subprocess

lth ='/home/gangling/Documents/ALM/lth_srl/'

model = lth + 'models/penn_00_18_split_dict.model'

dict =lth + 'v_n_a.txt'

mem ='100M'

cp ='{0}jars/lthsrl.jar:' \
    '{1}jars/utilities.jar:' \
    '{2}jars/trove.jar:' \
    '{3}jars/seqlabeler.jar'.format(lth,lth,lth,lth)

targetFile = '<' + lth + 'TestPool/SingleSupportingFact.txt>'
outputFile = lth + 'TestOutput/test.tokens'


cmd = 'java -Xmx{0} -cp {1} se.lth.cs.nlp.depsrl.Preprocessor -allLTH {2} {3} {4} {5}'.format(mem,cp,model,dict,targetFile,outputFile)

subprocess.call(cmd,shell=True)

