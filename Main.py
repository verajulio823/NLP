from numpy.lib.shape_base import split
from typing import Tuple
import Trie
from Trie import TrieNode
from Trie import MyTrie
import pandas as pd
import numpy as np
from scipy.sparse import csr_matrix
import re
import ast
import os

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
'''
df = pd.read_csv('datasetTest.csv')

for i in range(0,4):
  document = df.iloc[i]["Content"]
  page_id = df.iloc[i]["page_id"]
  title = df.iloc[i]["title"]
  document=document.replace("[","").replace("]","").replace("'","").replace(" ","")
  
  listWords= document.split(",")
  listUniqueWords = list(set(listWords))
  for word in listUniqueWords:
      #print(word)
      #print(listWords.count(word), " ", word)
      Trie.add2(root,page_id,word, listWords)
      #td, tf = calculateTF(word, listWords)
      #nodeTF = {"ndoc":page_id,"td": td, "TF": tf}
      #print("word: ", word, " ",nodeTF)
  #print(listWords[0])
  #Trie.add()
'''

general_path = "C:/Users/rjru/OneDrive/Documentos/wiki_proyect/"
index_bd_file = pd.read_csv(general_path + "indice_test.csv") 
for fn in index_bd_file["filename"]: # leemos el batch de documentos.
    file_df = pd.read_csv(general_path+"dataset_tokenized_remove_stopword_lemma/"+os.path.splitext(fn)[0]+".csv", index_col=0)
    
    for doc in file_df.itertuples():
      listUniqueWords = list(set(ast.literal_eval(doc.Content)))
      for word in listUniqueWords:
        Trie.add2(root, doc.page_id, word, ast.literal_eval(doc.Content))
    print("Fin Doc")


isFinish, node=  Trie.find_word(root, 'air')
#print(node)
isFinish, node=  Trie.find_word(root, 'sunny')
#print(node)
print("************************")
print(Trie.dfsTrie(root, 4))
#print(Trie.searchQuery(root, "island singapore"))
