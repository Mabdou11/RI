import re
from nltk.corpus import stopwords
from nltk import FreqDist as fd
import math
import pickle

"""""""""""""""""""""""""""""""""""""""

	ONLY USE create_indexFile function
	others will take way too much time
>	USE "create_pkls.py" for the rest
	it's much faster
>	you can modify the script if you
	want to dump on a txt file

"""""""""""""""""""""""""""""""""""""""


documents = open("./cacm/cacm.all","r+", encoding="utf-8").read()
stopwords = stopwords.words('english')


def get_doc(number):
	match = re.search(r"\.I ("+str(number)+")\n\.T\n((.|\n)*?)\n\.B", documents)
	if not match:
		return ""
	return match.group(0)
docList= []
i=1
while(get_doc(i)!=""):
	docList.append(get_doc(i))
	i+=1
i=1
def num_docs():
	i=1
	while(get_doc(i)!=""):
		i+=1
	return i-1

N = num_docs()

def get_title(number):
	doc = get_doc(number)
	match = re.search(r".T\n((.|\n)*?)\n\.", doc)
	if not match:
		return ""	
	return match.group(1)

def get_words(number):
	doc = docList[number-1]
	match = re.search(r".W\n((.|\n)*?)\n\.", doc)
	if not match:
		return ""
	return match.group(1)


def fdWords(number):
	title = re.split(" |\.|,|;|/|\?|`|\:|\*|\n|\t|\r|\"|\(|\)|\[|\]|\{|\}|\<|\>|=|\'|\||-",get_title(number))
	words = re.split(" |\.|,|;|/|\?|`|\:|\*|\n|\t|\r|\"|\(|\)|\[|\]|\{|\}|\<|\>|=|\'|\||-",get_words(number))
	title = [t.lower() for t in title if (t.lower() not in stopwords) & (len(t)>0)]
	words = [word.lower() for word in words if (word.lower() not in stopwords) & (len(word)>0)]
	doc = title + words
	return fd(sorted(doc))

def freq_word(word, number):
	return fdWords(number)[word]

def freq_word_all(word):
	sum = 0
	i = 1
	while(get_doc(i)!=""):
		sum+=freq_word(word.lower(),i)
		i+=1
	return sum

def docs_contain(word):
	i = 1
	docs =[]
	while(i<=N):
		if word in [words[0] for words in fdWords(i).items()]:
			docs.append(i)
		i+=1
	return docs


def wdf():#word_doc_freq
	sum = 0
	rev = []
	i = 1
	while(get_doc(i)!=""):
		for w in fdWords(i).items():
			rev.append((w[0],i,w[1]))
		i+=1
	#rev = sorted(rev, key=lambda tup: tup[0])
	return rev

def wdf_dict():#word_doc_freq
	sum = 0
	rev = []
	i = 1
	_dict = {}
	while(get_doc(i)!=""):
		for w in fdWords(i).items():
			_dict["doc"] = i
			_dict["word"] = w[0]
			_dict["freq"] = w[1]

			rev.append(_dict)
		i+=1
	#rev = sorted(rev, key=lambda tup: tup[0])
	return rev


def weighted_wdf():
	
	#word_doc_freq
	#fornmula
	
	N = 1
	i = 1
	rev = []
	#poids(ti, dj)=(freq(ti,dj)/Max(freq(dj))*math.log((N/ni) +1)

	while(get_doc(N)!=""):
 		N+=1
	N-=1
	weighted= open("weighted_reversed_file.txt","w+",  encoding="utf-8")	
	while(get_doc(i)!=""):
		doc = fdWords(i).items()
		maxF =  max([word[1] for word in doc])
		for word in doc:
			ni = len(docs_contain(word[0]))
			freq = word[1]
			weight = (freq/maxF)*(math.log10(N/ni+1)+1)
			weighted.write("("+word[0]+", "+str(i)+") -> "+str(weight)+"\n")
			print("("+word[0]+", "+str(i)+") -> "+str(weight))
			#rev.append((word[0],i,weight))
		i+=1
	#rev = sorted(rev, key=lambda tup: tup[0])
	return print("created weighted reversed file") #rev




def create_indexFile():
	index= open("index_file.txt","w+",  encoding="utf-8")
	pklIndex = open("index_file.pkl", 'wb')
	sum = 0
	i = 1
	dictio = dict()
	while(get_doc(i)!=""):
		dicti = dict()
		index.write(str(i)+" ->\n")
		for w in fdWords(i).items():
			index.write("("+str(w[0])+", "+str(w[1])+")\n")
			dicti[w[0]] = w[1]
		dictio[i] = dicti
		i+=1
	pickle.dump(dictio, pklIndex)	
	index.close
	return "index file created"

create_indexFile()


"""print("----step1.2----")
print (fdWords(123).items())
print (freq_word('compiler',123))
print("\n------------all--------------\n")
print(get_words(123))
print("\n--------------------------\n")
"""

def create_revFile():
	with open("reversed_file.txt","w+",  encoding="utf-8")as w:
		wdf()[0]
		for tup in wdf():
			w.write("("+tup[0]+", "+str(tup[1])+") -> "+str(tup[2])+"\n")
			print("("+tup[0]+", "+str(tup[1])+") -> "+str(tup[2])+"\n")
		w.close()
	return "reversed file created"


def create_weighted_revFile():
	weighted= open("weighted_reversed_file.txt","w+",  encoding="utf-8")
	for tup in weighted_wdf():
		weighted.write("("+tup[0]+", "+str(tup[1])+") -> "+str(tup[2])+"\n")
	weighted.close
	return "created weighted reversed file"
