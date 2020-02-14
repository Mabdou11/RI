import pickle 
import time
import math

start = time.time()
f =  open('pkl/index_file.pkl', 'rb')
index = pickle.load(f)
f =  open('pkl/reversed_file.pkl', 'rb')
rev = pickle.load(f)
f =  open('pkl/weighted_reversed_file.pkl', 'rb')
weighted = pickle.load(f)

def inner_product(req, weighted):
    requete = req.split()
    somme = 0.0 # somme des poids
    lendocs = weighted[len(weighted)-1][1]
    docList = []
    j=0
    for i in range(1,lendocs+1):
        if i != weighted[j][1]:
            while  j < len(weighted) and i != weighted[j][1]:
                j+1
        while j < len(weighted) and  i == weighted[j][1] :
            for term in requete:
                if term == weighted[j][0]:
                    somme += weighted[j][2]
            j+=1
        if somme>0:
            docList.append([somme,i])
        somme = 0
        docList.sort(reverse=True)
    return docList

def dice(req, weighted):
    requete = req.split()
    somme = 0.0
    lendocs = weighted[len(weighted)-1][1]
    docList = []
    j=0
    docs=0.0
    X2 = 0.0
    for i in range(1,lendocs+1):
        if i != weighted[j][1]:
            while  j < len(weighted) and i != weighted[j][1]:
                j+1
        while j < len(weighted) and  i == weighted[j][1] :
            for term in requete:
                if term == weighted[j][0]:
                    somme += weighted[j][2]
                    X2+= somme*somme
                    docs+=1
            j+=1
        if somme>0:
            poid = 2*somme /(X2 + docs)
            docList.append([poid,i])
        somme = 0
        docs = 0
        docList.sort(reverse=True)
    return docList

def jaccard(req, weighted):
    requete = req.split()
    somme = 0.0
    lendocs = weighted[len(weighted)-1][1]
    docList = []
    j=0
    docs=0.0
    X2 = 0.0
    for i in range(1,lendocs+1):
        if i != weighted[j][1]:
            while  j < len(weighted) and i != weighted[j][1]:
                j+1
        while j < len(weighted) and  i == weighted[j][1] :
            for term in requete:
                if term == weighted[j][0]:
                    somme += weighted[j][2]
                    X2+= somme*somme
                    docs+=1
            j+=1
        if somme>0:
            poid = somme /(X2 + docs - somme)
            docList.append([poid,i])
        somme = 0
        docs = 0
        docList.sort(reverse=True)
    return docList


def cosinus(req, weighted):
    requete = req.split()
    somme = 0.0
    lendocs = weighted[len(weighted)-1][1]
    docList = []
    j=0
    docs=0.0
    X2= 0.0
    for i in range(1,lendocs+1):
        if i != weighted[j][1]:
            while  j < len(weighted) and i != weighted[j][1]:
                j+1
        while j < len(weighted) and  i == weighted[j][1] :
            for term in requete:
                if term == weighted[j][0]:
                    somme += weighted[j][2]
                    X2+= somme*somme
                    docs+=1
            j+=1
        if somme>0:
            poid = somme /math.sqrt(X2 + docs*docs)
            docList.append([poid,i])
        docs = 0
        somme = 0
        docList.sort(reverse=True)
    return docList


start = time.time()


# print(cosinus('artificial',weighted))
# print(jaccard('artificial',weighted))
# print(dice('artificial',weighted))
# print(inner_product('artificial',weighted))
# print(time.time()-start)

