# README #

From Narrative Text to Formal Action Language System Descriptions

### What is this repository for? ###

Program the system Text2DRS in Java and python.
To test my system, I will create a corpora consisting of short and interesting narratives from the bAbl Tasks Data (Facebook AI Research,. 2016) and annotate them with respective DRSes.
These narratives will be used to evaluate the quality of my system.

* System Text2DRS that takes a narrative as an input and produces a Neo-Davidsonian style DRS as an output
* Annotated corpora of bAbl narratives
* Evaluation of Text2DRS
* System Text2DRS description

### System components ###

* Download or clone Text2DRS repository
* Download LTH (http://nlp.cs.lth.se/software/semantic-parsing-propbank-nombank-frames/)
* Unzip LTH package and move the package dictionary into Text2DRS repository folder
* Make sure the LTH folder name is "lth_srl"
* Download Standford core-NLP package (https://stanfordnlp.github.io/CoreNLP/index.html#download)
* Unzip core-NLP package and move the package dictionary into Text2DRS repository folder
* Rename the core-NLP folder as "stanford-core-full" (just remove the version number)

### Parameters ###

* main.py (path to input file)

### Additional Links ###

* Link to bAbl (https://research.fb.com/downloads/babi/)
* Link to VerbNet (https://verbs.colorado.edu/verb-index/)
* Link to SemLink (https://verbs.colorado.edu/semlink/)

### Contribution guidelines ###

* Writing tests
* Code review

### Who do I talk to? ###

* Gang Ling
* Dr. Yuliya Lierler