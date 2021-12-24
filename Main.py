from numpy.lib.shape_base import split
from typing import Tuple
import Trie
from Trie import TrieNode
from Trie import MyTrie
import pandas as pd
import numpy as np
from scipy.sparse import csr_matrix
import re

def calculateTF(word, listWords: list) -> Tuple[int, float]:
    t =listWords.count(word)
    tf = t/len(listWords)
    return t,tf


""""
Trie.add(root, "hackathon")
Trie.add(root, 'hack')

print(Trie.find_prefix(root, 'hac'))
print(Trie.find_prefix(root, 'hack'))
print(Trie.find_prefix(root, 'hackathon'))
print(Trie.find_prefix(root, 'ha'))
print(Trie.find_prefix(root, 'hammer'))

print("*********************************")

print(Trie.find_word(root, 'hac'))
print(Trie.find_word(root, 'hack'))
print(Trie.find_word(root, 'hackathon'))
print(Trie.find_word(root, 'ha'))
print(Trie.find_word(root, 'hammer'))
"""
root = TrieNode('*')
myTrie = MyTrie()
#myTrie.sparseMatrixTF.append({"ndoc":0,"td":1, "TF": 0.4})
#print(myTrie.sparseMatrixTF[0])

df = pd.read_csv('datasetTest.csv')

for i in range(0,4):
  document = df.iloc[i]["Content"]
  page_id = df.iloc[i]["page_id"]
  title = df.iloc[i]["title"]
  document=document.replace("[","").replace("]","").replace("'","").replace(" ","")
  
  listWords= document.split(",")
  listUniqueWords = list(set(listWords))
  for word in listUniqueWords:
     # print(word)
      #print(listWords.count(word), " ", word)
      Trie.add(root,word)
      td, tf = calculateTF(word, listWords)
      nodeTF = {"ndoc":page_id,"td": td, "TF": tf}
      print("word: ", word, " ",nodeTF)
  #print(listWords[0])
  #Trie.add()
print(Trie.find_word(root, 'air'))


