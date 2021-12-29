from numpy.lib.shape_base import split
from typing import Tuple
import Trie
from Trie import TrieNode
from Trie import MyTrie
from Trie import *
import pandas as pd
import os
import json
from time import process_time
import pickle


def main():
    root = TrieNode('*')
    myTrie = MyTrie()

    general_path = "C:/Users/rjru/OneDrive/Documentos/wiki_proyect/"
    index_bd_file = pd.read_csv(general_path + "indice.csv") 

    for fn in index_bd_file["filename"]: # leemos el batch de documentos.
        
        t1_start = process_time()

        file_df = pd.read_csv(general_path+"dataset_tokenized_remove_stopword_lemma_count/"+os.path.splitext(fn)[0]+".csv", index_col=0)
        
        for doc in file_df.itertuples():
            document = doc.Content
            page_id = doc.page_id
            title = doc.title

            document = document.replace("'", "\"")
            jdoc = json.loads(document)

            for word in jdoc:
                myTrie.add3(root, page_id, word, jdoc[word], len(jdoc))
        
            print("Fin Doc: ", page_id, end="\r")

        print("Fin BATCH: ", os.path.splitext(fn)[0])

        t1_stop = process_time()
        print("Elapsed time:", t1_stop, t1_start)

        print("save myTrie.dictTF")
        with open(general_path+"dicttf/"+os.path.splitext(fn)[0]+".p", 'wb') as fp:
            pickle.dump(myTrie.dictTF, fp, protocol=pickle.HIGHEST_PROTOCOL)

        myTrie.dictTF = {}


"""""
isFinish, node=  Trie.find_word(root, 'air')
print(isFinish)
isFinish, node=  Trie.find_word(root, 'sunny')
print(isFinish)
print("************************")
print(Trie.dfsTrie(root, len(df)))
print("************************")
print(Trie.searchQuery(root, "island singapore"))
"""""

if __name__=="__main__":
    main()



'''
    df = pd.read_csv('C:/Users/rjru/OneDrive/Documentos/wiki_proyect/datasetTest.csv')

    t1_start = process_time() 
    for i in df.index:
        document = df.iloc[i]["Content"]
        page_id = df.iloc[i]["page_id"]
        title = df.iloc[i]["title"]

        document = document.replace("'", "\"")
        jdoc = json.loads(document)
        for word in jdoc:
            # print(word)
            myTrie.add3(root, page_id, word, jdoc[word], len(jdoc))
            print(word)
    t1_stop = process_time()

    print("save myTrie")
    with open("C:/Users/rjru/OneDrive/Documentos/wiki_proyect/dicttf/trie.p", 'wb') as fp:
        pickle.dump(root, fp, protocol=pickle.HIGHEST_PROTOCOL)
'''