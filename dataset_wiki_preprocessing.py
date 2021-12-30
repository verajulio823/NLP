from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from gensim.parsing.preprocessing import remove_stopwords
from gensim.corpora.wikicorpus import WikiCorpus
from nltk.stem import WordNetLemmatizer 
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from collections import Counter
import pandas as pd
import pattern
from pattern.text.en import lemma
import nltk
import ast
import os
import json

# bd orignal https://dumps.wikimedia.your.org/enwiki/20211220/

general_path = "C:/Users/rjru/OneDrive/Documentos/wiki_proyect/"
nltk.download('stopwords')
cachedStopWords = stopwords.words("english")

def get_wordnet_pos(word):
    """Map POS tag to first character lemmatize() accepts"""
    tag = nltk.pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}

    return tag_dict.get(tag, wordnet.NOUN)

lemmatizer = WordNetLemmatizer()

class TaggedWikiDocument(object):
    def __init__(self, wiki):
        self.wiki = wiki
        self.wiki.metadata = True
    def __iter__(self):
        for content, (page_id, title) in self.wiki.get_texts():
            yield TaggedDocument([c.decode("utf-8") for c in content], [title])

def tokenizeBatchWiki(index_bd_file):
    for fn in index_bd_file["filename"]:
        wiki = WikiCorpus(fname=general_path+"dataset_original/"+fn, article_min_tokens=250, token_min_len=3, lower=True)
        documents = TaggedWikiDocument(wiki)

        res = []
        for doc in documents.wiki.get_texts():
            #print("Contenido: ", doc[0])
            #print("id: ", doc[1][0])
            #print("título: ", doc[1][1])
            res.append([doc[1][0], doc[1][1], doc[0]])
            #print(doc[1][0])
        df = pd.DataFrame(res, columns = ['page_id', 'title', 'Content'])
        df.to_csv(general_path + "dataset_tokenized/" + fn + ".csv")
        print("The file was processed: ", fn)

def RemoveStopWordBatchWiki(index_bd_file):
    for fn in index_bd_file["filename"]:
        file_df = pd.read_csv(general_path+"dataset_tokenized/"+fn+".csv", index_col=0)
        file_df["Content"] = file_df["Content"].apply(lambda x: [item for item in ast.literal_eval(x) if item not in cachedStopWords])
        file_df.to_csv(general_path + "dataset_tokenized_remove_stopword/" + os.path.splitext(fn)[0] +".csv")
        print("The file was processed: ", fn)

def lemmaBatchWiki(index_bd_file):
    # https://www.machinelearningplus.com/nlp/lemmatization-examples-python/
    # https://stackoverflow.com/questions/44234796/pattern-package-for-python-3-6-anaconda
    for fn in index_bd_file["filename"]:
        file_df = pd.read_csv(general_path+"dataset_tokenized_remove_stopword/"+os.path.splitext(fn)[0]+".csv", index_col=0)
        # muy lento
        #file_df["Content"] = file_df["Content"].apply(lambda x: [lemmatizer.lemmatize(w, get_wordnet_pos(w)) for w in ast.literal_eval(x)])
        # usando esta libreria es más rápido
        # https://github.com/clips/pattern/wiki/pattern-en
        file_df["Content"] = file_df["Content"].apply(lambda x: [lemma(wd) for wd in ast.literal_eval(x)])
        
        file_df.to_csv(general_path + "dataset_tokenized_remove_stopword_lemma/" + os.path.splitext(fn)[0] +".csv")
        print("The file was processed: ", fn)

def WordCountBatchWiki(index_bd_file):
    for fn in index_bd_file["filename"]:
        file_df = pd.read_csv(general_path+"dataset_tokenized_remove_stopword_lemma/"+os.path.splitext(fn)[0]+".csv", index_col=0)

        file_df["Content"] = file_df["Content"].apply(lambda x: dict(Counter(ast.literal_eval(x))))
        
        file_df.to_csv(general_path + "dataset_tokenized_remove_stopword_lemma_count/" + os.path.splitext(fn)[0] +".csv")
        print("The file was processed: ", fn)


def WordCountTotalBatchWiki(index_bd_file):
    totalCountWord = {}

    # open file for writing, "w" 
    f = open("result.json","w", encoding="utf-8")
    i = 0
    for fn in index_bd_file["filename"]:
        file_df = pd.read_csv(general_path+"dataset_tokenized_remove_stopword_lemma_count/"+os.path.splitext(fn)[0]+".csv", index_col=0)

        #file_df["Content"] = file_df["Content"].apply(lambda x: dict(Counter(ast.literal_eval(x))))
        for doc in file_df.itertuples():
            document = doc.Content
            document = document.replace("'", "\"")
            jdoc = json.loads(document)

            for word in jdoc:
                if word in totalCountWord.keys():
                    totalCountWord[word] = totalCountWord[word] + jdoc[word]
                else:
                    totalCountWord[word] = jdoc[word]
            # print(word)
                #Trie.add3(root, page_id, word, jdoc[word], len(jdoc))
        i = i+1
        print("Fin batch: ", i)
    orderWordCount = {k: v for k, v in sorted(totalCountWord.items(), key=lambda item: item[1], reverse=True)}
    #f.write(str(totalCountWord))
    json.dump(orderWordCount, f, ensure_ascii=False, indent=4)
    f.close()

if __name__ == '__main__':
    index_bd_file = pd.read_csv(general_path + "indice.csv")  
    #tokenizeBatchWiki(index_bd_file)
    #RemoveStopWordBatchWiki(index_bd_file)
    #lemmaBatchWiki(index_bd_file)
    #WordCountBatchWiki(index_bd_file)
    WordCountTotalBatchWiki(index_bd_file)
    print("That it is done")