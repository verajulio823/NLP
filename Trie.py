from typing import Tuple
from scipy.sparse import csr_matrix
import numpy as np
from math import log
import csv
import os
import pickle


class TrieNode(object):
    
    def __init__(self, char: str):
        self.char = char
        self.children = []
        # Esta variable verifica si el caracter termina en palabra
        self.word_finished = False
        self.counter = 1
        self.indexTF = 0
        self.TF = []
        self.countDocument =0
        self.IDF = 0.0
        self.indexTFIDF = 0
        self.TFIDF =[]

    def __str__(self) -> str:
        return "TrieNode\{ char: %s countDocument:%s TF:%s \nIDF: %s TFIDF: %s\}" % (self.char, self.countDocument, self.TF, self.IDF, self.TFIDF)

class MyTrie:

    def __init__(self):
        self.sparseMatrixTF = []
        self.sparseMatrixTFIDF = []
        self.dictTF = {}

    def add3(self, root, page_id:int, word: str, count: int, ndocs: int):
        """
        Adding a word in the trie structure
        """
        node = root
        for char in word:
            found_in_child = False
            # Busca para el caracter en los hijos del nodo actual
            for child in node.children:
                if child.char == char:
                    child.counter += 1                    
                    node = child
                    found_in_child = True
                    break
            # Si no encontramos un hijo creamos un nodo
            if not found_in_child:
                new_node = TrieNode(char)
                node.children.append(new_node)
                # y actualizamos el nuevo nodo
                node = new_node
        # Cada ves que terminamos de recorrer marcamos como palabra
        node.countDocument= node.countDocument+1
        node.word_finished = True

        td_c, tf_c = calculateTF2(count, ndocs)
        td_c =  round(td_c, 5)
        tf_c =  round(tf_c, 5)

        nodetf = NodeTF(page_id, td_c, tf_c)
        #nodeTF = {"ndoc":page_id,"td": td_c, "TF": tf_c}
        #print(nodetf)
        #node.TF.append(nodetf)

<<<<<<< HEAD
        '''
=======
        
>>>>>>> 89680080e2e03b2679a123cafff27ddac9e2a90e
        if word in self.dictTF.keys():
            #self.dictTF[word].append([str(page_id), str(td_c), str(tf_c)])
            self.dictTF[word].update({str(page_id): [str(td_c), str(tf_c)]})
          
        else:
            self.dictTF[word] = {}
            #self.dictTF[word].append([str(page_id), str(td_c), str(tf_c)])
            self.dictTF[word].update({str(page_id): [str(td_c), str(tf_c)]})
<<<<<<< HEAD
        #appendTFdisk(word, node.TF)
        #node.TF = []
        #if len(node.TF) > 10000:
        #    appendTFdisk(word, node.TF)
        #    node.TF = []
        '''
=======
        
>>>>>>> 89680080e2e03b2679a123cafff27ddac9e2a90e


class NodeTF:
    def __init__(self, ndoc: int, td: int, TF : float):
        self.ndoc = ndoc
        self.td = td
        self.TF = TF

    def __repr__(self) -> str:
        return "NodeTF ( %s, %s, %s)" %(self.ndoc, self.td, self.TF)

    def __hash__(self):
        return hash(self.__repr__())

class NodeTFIDF:
    def __init__(self, ndoc: int, tfidf: float ):
        self.ndoc = ndoc
        self.tfidf = tfidf
    def __repr__(self) -> str:
        return "NodeTFIDF ( %s, %s)" %(self.ndoc, self.tfidf)

    def __hash__(self):
        return hash(self.__repr__())

def calculateTF2(count: int, ndocs: int) -> Tuple[int, float]:
    tf = count/ndocs
    return count,tf

def calculateIDF(D: int, countDocument: int)-> float:
    return log(D/countDocument)

def find_word(root, word: str) -> Tuple[bool, TrieNode]:
    #Funcion para buscar una palabra en el Trie
    node = root
    if not root.children:
        return False, 0
    #Buscamos caracter por caracter en el Trie    
    for char in word:
        char_not_found = True
        for child in node.children:
            if child.char == char:
                char_not_found = False
                node = child
                break
        if char_not_found:
            return False, 0
    if node.word_finished:
        # si encontramos el nodo retornamos True
        return True, node

    
    return False, node
    
def dfsTrie(node:TrieNode, D: int) -> bool:
    
    #Recorremos en DFS el Trie para ir calculando el IDF
    for child in node.children:
        
        if(child.word_finished):
            child.IDF=calculateIDF(D, child.countDocument)            
            
            for ctf in child.TF:
               
                tfidf = NodeTFIDF(ctf.ndoc, ctf.TF*child.IDF)
                child.TFIDF.append(tfidf)

        if dfsTrie(child, D):
            return True
    return False

def searchMatchin(listTFIDF: list) -> list:
    listResult=[]
    size=0 
    if len(listTFIDF[0]) >10:
        size=10
    else:
        size= len(listTFIDF[0])    
    for i in range(len(listTFIDF)):
       for key in listTFIDF[i]:
            for i_c in range(len(listTFIDF)):
                for key_c in listTFIDF[i_c]:
                   print(key, " ***** ", key_c)
                   if i!=i_c:
                       listResult.append(listTFIDF[i])

                      # if  listTFIDF[i][j].ndoc ==listTFIDF[i_c][j_c].ndoc:
                      #     listResult.append(listTFIDF[i][j])
   # for ltfidf in listTFIDF:
   #     for n in range(0,size):
   #         listResult.append(ltfidf[n])

    #print("Result: " ,listResult)
    return list(set(listResult))

def searchQuery(root: TrieNode, query: str) -> str:

    # buscamos las palabras sus TFIDF
    listWords = query.split(" ")
    listTFIDF=[]

    #recorremos cada palabra de consulta en el Trie
    for word in listWords:
        node = root    
        if not root.children:
            return ""
        for char in word:
            char_not_found = True
            for child in node.children:
                if child.char == char:
                    char_not_found = False
                    node = child
                    break
            if char_not_found:
                return ""
        if node.word_finished:
            # Si termina en palabra cargamos sus valores de TF*IDF
            with open("alphabetic/" +word[0].upper() +".p", 'rb') as fp:
                data = pickle.load(fp) 
            listTFIDF.append(data[word])

    
   # print("LIST RESULT: ", listTFIDF)
    return searchMatchin(listTFIDF)

def find_prefix(root, prefix: str) -> Tuple[bool, int]:
   
    node = root
    # Si el nodo raiz no tiene palabra retornamos falso
    
    if not root.children:
        return False, 0
    for char in prefix:
        char_not_found = True
        # Buscamos el nodo hijo en el presente nodo
        for child in node.children:
            if child.char == char:
                # Buscamos el caracter en el presente nodo
                char_not_found = False
                node = child
                break
        
        if char_not_found:
            return False, 0
    return True, node.counter

