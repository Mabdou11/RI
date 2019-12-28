import re
from nltk.corpus import stopwords
from nltk import FreqDist as fd
# step 1:

document = open("./cacm/cacm.all","r+", encoding="utf-8").read()


def get_title(documents,number):
	document = get_doc(documents, number)
	match = re.search(r".T\n((.|\n)*?)\n\.", document)
	return match.group(1)

def get_words(documents, number):
	document = get_doc(documents, number)
	match = re.search(r".W\n((.|\n)*?)\n\.", document)
	if match:
		return match.group(1)
	else:
		return "None"

def get_doc(documents, number):

	match = re.search(r"\.I ("+str(number)+")\n\.T\n((.|\n)*?)\n\.B", documents)
	return match.group(0)


print()
print(get_title(document,123))
print()
print(get_words(document,113))


