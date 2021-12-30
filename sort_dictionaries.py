import pickle5 as pickle
from Trie import *
import os

general_path = "/content/drive/MyDrive/VIII Semestre UNSA/ds/"

with open(general_path+"trieLight"+".p", 'rb') as fp:
    root = pickle.load(fp)
    

general_path = "/content/drive/MyDrive/VIII Semestre UNSA/ds/TFIDF/"

D = 249867

for filename in os.listdir(general_path+"files/"):
  data = []
  print("loading file " + filename + "...")
  with open(general_path+ "files/" + filename, 'rb') as fp:
        data = pickle.load(fp)
  print("finished loading file " + filename)
  for word, nodoTF in data.items():
    _, trieNode = find_word(root, word)
    DF = trieNode.countDocument
    IDF = calculateIDF(D, DF)
    data[word] = {k: v for k, v in sorted(nodoTF.items(), key=lambda item: (float(item[1][1]) * IDF), reverse=True)}
    for nDoc, TF in nodoTF.items():
      data[word][nDoc] = float(TF[1]) * IDF
  print("saving sorted file " + filename)
  with open(general_path + "sortedFiles/" + filename, 'wb') as fp:
        pickle.dump(data, fp, protocol=pickle.HIGHEST_PROTOCOL)
  print("done saving sorted file " + filename)
  