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
    index_bd_file = pd.read_csv(general_path + "indice_light.csv") 

    if flagProcessing ==False:
        general_path = "C:/Users/veraj/Documents/Workspace/Python/NLP/"
        index_bd_file = pd.read_csv("indice_julio.csv") 

        index_files =0
        for fn in index_bd_file["filename"]: # leemos el batch de documentos.
            
            t1_start = process_time()

            file_df = pd.read_csv(general_path+"dataset_tokenized/"+os.path.splitext(fn)[0]+".csv", index_col=0)
            
            for doc in file_df.itertuples():
                document = doc.Content
                page_id = doc.page_id
                title = doc.title
                index_files=index_files+1

        #print("save myTrie.dictTF")
        #with open(general_path+"dicttf/"+os.path.splitext(fn)[0]+".p", 'wb') as fp:
        #    pickle.dump(myTrie.dictTF, fp, protocol=pickle.HIGHEST_PROTOCOL)

        #myTrie.dictTF = {}
    print("save myTrie")
    with open("C:/Users/rjru/OneDrive/Documentos/wiki_proyect/trieLight.p", 'wb') as fp:
        pickle.dump(root, fp, protocol=pickle.HIGHEST_PROTOCOL)

            print("Fin BATCH: ", os.path.splitext(fn)[0])

            t1_stop = process_time()
            print("Elapsed time:", t1_stop, t1_start)

            print("save myTrie.dictTF")
            with open(general_path+"dicttf/"+os.path.splitext(fn)[0]+".p", 'wb') as fp:
                pickle.dump(myTrie.dictTF, fp, protocol=pickle.HIGHEST_PROTOCOL)

            myTrie.dictTF = {}

    with open("trieLight.p", 'rb') as fp:
        trieRoot = pickle.load(fp) 
        

    #print(index_files)    
    #print(Trie.dfsTrie(root,249867))
    print(Trie.searchQuery(trieRoot, "elektriska monumental"))


if __name__=="__main__":
    main()
