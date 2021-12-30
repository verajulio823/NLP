from Trie import *
import pickle
import pandas as pd
import os
import json
    

general_path = "C:/Users/veraj/Documents/Workspace/Python/NLP/"
index_bd_file = pd.read_csv(general_path + "indice_light.csv")

values_a = {}
values_b = {}
values_c = {}
values_d = {}
values_e = {}
values_f = {}
listdic = []

for fn in index_bd_file["filename"]: # leemos el batch de documentos.
    with open("C:/Users/veraj/Documents/Workspace/Python/NLP/dicttf/" + os.path.splitext(fn)[0]+".p", 'rb') as fp:
        data = pickle.load(fp) 
        print(fn)
        for key in data:
            if key[0] == "u":
                if key in values_a.keys():
                    values_a[key].update(data[key])
                else:                   
                    values_a[key] = data[key]

            if key[0] == "v":             
                if key in values_b.keys():                  
                    values_b[key].update(data[key])
                else:                   
                    values_b[key] = data[key]

            if key[0] == "w":             
                if key in values_c.keys():                  
                    values_c[key].update(data[key])
                else:                   
                    values_c[key] = data[key]
            if key[0] == "x":             
                if key in values_d.keys():                  
                    values_d[key].update(data[key])
                else:                   
                    values_d[key] = data[key]
            if key[0] == "y":             
                if key in values_e.keys():                  
                    values_e[key].update(data[key])
                else:                   
                    values_e[key] = data[key]
            if key[0] == "z":             
                if key in values_f.keys():                  
                    values_f[key].update(data[key])
                else:                   
                    values_f[key] = data[key]


print("save A y B")

#print(values_a)
#print(values_b)
with open(general_path+"alphabetic/"+"U"+".p", 'wb') as fp:
    pickle.dump(values_a, fp, protocol=pickle.HIGHEST_PROTOCOL)
with open(general_path+"alphabetic/"+"V"+".p", 'wb') as fp:
    pickle.dump(values_b, fp, protocol=pickle.HIGHEST_PROTOCOL)
with open(general_path+"alphabetic/"+"W"+".p", 'wb') as fp:
    pickle.dump(values_c, fp, protocol=pickle.HIGHEST_PROTOCOL)
with open(general_path+"alphabetic/"+"X"+".p", 'wb') as fp:
    pickle.dump(values_d, fp, protocol=pickle.HIGHEST_PROTOCOL)
with open(general_path+"alphabetic/"+"Y"+".p", 'wb') as fp:
    pickle.dump(values_e, fp, protocol=pickle.HIGHEST_PROTOCOL)
with open(general_path+"alphabetic/"+"Z"+".p", 'wb') as fp:
    pickle.dump(values_f, fp, protocol=pickle.HIGHEST_PROTOCOL)


