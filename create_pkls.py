import pickle 
import time
import math
start = time.time()
f =  open('pkl/index_file.pkl', 'rb')
index = pickle.load(f)

def create_rev(index):
    rev = dict()
    doc =1
    for i in index.values():
        for w in i.keys():
            rev[w,doc] = i[str(w)]
            #rev.append([w,doc,i[str(w)]])
        doc+=1
    return rev

w =  open('pkl/reversed_file_dict.pkl', 'wb')
pickle.dump(create_rev(index),w)

print(time.time()-start)

"""
took 0.12555789947509766 to create. rev file

"""

def create_weighted_rev(index,rev):
    w_rev= dict()
    N = len(index) # obvious
    #listWords = [i.keys() for i in index.values()]    
    for word in rev:
        # reversed --> [ mot, doc, freq],   index --> {doc: {mot: freq}}
        ni=0
        freq = word[2] # freq of ti
        maxF = max(index[str(word[1])].values()) # list of freq = index['doc'].values()
        #ni = [words for words in listWords if word[0] is words]
        for i in index.values():
            if word[0] in i.keys():
                ni+=1
        poid = (freq/maxF*math.log10(N/ni)+1)
        w_rev[word[0],word[1]] = poid
        #w_rev.append([word[0], word[1], poid])
        print(word[0]+','+str(word[1])+'->'+str(poid))
    return w_rev
    
# r =  open('pkl/reversed_file_dict.pkl', 'rb')
# rev_d = pickle.load(r)
# r.close()
# print(rev_d)

start = time.time()
r =  open('pkl/reversed_file.pkl', 'rb')
rev = pickle.load(r)

w =  open('pkl/weighted_reversed_file_dict.pkl', 'wb')
pickle.dump(create_weighted_rev(index, rev),w)
w.close()
print(time.time()-start)
"""
Time took: 67.16217803955078 seconds
"""

