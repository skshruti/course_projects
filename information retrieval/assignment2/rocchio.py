import numpy as np
import pandas as pd
import os
import json
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.stem import LancasterStemmer
from nltk.corpus import stopwords
from bs4 import BeautifulSoup as bs
import time
import collections
from scipy import spatial
import re
import sys
import math

topicsfile = sys.argv[1]
topqrelsfile = sys.argv[2]
direc = sys.argv[3]
outfile = sys.argv[4]

# direc = 'colldir'
# metadatafile = direc+'/'+'metadata.csv'
# qrelsfile = './col764-ass2-release/t40-qrels.txt'
# topqrelsfile = './col764-ass2-release/t40-top-100.txt'
# topicsfile = './col764-ass2-release/covid19-topics.xml'


evaluate = 0

#initialise nltk
porter = PorterStemmer()
lancaster = LancasterStemmer()
stopwordsList = set(stopwords.words('english'))
metadatafile = direc+'/'+'metadata.csv'

def getTerms(review):
    terms = []
    review = review.lower()
    words = re.split(r'[\n`;,\s.:"\'\[\](){}]\s*', review) 
    #words = word_tokenize(review)
    for word in words:
        if (word not in stopwordsList):
            terms.append(porter.stem(word))
            #terms.append(lancaster.stem(word))
    return terms

# read data given
metadatatemp = pd.read_csv(metadatafile)
metadata = {}
for i in range(len(metadatatemp)):
    metadata[metadatatemp['cord_uid'][i]] = {
        'pmc_json' : metadatatemp['pmc_json_files'][i],
        'pdf_json' : metadatatemp['pdf_json_files'][i],
        'abstract' : metadatatemp['abstract'][i],
        'title' : metadatatemp['title'][i],
    }
# metadata = json.load(open('../newmeta.json'))

if evaluate:
    qrelsfile = '../col764-ass2-release/t40-qrels.txt'
    # qrelsfile = '../queriesdirshort/t40-qrels.txt'
    qrels = {}
    with open(qrelsfile,'r') as f:
        for line in f.readlines():
            split = line.split(' ')
            if len(split)==4:
                if split[0] not in qrels:
                    qrels[split[0]] = {split[2]: split[3].split('\n')[0]}
                else:
                    qrels[split[0]][split[2]]=split[3].split('\n')[0]

topqrels = {}
allRelDocs = set()
with open(topqrelsfile,'r') as f:
    for line in f.readlines():
        split = line.split(' ')
        if len(split)==6:
            allRelDocs.add(split[2])
            if split[0] not in topqrels:
                topqrels[split[0]] = {split[3]: split[2]}
            else:
                topqrels[split[0]][split[3]]=split[2]

queries = {}
tag = 'query'
with open(topicsfile,'r') as f:
    lines = f.readlines()
    lines = "".join(lines)
    content = bs(lines, "xml")
    topics = content.find_all('topic')
    count = 1
    for topic in topics:
        query = topic.find(tag)
        queries[str(count)] = {'ori': getTerms(query.contents[0])}
        count += 1


#generate TF-IDF 
def getVocab(source):
    #source->metadata/allRelDocs
    count = 0
    vocab = {}
    for doc in source:
        count+=1
        #print(count)
        abstract, title, body = [],[],[]
        if type(metadata[doc]['abstract']) == str:
            abstract = getTerms(metadata[doc]['abstract'])
        if type(metadata[doc]['title']) == str:
            title = getTerms(metadata[doc]['title'])
        val = ''
        if type(metadata[doc]['pmc_json']) == str:
            val = 'pmc_json'
        elif type(metadata[doc]['pdf_json']) == str:
            val = 'pdf_json'
        if val!='':
            files = metadata[doc][val].split(';')
            files = [file.strip() for file in files]
            body = []
            for file in files:
                with open(direc+'/'+file, 'r') as f:
                    content = json.load(f)
                    for section in content['body_text']:
                        body = np.hstack([body,getTerms(section['text'])])
        allTerms = np.hstack([body, abstract, title])
        terms = collections.Counter(allTerms)
        for term in terms:
            if term in vocab:
                vocab[term]['tf'] += terms[term]
            else:
                vocab[term] = {'tf':terms[term],'df':1}
    #print(json.dumps(vocab, indent=4), file=open('stored/metadatatfidfLancasterNohup.json', 'w+'))
    print('vocab found')
    return vocab

def getTfVecDoc(doc, vocab):
    abstract, title, body = [],[],[]
    if type(metadata[doc]['abstract']) == str:
        abstract = getTerms(metadata[doc]['abstract'])
    if type(metadata[doc]['title']) == str:
        title = getTerms(metadata[doc]['title'])
    val = ''
    if type(metadata[doc]['pmc_json']) == str:
        val = 'pmc_json'
    elif type(metadata[doc]['pdf_json']) == str:
        val = 'pdf_json'
    if val!='':
        files = metadata[doc][val].split(';')
        files = [file.strip() for file in files]
        body = []
        for file in files:
            with open(direc+'/'+file, 'r') as f:
                content = json.load(f)
                for section in content['body_text']:
                    body = np.hstack([body,getTerms(section['text'])])
    allTerms = np.hstack([body, abstract, title])
    tf = collections.Counter(allTerms)
    dtf = [1 + np.log2(tf[term]) if term in tf else 0 for term in vocab]
    #print(len(allTerms),len(tf),len(dtf))
    return dtf

def getSimScores(qtf,qopt,query,tfVecDocs,idf,N):
    scoresOri, scoresOpt = [], {}
    for rank in topqrels[query]:
        tfVecDoc = tfVecDocs[topqrels[query][rank]]
        tfIdfVecDoc = tfVecDoc*np.log2(N/idf)
        tfIdfqopt = qopt*np.log2(N/idf)
        scoresOpt[topqrels[query][rank]] = 1 - spatial.distance.cosine(tfIdfVecDoc, tfIdfqopt)
    rankedDocs = sorted(scoresOpt, key = lambda i: scoresOpt[i], reverse = True)
    optResults = {}
    for val in rankedDocs:
        optResults[val] = scoresOpt[val]
    return scoresOri, rankedDocs, optResults

def rocchio(alpha, beta, N, evaluate):
    with open(outfile,'w+') as f:
        idf = np.array([idfs[term]['df'] for term in vocab])
        ndcgs = {}
        logarr = [np.log2(i+2) for i in range(100)]
        tfVecDocs = {}
        meanap = 0
        meanapori = 0
        temp = 0
        mrr = 0
        report = [0,0,0]
        reportori = [0,0,0]
        for query in queries:
            temp += 1
            #if(temp>2): break
            qterms = queries[query]['ori']
            print(query)
            tf = collections.Counter(qterms)
            qtf = np.array([1 + np.log2(tf[term]) if term in tf else 0 for term in vocab])
            
            ideal = {}
            
            sigmadtf = np.array([0 for term in vocab])
            for rank in topqrels[query]:
                doc = topqrels[query][rank]
                tfVecDoc = np.array(getTfVecDoc(doc, vocab))
                tfVecDocs[doc] = tfVecDoc
                sigmadtf = sigmadtf + tfVecDoc
                if evaluate: ideal[doc] = int(qrels[query][doc]) if doc in qrels[query] else 0
                
            qopt = alpha*qtf + (beta*sigmadtf)/100
            ori, rankedDocsOpt, optResults = getSimScores(qtf,qopt,query,tfVecDocs,idf,N)

            for i in range(len(rankedDocsOpt)):
                f.write(query+' Q0 '+rankedDocsOpt[i]+' '+str(i+1)+' '+str(optResults[rankedDocsOpt[i]])+' shruti\n')

            if evaluate:               
                topDocs = [doc for doc in ideal if ideal[doc]==2]
                ideal = sorted(ideal, key = lambda i: ideal[i], reverse = True)
                gideal = np.array([int(qrels[query][doc]) if doc in qrels[query] else 0 for doc in ideal])
                dcgideal = np.array([np.sum([gideal[:k+1]])/logarr[k] for k in range(len(gideal))])    
                
                #old ranks
                g = np.array([int(qrels[query][topqrels[query][rank]]) if topqrels[query][rank] in qrels[query] else 0 for rank in topqrels[query]])
                dcg = np.array([np.sum([g[:k+1]])/logarr[k] for k in range(len(g))])
                ndcgori5 = (dcg/dcgideal)
                reportori[0]+=0 if math.isnan (ndcgori5[5]) else ndcgori5[5]
                reportori[1]+=0 if math.isnan (ndcgori5[5]) else ndcgori5[10]
                reportori[2]+=0 if math.isnan (ndcgori5[5]) else ndcgori5[15]

                #new ranks
                g = np.array([int(qrels[query][doc]) if doc in qrels[query] else 0 for doc in rankedDocsOpt])
                dcg = np.array([np.sum([g[:k+1]])/logarr[k] for k in range(len(g))])
                ndcgs[query] = dcg/dcgideal
                #print('new:', ndcgnew5)
                #print(ndcgs[query][5], ndcgs[query][10], ndcgs[query][15])
                #print(ndcgnew5-ndcgori5)
                report[0]+=0 if math.isnan (ndcgs[query][5]) else ndcgs[query][5]
                report[1]+=0 if math.isnan (ndcgs[query][5]) else ndcgs[query][10]
                report[2]+=0 if math.isnan (ndcgs[query][5]) else ndcgs[query][15]
                #print(reportori, report)
                avgp = 0
                avgpori = 0
                results = []
                resultsori = []
                mrrq = -1
                #rankedDocsOpt = list(topqrels[query].values())
                for i in range(len(rankedDocsOpt)):
                    if(rankedDocsOpt[i] in topDocs and mrrq == -1): mrrq = 1/(i+1)
                    results.append(qrels[query].get(rankedDocsOpt[i],0)=='2')
                    prej = np.sum(np.array(results))/len(results)
                    avgp += prej
                    resultsori.append(qrels[query].get(rankedDocsOpt[i],0)=='2' or qrels[query].get(rankedDocsOpt[i],0)=='1')
                    prejori = np.sum(np.array(resultsori))/len(resultsori)
                    avgpori += prejori
                meanap += avgp/100
                meanapori += avgpori/100
                #print(meanap, meanapori)
                if mrrq!=-1: mrr += mrrq 


        meanap /= len(queries) 
        meanapori /= len(queries)
        if evaluate: 
            print(np.array(report)/len(queries))
            print('MRR: ', mrr/(temp-1), 'MAP2: ', meanap, 'MAP12: ', meanapori)

idfs = getVocab(metadata)
vocab = getVocab(allRelDocs)

# idfs = json.load(open('stored/metadatatfidfPorter.json'))
# vocab = json.load(open('stored/vocabRelDocsPorter.json'))

#bash rocchio_rerank.sh ../col764-ass2-release/covid19-topics.xml ../col764-ass2-release/t40-top-100.txt ../colldir ../outfiles/rocchio.out
#bash rocchio_rerank.sh ../queriesdirshort/covid19-topics.xml ../queriesdirshort/t40-top-100.txt ../colldir ../outfiles/rocchio.out

rocchio(1,0,len(metadata), evaluate)