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
from multiprocessing import Pool, freeze_support
import json
from time import process_time

def calculateTF(word, listWords: list) -> Tuple[int, float]:
    t =listWords.count(word)
    tf = t/len(listWords)
    return t,tf

def addNodeTrie(root: TrieNode , page_id: int, word: str, listWords: list):
      #print(word)
      #print(listWords.count(word), " ", word)
      Trie.add2(root,page_id,word, listWords)
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

def main():
    root = TrieNode('*')
    myTrie = MyTrie()
    #myTrie.sparseMatrixTF.append({"ndoc":0,"td":1, "TF": 0.4})
    #print(myTrie.sparseMatrixTF[0])

    #df = pd.read_csv('datasetTest.csv')
    df = pd.read_csv('datasetcount.csv')

    t1_start = process_time() 
    for i in df.index:
        document = df.iloc[i]["Content"]
        page_id = df.iloc[i]["page_id"]
        title = df.iloc[i]["title"]

       # print(document)
        document = document.replace("'", "\"")
        jdoc = json.loads(document)
        for word in jdoc:
           # print(word)
            Trie.add3(root,page_id,word, jdoc[word], len(jdoc))

        #print(i)
        #document=document.replace("[","").replace("]","").replace("'","").replace(" ","")
        
        #listWords= document.split(",")
        #listUniqueWords = list(set(listWords))

        #pool_obj = Pool()

       # arguments=[]

       # for word in listUniqueWords:
            #print(word)
            #print(listWords.count(word), " ", word)
            #Trie.add2(root,page_id,word, listWords)

        #    arguments.append((root, page_id, word, listWords))

        #print(arguments)
        #pool_obj.starmap(addNodeTrie,arguments)
        #td, tf = calculateTF(word, listWords)
        #nodeTF = {"ndoc":page_id,"td": td, "TF": tf}
        #print("word: ", word, " ",nodeTF)
    #print(listWords[0])
    #Trie.add()

    """""
    general_path = "C:/Users/rjru/OneDrive/Documentos/wiki_proyect/"
    index_bd_file = pd.read_csv(general_path + "indice_test.csv") 
    for fn in index_bd_file["filename"]: # leemos el batch de documentos.
        file_df = pd.read_csv(general_path+"dataset_tokenized_remove_stopword_lemma/"+os.path.splitext(fn)[0]+".csv", index_col=0)
        
        for doc in file_df.itertuples():
        listUniqueWords = list(set(ast.literal_eval(doc.Content)))
        for word in listUniqueWords:
            Trie.add2(root, doc.page_id, word, ast.literal_eval(doc.Content))
        print("Fin Doc")
    """
    t1_stop = process_time()
    
    print("Elapsed time:", t1_stop, t1_start)
    print("aquiiiiiiiiiiii")
    isFinish, node=  Trie.find_word(root, 'air')
    print(isFinish)
    isFinish, node=  Trie.find_word(root, 'sunny')
    print(isFinish)
    print("************************")
    print(Trie.dfsTrie(root, len(df)))
    print("************************")
    print(Trie.searchQuery(root, "island singapore"))


if __name__=="__main__":
    freeze_support()
    main()