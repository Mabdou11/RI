import re
from nltk.corpus import stopwords
from nltk import FreqDist as fd
# step 1:

documents = open("./cacm/cacm.all","r+", encoding="utf-8").read()
stopwords = stopwords.words('english')

def get_doc(number):
	match = re.search(r"\.I ("+str(number)+")\n\.T\n((.|\n)*?)\n\.B", documents)
	if not match:
		return ""
	return match.group(0)

def get_title(number):
	doc = get_doc(number)
	match = re.search(r".T\n((.|\n)*?)\n\.", doc)
	if not match:
		return ""	
	return match.group(1)

def get_words(number):
	doc = get_doc(number)
	match = re.search(r".W\n((.|\n)*?)\n\.", doc)
	if not match:
		return ""
	return match.group(1)


def fdWords(number):
	title = re.split(" |\.|,|;|/|\?|`|\:|\*|\n|\t|\r|\"|\(|\)|\[|\]|\{|\}|\<|\>|=|\'|\|",get_title(number))
	words = re.split(" |\.|,|;|/|\?|`|\:|\*|\n|\t|\r|\"|\(|\)|\[|\]|\{|\}|\<|\>|=|\'|\|",get_words(number))
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

def wdf():#word_doc_freq
	sum = 0
	i = 1
	rev = []
	while(get_doc(i)!=""):
		for w in fdWords(i).items():
			rev.append((w[0],i,w[1]))
		i+=1
	#rev = sorted(rev, key=lambda tup: tup[0])
	return rev


def create_indexFile():
	index= open("index_file.txt","w+",  encoding="utf-8")
	sum = 0
	i = 1
	while(get_doc(i)!=""):
		index.write(str(i)+" ->\n")
		for w in fdWords(i).items():
			index.write("("+str(w[0])+", "+str(w[1])+")\n")
		i+=1

	index.close
	return "index file created"



def create_revFile():
	with open("reversed_file.txt","w+",  encoding="utf-8")as w:
		wdf()[0]
		for tup in wdf():
			w.write("("+tup[0]+", "+str(tup[1])+") -> "+str(tup[2])+"\n")
		w.close()
	return "reversed file created"



def booleanModel(terms):

	terms = terms.split()
	r= open("index_file.txt","r+",  encoding="utf-8")
	doc = r.readlines()
	pertinent_docs = []
	i =0
	while i < len(doc):
		and_terms = terms
		d = re.search(r"([0-9]+) ->\n", doc[i] )
		if not d:
			i+=1
		else :
			d = d.group(1)
			i+=1
			temp_doc = []

			while(i < len(doc) and not re.search(r"[0-9]+ ->\n", doc[i])):
				word = re.search(r"\((.*?), ([0-9]+)\)", doc[i])
				temp_doc.append(word.group(1))
				i+=1
				
			if(any(elem in temp_doc for elem in and_terms)):
				pertinent_docs.append(d)
	r.close
	return pertinent_docs


#print(create_indexFile())


print(booleanModel('algebraic'))


