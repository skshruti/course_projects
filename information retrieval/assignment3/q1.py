import numpy as np
import os
import json
from nltk.stem import PorterStemmer
import collections
from scipy import spatial
import re
import sys
import networkx as nx
import sknetwork as skn
from sknetwork.utils import edgelist2adjacency
from sknetwork.ranking import PageRank
porter = PorterStemmer()

def getTerms(text):
    terms = []
    text = text.lower()
    words = re.split(r'[\n`;\-,\s.>?:"\'\[\](){}@#+!_~&*%^=|$/<>]\s*', text) 
    #words = word_tokenize(review)
    for word in words:
        if word!='':
            terms.append(porter.stem(word))
    return terms

colldir = '20news-bydate-test'
def getFiles(colldir):
    files = []
    for dir in os.listdir(colldir):
        if dir[0]!='.':
            try:
                for f in os.listdir(colldir+'/'+dir):
                    if f[0]!='.':
                        files.append(colldir+'/'+dir+'/'+f)
            except:
                files.append(colldir+'/'+dir)
    return files

def getTfFiles(files):
    tfDocs = {}
    for i,f in enumerate(files):
        t1 = getTerms(open(f,mode='r',encoding='iso-8859-15').read())
        tfDocs[f] = t1
    return tfDocs

def getSimScore(t1, t2, cosine, vocab, idf, N, tfIdf1, tfIdf2):
    if cosine:
        allterms = set().union(*[tfIdf1,tfIdf2])
        vec1 = np.array([tfIdf1.get(term,0) for term in allterms])
        vec2 = np.array([tfIdf2.get(term,0) for term in allterms])
        return (1 - spatial.distance.cosine(vec1, vec2))
    else:
        t1set = set(t1)
        t2set = set(t2)
        return len(t1set.intersection(t2set))/len(t1set.union(t2set))

def getTfIdfDocs(files, idf, tfDocs, vocab):
    tfIdfDocs = {}
    for i,f in enumerate(files):
        t1 = tfDocs[f]
        tf1 = collections.Counter(t1)
        tfIdf1 = {}
        for term in tf1:
            tfIdf1[term] = tf1[term]*np.log2(1+(len(files)/vocab[term]['df']))
        tfIdfDocs[f] = tfIdf1
    return tfIdfDocs

def simgraph_gen(files,outfile, cosine):
    vocab, idf, N = getVocabData(files)
    #vocab, idf, N = loadStored('tfIdfVocab.json', files)
    tfDocs = getTfFiles(files)
    tfIdfDocs, tfIdf1, tfIdf2 = {}, [], []
    if cosine:
        tfIdfDocs = getTfIdfDocs(files, idf, tfDocs, vocab)
    with open(outfile,'w+') as out:
        for i,f in enumerate(files):
            #t1 = getTerms(open(f,mode='r',encoding='iso-8859-15').read())
            t1 = tfDocs[f]
            if cosine: tfIdf1 = tfIdfDocs[f]
            if len(t1)>0:
                for j in range(i+1,len(files)):
                    #t2 = getTerms(open(files[j],mode='r',encoding='iso-8859-15').read())
                    t2 = tfDocs[files[j]]
                    if cosine: tfIdf2 = tfIdfDocs[files[j]]
                    if len(t2)>0:
                        score = getSimScore(t1, t2, cosine, vocab, idf, N, tfIdf1, tfIdf2)
                        print(f.split('/')[-2]+'/'+f.split('/')[-1],files[j].split('/')[-2]+'/'+files[j].split('/')[-1],"%.4f" % score, file = out)
            #if(i==3): break
            
def getVocabData(files):
    vocab = {}
    for i,f in enumerate(files):
        #print(i)
        allTerms = getTerms(open(f,mode='r',encoding='iso-8859-15').read())
        terms = collections.Counter(allTerms)
        for term in terms:
            if term in vocab:
                vocab[term]['tf'] += terms[term]
                vocab[term]['df'] += 1
            else:
                vocab[term] = {'tf':terms[term],'df':1}
    #print(json.dumps(vocab, indent=4), file=open('tfIdfVocab.json', 'w+'))
    idf = np.array([np.log2(1+(len(files)/vocab[term]['df'])) for term in vocab])
    N = np.sum(np.array([vocab[term]['tf'] for term in vocab]))
    return vocab, idf, N

def loadStored(f, files):
    vocab = json.load(open(f))
    idf = np.array([np.log2(1+(len(files)/vocab[term]['df'])) for term in vocab])
    N = np.sum(np.array([vocab[term]['tf'] for term in vocab]))
    return vocab, idf, N

def getPgScores(outfile):
    edges = []
    mapnames = {}
    count = 0
    with open(outfile) as f:
        lines = f.readlines()
        for line in lines:
            entries = line.strip().split(' ')
            #print(entries)
            if entries[0] not in mapnames:
                mapnames[entries[0]] = count
                count += 1
            edges.append((entries[0],entries[1],float(entries[2])))
    mapnames[entries[1]] = count
    count += 1
    edges_int = [(mapnames[entry[0]],mapnames[entry[1]],entry[2]) for entry in edges]
    graph = edgelist2adjacency(edges_int, undirected=True)
    pagerank = PageRank()
    scores = pagerank.fit_transform(graph)
    pairs = {}
    for file in mapnames:
        pairs[file] = scores[mapnames[file]]
    print('prTop20: ', sorted(pairs.items(), key=lambda x: x[1], reverse=True)[:20])


cosine = 1 if sys.argv[1]=='cosine' else 0
simgraph_gen(getFiles(sys.argv[2]),sys.argv[3],cosine)
getPgScores(sys.argv[3])
# getVocabData(getFiles(sys.argv[2]))
    
#bash simgraph_gen.sh cosine shortcoll outcosineShort.txt