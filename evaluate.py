import pickle 
import time
import math
import string
from nltk.corpus import stopwords
from vectorial import *
start = time.time()

f =  open('./pkl/index_file.pkl', 'rb')
index = pickle.load(f)
f =  open('./pkl/reversed_file.pkl', 'rb')
rev = pickle.load(f)
f =  open('./pkl/weighted_reversed_file.pkl', 'rb')
weighted = pickle.load(f)

def req_docs(file_name):
	file=open(file_name,"r",encoding="utf-8").readlines()
	i=0
	dic=dict()
	while i < len(file):
		line_i=file[i].split()
		docs=[]
		count=0
		j=i
		exit=0
		while (j < len(file) and not exit):
			line_j=file[j].split()
			j+=1
			if line_i[0]==line_j[0]:
				docs.append(line_j[1])
				count+=1
			else:
				exit=1
		i+=count
		dic[int(line_i[0])]=docs
	output = open('./pkl/relevant_docs.pkl', 'wb')
	pickle.dump(dic, output)
	output.close()
	return dic


def index_req(file_name):
	lines = open(file_name,"r",encoding="utf-8").readlines()
	dic=dict()
	docList=[]
	for i in range(0,len(lines)):
		document=""
		if lines[i].startswith(".I"):
			i+=1
			while  i<len(lines) and not lines[i].startswith(".I"):
				if i<len(lines) and lines[i].startswith(".W"):
					i+=1
					while i<len(lines) and not (lines[i].startswith(".I") or lines[i].startswith(".A") or lines[i].startswith(".N")):
						document+=lines[i]
						i+=1
				i+=1
			docList.append(document)
	stopWords = stopwords.words('english')
	punctuation=string.punctuation
	qList=[]
	for doc in docList:
		noPunct=""
		for c in doc:
			if c not in punctuation:
				noPunct+=c
			else :
				noPunct+=" "
		currentDoc=""
		for word in noPunct.split():
			if word.lower() not in stopWords:
				currentDoc+=" "+word.lower()
		qList.append(currentDoc)
	i=1
	for doc in qList:
		dic[i]=doc
		i+=1
	output = open('./pkl/queries.pkl', 'wb')
	pickle.dump(dic, output)
	output.close()
	return dic

diQuery = index_req("./cacm/query.text")
diDocs = req_docs("./cacm/qrels.text")



def recall(ourDocs , pertDocs):
	intersection = len([doc[1] for doc in ourDocs if doc[1] in pertDocs])
	return intersection / len(pertDocs)

def precision(ourDocs , pertDocs):
	intersection = len([doc[1] for doc in ourDocs if doc[1] in pertDocs])
	return intersection / len(ourDocs)
