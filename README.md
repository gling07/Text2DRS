# README #

From Narrative Text to Formal Action Language System Descriptions

### What is this repository for? ###

**Text2DRS** is written in Python3.

* System Text2DRS that takes a narrative text file as an input and produces a discourse representation structure (drs) as an output

### System setup guideline ###

* **Python 3.6** Note that the version of python is *ESSENTIAL*
* pip3 install dicttoxml  (tested with version 1.7.4)
* Download or clone Text2DRS repository
* Download LTH (http://nlp.cs.lth.se/software/semantic-parsing-propbank-nombank-frames/)
* Unzip LTH package and move the package dictionary into Text2DRS repository folder
* Download Standford core-NLP **3.7.0** package (https://stanfordnlp.github.io/CoreNLP/history.html)
* Unzip core-NLP package and move the package dictionary into Text2DRS repository folder

* create a file named CONFIG that includes two lines  specifying the place for LTH and core-NLP packages as follows

lth_srl  <path-to-lth-directory>/lth_srl/
corenlp  <path-to-corenlp-directory>/stanford-corenlp-full-2016-10-31/
   

### Parameters ###

* Command line to invoke the system:
* python3 text2drs.py <path-to-config-file>/CONFIG <path-to-input-file-with-text>/something.txt

For example, testFiles/paperExample.txt contains two sentences 
  Ann went to the room.
  Michael left the room.

If this file is an input file of text2drs.py then the output will be placed into 
*text2drsOutputs* folder under the name paperExample_drs.txt (See below)

### System output ###

* the output file is in the *text2drsOutputs* folder
* input file name: paperExample.txt

* drs output file name: paperExample_drs.txt
* verbnet srl output file name: paperExample_verbNetsrl.txt

* drs file contents:
```
% r1, r2, r3, e1, e2
% ============================================================

entity(r1). entity(r2). entity(r3).

property(r1, "Ann"). property(r2, "room"). property(r3, "Michael").

event(e1).
event(e2).

eventType(e1, "51.1"). eventType(e2, "13.3").

eventTime(e1, 0). eventTime(e2, 1).

eventArgument(e1, "Theme", r1). eventArgument(e1, "Destination", r2). eventArgument(e2, "Agent", r3).
eventArgument(e2, "Theme", r2).
```

### Additional Links ###

* Link to bAbl (https://research.fb.com/downloads/babi/)
* Link to VerbNet (https://verbs.colorado.edu/verb-index/)
* Link to SemLink (https://verbs.colorado.edu/semlink/)


### Who do I talk to? ###

* Gang Ling (gling@unomaha.edu)
* Dr. Yuliya Lierler (ylierler@unomaha.edu)
