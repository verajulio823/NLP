from typing import Tuple
from scipy.sparse import csr_matrix
import numpy as np
from math import log
import csv
import os


class TrieNode(object):
    """
    Our trie node implementation. Very basic. but does the job
    """
    
    def __init__(self, char: str):
        self.char = char
        self.children = []
        # Is it the last character of the word.`
        self.word_finished = False
        # How many times this character appeared in the addition process
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
            # Search for the character in the children of the present `node`
            for child in node.children:
                if child.char == char:
                    # We found it, increase the counter by 1 to keep track that another
                    # word has it as well
                    child.counter += 1
                    # And point the node to the child that contains this char
                    node = child
                    found_in_child = True
                    break
            # We did not find it so add a new chlid
            if not found_in_child:
                new_node = TrieNode(char)
                node.children.append(new_node)
                # And then point node to the new child
                node = new_node
        # Everything finished. Mark it as the end of a word.
        node.countDocument= node.countDocument+1
        node.word_finished = True

        td_c, tf_c = calculateTF2(count, ndocs)
        td_c =  round(td_c, 5)
        tf_c =  round(tf_c, 5)

        nodetf = NodeTF(page_id, td_c, tf_c)
        #nodeTF = {"ndoc":page_id,"td": td_c, "TF": tf_c}
        #print(nodetf)
        #node.TF.append(nodetf)

        '''
        if word in self.dictTF.keys():
            #self.dictTF[word].append([str(page_id), str(td_c), str(tf_c)])
            self.dictTF[word].update({str(page_id): [str(td_c), str(tf_c)]})
            # .update({'item3': 3})
        else:
            self.dictTF[word] = {}
            #self.dictTF[word].append([str(page_id), str(td_c), str(tf_c)])
            self.dictTF[word].update({str(page_id): [str(td_c), str(tf_c)]})
        #appendTFdisk(word, node.TF)
        #node.TF = []
        #if len(node.TF) > 10000:
        #    appendTFdisk(word, node.TF)
        #    node.TF = []
        '''


class NodeTF:
    def __init__(self, ndoc: int, td: int, TF : float):
        #{"ndoc":page_id,"td": td_c, "TF": tf_c}
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
          #tfidf= {"ndoc":ctf.ndoc,"tfidf": ctf.TF*child.IDF}
    def __repr__(self) -> str:
        return "NodeTFIDF ( %s, %s)" %(self.ndoc, self.tfidf)

    def __hash__(self):
        return hash(self.__repr__())

def calculateTF2(count: int, ndocs: int) -> Tuple[int, float]:
    #t =listWords.count(word)
    tf = count/ndocs
    return count,tf

def calculateIDF(D: int, countDocument: int)-> float:
    return log(D/countDocument)

def find_word(root, word: str) -> Tuple[bool, TrieNode]:

    node = root
    if not root.children:
        return False, 0
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
        return True, node

    
    return False, node
    
def dfsTrie(node:TrieNode, D: int) -> bool:
    
    #print("DFS: ",node.children)
   # if len(node.children) >1:
   #     print("char: ", node.char)
   #     return True
    for child in node.children:
        
        if(child.word_finished):
            child.IDF=calculateIDF(D, child.countDocument)            
            
            for ctf in child.TF:
                #print(ctf)
                tfidf = NodeTFIDF(ctf.ndoc, ctf.TF*child.IDF)
                child.TFIDF.append(tfidf)

          #  print("node: ", child)

        if dfsTrie(child, D):
            return True
    return False

def searchMatchin(listTFIDF: list) -> list:
    listResult=[]
    for i in range(len(listTFIDF)):
       for j in range(len(listTFIDF[i])):
            for i_c in range(len(listTFIDF)):
                for j_c in range(len(listTFIDF[i_c])):
                   if i!=i_c:
                       if listTFIDF[i][j].ndoc ==listTFIDF[i_c][j_c].ndoc:
                           listResult.append(listTFIDF[i][j])
    for ltfidf in listTFIDF:
        for n in range(0,2):
            listResult.append(ltfidf[n])

    #print("Result: " ,listResult)
    return list(set(listResult))

def searchQuery(root: TrieNode, query: str) -> str:

    listWords = query.split(" ")
    listTFIDF=[]

   
    
    for word in listWords:
        node = root    
        if not root.children:
            return ""
        #print(word)
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
            #print("Encontrreee: ", node)
            listTFIDF.append(node.TFIDF)
            #return ""
    
    #print(listTFIDF)
    return searchMatchin(listTFIDF)

def find_prefix(root, prefix: str) -> Tuple[bool, int]:
    """
    Check and return 
      1. If the prefix exsists in any of the words we added so far
      2. If yes then how may words actually have the prefix
    """
    node = root
    # If the root node has no children, then return False.
    # Because it means we are trying to search in an empty trie
    if not root.children:
        return False, 0
    for char in prefix:
        char_not_found = True
        # Search through all the children of the present `node`
        for child in node.children:
            if child.char == char:
                # We found the char existing in the child.
                char_not_found = False
                # Assign node as the child containing the char and break
                node = child
                break
        # Return False anyway when we did not find a char.
        if char_not_found:
            return False, 0
    # Well, we are here means we have found the prefix. Return true to indicate that
    # And also the counter of the last node. This indicates how many words have this
    # prefix
    return True, node.counter

