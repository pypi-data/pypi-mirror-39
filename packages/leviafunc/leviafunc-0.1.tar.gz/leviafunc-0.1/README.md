```sh
Leviafunc(legal_acts):
    return work_of_Leviathan
```
# NLP of legal texts
Analysis of agreements between governments

* Key words & key phrases extraction with TF-IDF and N-gramms
* NER for DATES with (Natasha (rule-based lib for Russian language). 
Sequence model, implemented in AnaGo and NER by DeepMIPT both have lower accuracy for this type of documents.
* Dictionary method with morphological analysis for finding ORGANIZATIONS and COUNTRIES 

### use as a module
```sh
$ pip install leviafunc
```
use cases are described in example.py

### or run as a script
```sh
$ git clone https://github.com/alissiawells/Leviafunc.git
$ cd Leviafunc
$ mkvirtualenv Leviafunc
$ pip install -r requirements.txt
$ python leviafunc.py input.txt [-f / output.txt] [-c yourcorpus.txt]
```
run without [additional options] for console output with initial corpus ('corpus.txt')

### tests:
```sh
python setup.py test
```

### for experiments, it is more conveient to use jupyter notebook
```sh
$ jupyter notebook
```
open on localhost 'Analysis.ipynb'


![](https://github.com/alissiawells/Leviafunc/blob/master/Leviathan.jpg)
