# README #

From Narrative Text to Formal Action Language System Descriptions

### What is this repository for? ###

**Text2DRS** is written in Python3.

* System Text2DRS that takes a narrative text file as an input and produces a discourse representation structure (drs) as an output

### System setup guideline ###

* **Python 3**
* pip3 install dicttoxml
* Download or clone Text2DRS repository
* Download LTH (http://nlp.cs.lth.se/software/semantic-parsing-propbank-nombank-frames/)
* Unzip LTH package and move the package dictionary into Text2DRS repository folder
* Make sure the LTH folder name is "lth_srl"
* Download Standford core-NLP **3.7.0** package (https://stanfordnlp.github.io/CoreNLP/history.html)
* Unzip core-NLP package and move the package dictionary into Text2DRS repository folder

### Parameters ###

* Example system parameters:
* python3 main.py /*your system path to the project repository folder*/text2drs/testFiles/paperExample.txt


### System output ###

* the output file is in the *text2drsOutputs* folder
* input file name: paperExample.txt
* output file name: paperExample.txt
* file contents:
```
  DRS Table
  r1, r2, r3, e1, e2
  ============================================================
  entity r1 entity r2 entity r3

  property ('r1', 'Ann') property ('r2', 'room') property ('r3', 'Michael')

  event e1 event e2

  eventType ('e1', '51.1')
  eventType ('e2', '13.3')

  eventTime ('e1', 0) eventTime ('e2', 1)

  eventArgument ('e1', 'Theme', 'r1') eventArgument ('e1', 'Destination', 'r2')
  eventArgument ('e2', 'Agent', 'r3') eventArgument ('e2', 'Theme', 'r2')
```

### Additional Links ###

* Link to bAbl (https://research.fb.com/downloads/babi/)
* Link to VerbNet (https://verbs.colorado.edu/verb-index/)
* Link to SemLink (https://verbs.colorado.edu/semlink/)

### Contribution guidelines ###

* Writing tests
* Code review

### Who do I talk to? ###

* Gang Ling (gling@unomaha.edu)
* Dr. Yuliya Lierler