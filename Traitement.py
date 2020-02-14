# -*- coding: utf-8 -*-
"""
Created on Fri Dec 27 06:25:13 2019

@author: DELL
"""

from nltk import word_tokenize
#from nltk.corpus import stopwords
import time
import pickle
from PyQt5 import QtWidgets
from evaluate import *
import re
from vectorial import *
class traitement :
    
    def __init__(self):
        
        infile = open('pkl/index_file.pkl','rb')
        self.index = pickle.load(infile)
        infile.close()
        infile = open('pkl/reversed_file_dict.pkl','rb')
        self.reversed = pickle.load(infile)
        infile.close()

        infile =open('pkl/weighted_reversed_file_dict.pkl','rb')
        self.weighted_reversed_file = pickle.load(infile)
        infile.close()
        
        
#        #stopwords = set(stopwords.words('english'))
#        for i in self.files_with_index :
#            print(i,self.files_with_index[i].keys())
#            break
#
        self.unique_word=[word for index in self.index for word in self.index[index].keys()]
        self.unique_word=list(sorted(set(self.unique_word)))
#        
#        infile = open('CodePython/w_invertedFile.pkl','rb') 
#        self.w_invertedFile = pickle.load(infile) 
#        infile.close()


    def Fonctions_dacces1(self,interface) :
        ## recherche mot
        interface.listWidget.clear()
        interface.listWidget_6.clear()
        idDoc= interface.spinBox.value()
        
        interface.listWidget.addItem("Document . "+str(idDoc))
        
        for j in self.index[str(idDoc)]:
            interface.listWidget_6.addItem(" "+j+" |Freq:"+str(self.index[str(idDoc)][j])+"| weight: "+str(self.weighted_reversed_file[(j,int(idDoc))])[:4])

    def Fonctions_dacces2(self,interface):
        ## rechercher document

        interface.listWidget.clear()
        interface.listWidget_6.clear()
        L2=list()
        word=interface.lineEdit.text().lower()
        for i in self.reversed :
            if i[0] == word :
                L1=list()
                L1.append(i[1])
                L1.append(self.reversed[i])
                L1.append(self.weighted_reversed_file[i])
                #t=tuple(L1)
                L2.append(L1)
        
        for element in L2:
            interface.listWidget_6.addItem("I ."+str(element[0])+"\tfreq= "+str(element[1])+"|\tWeight:%.4f"%element[2])

    def boolean_query(self,q):
        
        q.listWidget.clear()
        q.listWidget_5.clear()
        qery=q.textEdit.toPlainText()
        if qery =='':
            error=QtWidgets.QErrorMessage()
            error.showMessage("Veuillez écrire la requête")
            error.exec_()
            return
        words=[word.lower() for word in word_tokenize(qery)]
        boolean_qery=[word for word in word_tokenize(qery)]
        list_fich_pert=list()
        start = time.time()
        for i in self.index:
            for j in range(len(words)) :
                if words[j] not in ['and','or','not','(',')'] :
                    if words[j] in self.index[i].keys() :
                        #print(i)
                        boolean_qery[j]=1
                    else:
                        boolean_qery[j]=0
            try:#evaluer la requette logique final (apres remplacement avec 0 et 1)
                bool_=eval(' '.join(str(e) for e in boolean_qery))
                #print(' '.join(str(e) for e in boolean_qery))
            except SyntaxError:
                error=QtWidgets.QErrorMessage()
                error.showMessage("Veuillez corriger le format de la requête")
                error.exec_()
                return #en cas d'exception la liste de fichier contien un nombre negative

            if bool_ == 1 :
                list_fich_pert.append(i)
        end = time.time()
        
        if len(list_fich_pert) == 0 :
                q.listWidget_5.addItem("Aucun document ne satisfait votre requête")

        for element in list_fich_pert:
            q.listWidget_5.addItem("Document . "+str(element))
        t= end - start
        q.textEdit_3.setText("%.2f s"%t)

    def checkIi(affiche) :
        pass


    def ChoixAffichage(self,interface, typeIndex): 
     
        interface.listWidget.clear()
       
        interface.listWidget_6.clear()
    # Affichage par documents
       
        if(interface.radioButton.isChecked()):
            
            if typeIndex=="Index" :
                
                self.AfficherDocs(interface)
                interface.listWidget.itemDoubleClicked.connect(lambda: self.LectureItemDocs(interface,typeIndex))
           
            elif typeIndex=="IndexP":
                
                self.AfficherDocs(interface)
                interface.listWidget.itemDoubleClicked.connect(lambda: self.LectureItemDocs(interface,typeIndex))
        elif(interface.radioButton_2.isChecked()):
            
            if typeIndex=="Index" :
               
                self.AfficherMots(interface)
                interface.listWidget.itemDoubleClicked.connect(lambda: self.LectureWords(interface,typeIndex))
           
            elif typeIndex=="IndexP":
                self.AfficherMots(interface)
                interface.listWidget.itemDoubleClicked.connect(lambda: self.LectureWords(interface,typeIndex))
        else:
            
            error=QtWidgets.QErrorMessage()
            error.showMessage("Veuillez choisir un mode d'affichage.")
            error.exec_() 
     
        return 0   

        #q.textEdit3

                
    def AfficherDocs(self,interface):
        
        interface.listWidget.clear()
        interface.listWidget_6.clear()
        for index in self.index:   
            interface.listWidget.addItem("I . {}".format(index))  
        #print(listeDec)
        

    def AfficherMots(self,interface):
        
        interface.listWidget.clear()
        
        interface.listWidget_6.clear()
        
        for word in self.unique_word:
             
            interface.listWidget.addItem(word)


    def LectureItemDocs(self,interface,type_):
       
        import re
        
        interface.listWidget_6.clear()
        Doc=interface.listWidget.currentItem().text()
        if type_=='IndexP':
            
            if(Doc.startswith('I . ')):
                num=re.findall('(\d+)',Doc)[0]
                for element in self.index[num]:
                     interface.listWidget_6.addItem(element+" : {}".format(self.weighted_reversed_file[(element,int(num))]))
            
            return 
        
        
        if(Doc.startswith('I . ')):
            num=re.findall('(\d+)',Doc)[0]
            
            for element in self.index[num]:
                
                interface.listWidget_6.addItem(element+" : {}".format(self.reversed[(element,int(num))]))
    
    def LectureWords(self,interface,typeIndex):
        
        Liste=dict()        
        interface.listWidget_6.clear()
        word=interface.listWidget.currentItem().text()
        if(typeIndex=="Index"):
            Liste = self.reversed

        elif(typeIndex=="IndexP"):
            Liste = self.weighted_reversed_file

        for element in Liste:
            if word == element[0]:
                interface.listWidget_6.addItem("D. "+str(element[1])+" : %.4f"%Liste[element])


    def evaluation(self,q,max):
        if not q.listWidget_3.currentItem():
            error=QtWidgets.QErrorMessage()
            error.showMessage("Veuillez selectionner une requête")
            error.exec_()
            return


        
        q.listWidget_5.clear()
        Doc=q.listWidget_3.currentItem().text()
        num=re.findall('^(\d+)',Doc)[0]
        ourDocs = cosinus(q.queries[int(num)],weighted)

        if q.radioButton_3.isChecked():
            ourDocs = inner_product(q.queries[int(num)], weighted)
        elif q.radioButton_4.isChecked():
            ourDocs = dice(q.queries[int(num)], weighted)
        elif q.radioButton_5.isChecked():            
            ourDocs = cosinus(q.queries[int(num)], weighted)
        elif q.radioButton_6.isChecked():
            ourDocs = jaccard(q.queries[int(num)], weighted)
        else:
            q.radioButton_5.setChecked(True)
            ourDocs = cosinus(q.queries[int(num)], weighted)
        ourDocs = ourDocs[:int(len(ourDocs)*max/100)]
        [q.listWidget_5.addItem("document:\t"+str(doc[1])+"\t\tpoids:\t"+str(doc[0])) for doc in ourDocs]
        try:        
            pertDocs = [int(doc) for doc in q.relevant_docs[int(num)]]
            q.textEdit_4.setPlainText(str(recall(ourDocs,pertDocs))[:5])
            q.textEdit_5.setPlainText(str(precision(ourDocs,pertDocs))[:5])
        except:
            pass


#if __name__ == '__main__':
#    t=traitement()
#    for j in t.f_w_index['1'] :
#        print(j,t.f_w_index['1'][j][0],t.f_w_index['1'][j][1])
#        print('****************')
#        break


# t = traitement()

# print(t.boolean_query( 'artificial and intelligence and computer or (computers and systems)'))