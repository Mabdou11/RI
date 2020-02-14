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


def similarity_study():
	start = time.time()
	print("rappel & precision:")
	evaldict = dict()
	pevalist = []
	revalist = []

	smin = list()
	for val in range(1,70, 5):
		print("n°,Produit_interne, Dice, Cosinus, Jaccard")
		valdict = dict()
		minSeuil = []
		recallist = []
		precilist = []
		for i in range(1,len(diQuery)+1):
			try:
				didoc =	[int(doc) for doc in diDocs[i]]

				cos	=	cosinus	(	  diQuery[i],weighted)	[:int(len(diQuery[i])*val/100)]
				# di	=	dice	(	  diQuery[i],weighted)	[:int(len(diQuery[i])*val/100)]
				# jac	=	jaccard	(	  diQuery[i],weighted)	[:int(len(diQuery[i])*val/100)]
				# ip	=	inner_product(diQuery[i],weighted)	[:int(len(diQuery[i])*val/100)]

				# ri_p = recall( ip, didoc)
				# rdic = recall( di, didoc)
				rcos = recall([v for v in cos if v[0]>=(i/100.0)], didoc)
				# rjac = recall(jac, didoc)
				
				# pi_p = precision( ip, didoc)
				# pdic = precision( di, didoc)
				pcos = precision([v for v in cos if v[0]>=(i/100.0)], didoc)
				# pjac = precision(jac, didoc)
				minSeuil.append(min([v[0] for v in cos]))
				# valdict[i]	+=	{'recall':rcos}
				# valdict[i]	+= 	{'precision':pcos}
				
				recallist.append(rcos)
				precilist.append(pcos)
				# print(str(i)+", %.5f"%ri_p+", %.5f"%rdic+", %.5f"%rcos+", %.5f"%rjac)
				# print(str(i)+", %.5f"%pjac)
				# print("------------------------------------------")
			except KeyboardInterrupt:
				return 
			except:
				# print("no relevant document for query %d"%i)
				# print("------------------------------------------")
				continue
		# evaldict['val'] = valdict
		smin.append(minSeuil)
		revalist.append(recallist)
		pevalist.append(precilist)
		print("length: "+str(val) +"%% elapsed time: %.5f (s)"%(time.time()-start))
		print("-----------------------")
		print()
	evaldict['recall'] = revalist
	evaldict['precision'] = pevalist
	evaldict['seuilmin'] = smin
	eval_file = open("evaluation_seuil_005.pkl","wb")
	pickle.dump(evaldict, eval_file)
	eval_file.close()
	return revalist, pevalist

# raffilist, paffilist = similarity_study()


# similarity_study()

f= open("evaluation_seuil_005.pkl","rb")
pkl =pickle.load(f)
import matplotlib.pyplot as plt

# print(pkl['recall'])
# print(pkl['precision'])


reclist = [(sum(val)/len(val)) for val in pkl['recall']]
prelist = [(sum(val)/len(val)) for val in pkl['precision']]
seuilx = [sum(seuil)/len(seuil) for seuil in pkl['seuilmin']]

for s in seuilx:
	print(s)
print("recall")
for r  in reclist:
	print(r)
print("precision")

for p in prelist:
	print(p)




plt.plot(reclist,prelist, '.-', label="précision/rappel")
plt.legend()  # To draw legend

plt.show()
# print(max)

# # for k in pkl[40].values():
# 	# plt.plot(k, pkl[40][k]['recall']['inner_product'], '.-', label=k)
# 	# NOTE: changed `range(1, 4)` to mach actual values count
# plt.legend()  # To draw legend
# plt.show()



