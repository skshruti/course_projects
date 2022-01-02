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
topicsfile = sys.argv[2]
topqrelsfile = sys.argv[3]
direc = sys.argv[4]
outfile = sys.argv[5]
expansions = sys.argv[6]
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
    #qrelsfile = '../queriesdirshort/t40-qrels.txt'
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
        print(count)
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
    #print(json.dumps(vocab, indent=4), file=open('./metadatatfidf.json', 'w+'))
    print('vocab found')
    return vocab

def getTfDoc(doc):
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
    return tf

def rm(mu, rm1, evaluate):
    with open(outfile,'w+') as f, open(expansions,'w+') as e:
        tfVecDocs = {}
        meanap = 0
        meanapori = 0
        tfDocs = {}
        results = {}
        ndcgs = {}
        logarr = [np.log2(i+2) for i in range(100)]
        qcount = 0
        mrr = 0
        report = [0,0,0]
        reportori = [0,0,0]
        for query in queries:
            qcount += 1 
            #if(qcount > 5): break
            qterms = queries[query]['ori']
            print(query)
            tf = collections.Counter(qterms)
            probqdoc = {}
            ideal = {}
            pwq = {}

            #calculating p(w,q)
            if rm1:
                for rank in topqrels[query]:
                    doc = topqrels[query][rank]
                    if evaluate: ideal[doc] = int(qrels[query][doc]) if doc in qrels[query] else 0
                    tfDoc = getTfDoc(doc)
                    tfDocs[doc] = tfDoc
                    pq = 1
                    for qterm in qterms:
                        pt = (tfDoc.get(qterm,0) + ((mu*metadataColl[qterm]['tf'])/lenColl))/(len(tfDoc) + mu)
                        pq *= pt
                    probqdoc[doc] = pq

                    for word in vocab:
                        if word in pwq:
                            pwq[word] += (tfDoc.get(word,0) + ((mu*metadataColl[word]['tf'])/lenColl))/(len(tfDoc) + mu)*pq
                        else:
                            pwq[word] = (tfDoc.get(word,0) + ((mu*metadataColl[word]['tf'])/lenColl))/(len(tfDoc) + mu)*pq
            
            else:
                pt = {}
                for rank in topqrels[query]:
                    doc = topqrels[query][rank]
                    if evaluate: ideal[doc] = int(qrels[query][doc]) if doc in qrels[query] else 0
                    tfDoc = getTfDoc(doc)
                    tfDocs[doc] = tfDoc
                    pq = 1
                    for qterm in qterms:
                        pt[(qterm, doc)] = (tfDoc.get(qterm,0) + ((mu*metadataColl[qterm]['tf'])/lenColl))/(len(tfDoc) + mu)
                        pq *= (pt[(qterm, doc)]**tf.get(qterm,0))
                    probqdoc[doc] = pq

                for word in vocab:
                    pw = np.sum([(tfDocs[topqrels[query][rank]].get(word,0) + ((mu*metadataColl[word]['tf'])/lenColl))/(len(tfDocs[topqrels[query][rank]]) + mu) for rank in topqrels[query]])
                    for qterm in qterms:
                        pqtermw = 0
                        for rank in topqrels[query]:
                            doc = topqrels[query][rank]
                            pqtermw += ((tfDocs[doc].get(qterm,0)/len(tfDocs[doc]))*pt[(qterm, doc)])/pw
                        if word in pwq:
                            pwq[word] *= pqtermw
                        else:
                            pwq[word] = pqtermw*pw

            top20words = sorted(pwq, key = lambda i: pwq[i])[:20]
            e.write(query+' : ')
            for word in top20words:
                e.write(word+' ')
            e.write('\n')

            #scaleC = 1/np.sum([tfDoc.get(word,0)/len(tfDoc) for word in top20words])
            #KL divergence
            kldoc = {}
            for rank in topqrels[query]:
                doc = topqrels[query][rank]
                tfDoc = tfDocs[doc]
                temp = 0
                for word in top20words:
                    #temp += pwq[word]*np.log((tfDoc.get(word,0)*scaleC) + ((mu*metadataColl[word]['tf'])/lenColl))/(20 + mu)
                    temp += pwq[word]*np.log((tfDoc.get(word,0)) + ((mu*metadataColl[word]['tf'])/lenColl))/(len(tfDoc) + mu)
                kldoc[doc] = temp

            #ranked = sorted(probqdoc, key = lambda i: probqdoc[i], reverse = True)
            if rm1: 
                ranked = sorted(kldoc, key = lambda i: kldoc[i])
            else:
                ranked = sorted(kldoc, key = lambda i: kldoc[i], reverse=True)
           
            for i in range(len(ranked)):
                f.write(query+' Q0 '+ranked[i]+' '+str(i+1)+' '+str(probqdoc[ranked[i]])+' shruti\n')

            if evaluate: 
                topDocs = [doc for doc in ideal if ideal[doc]==2]
                ideal = sorted(ideal, key = lambda i: ideal[i], reverse = True)
                gideal = np.array([int(qrels[query][doc]) if doc in qrels[query] else 0 for doc in ideal])
                dcgideal = np.array([np.sum([gideal[:k+1]])/logarr[k] for k in range(len(gideal))])    
                #print('ideal:',ideal[:15])
                #old ranks
                g = np.array([int(qrels[query][topqrels[query][rank]]) if topqrels[query][rank] in qrels[query] else 0 for rank in topqrels[query]])
                dcg = np.array([np.sum([g[:k+1]])/logarr[k] for k in range(len(g))])
                ndcgori5 = (dcg/dcgideal)
                reportori[0]+=0 if math.isnan (ndcgori5[5]) else ndcgori5[5]
                reportori[1]+=0 if math.isnan (ndcgori5[5]) else ndcgori5[10]
                reportori[2]+=0 if math.isnan (ndcgori5[5]) else ndcgori5[15]

                #new ranks
                g = np.array([int(qrels[query][doc]) if doc in qrels[query] else 0 for doc in ranked])
                dcg = np.array([np.sum([g[:k+1]])/logarr[k] for k in range(len(g))])
                ndcgs[query] = dcg/dcgideal
                #print(ndcgs[query][5], ndcgs[query][10], ndcgs[query][15])
                report[0]+=0 if math.isnan (ndcgs[query][5]) else ndcgs[query][5]
                report[1]+=0 if math.isnan (ndcgs[query][5]) else ndcgs[query][10]
                report[2]+=0 if math.isnan (ndcgs[query][5]) else ndcgs[query][15]
                # print(reportori, report)
                # print((ndcgs[query]-ndcgori5)[:5])
                avgp = 0
                avgpori = 0
                results = []
                resultsori = []
                mrrq = -1
                for i in range(len(ranked)):
                    if(ranked[i] in topDocs and mrrq == -1): mrrq = 1/(i+1)
                    results.append(qrels[query].get(ranked[i],0)=='2')
                    prej = np.sum(np.array(results))/len(results)
                    avgp += prej
                    resultsori.append(qrels[query].get(ranked[i],0)=='2' or qrels[query].get(ranked[i],0)=='1')
                    prejori = np.sum(np.array(resultsori))/len(resultsori)
                    avgpori += prejori
                meanap += avgp/100
                meanapori += avgpori/100
                if mrrq!=-1: 
                    mrr += mrrq
                    #print(mrr) 

        if evaluate: 
            print(np.array(report)/len(queries))
            print('MRR only: ', mrr, 'MRR: ', mrr/len(queries), 'MAP2: ', meanap/len(queries), 'MAP12: ', meanapori/len(queries))

metadataColl = getVocab(metadata)
vocab = getVocab(allRelDocs)

# metadataColl = json.load(open('stored/metadatatfidfPorter.json'))
# vocab = json.load(open('stored/vocabRelDocsPorter.json'))

lenColl = len(metadataColl)

#bash lm_rerank.sh rm1 ../col764-ass2-release/covid19-topics.xml ../col764-ass2-release/t40-top-100.txt ../colldir ../outfiles/lm.out ../outfiles/exp.out
#bash lm_rerank.sh rm1 ../queriesdirshort/covid19-topics.xml ../queriesdirshort/t40-top-100.txt ../colldir ../outfiles/lm.out ../outfiles/exp.out

rm1 = 1 if sys.argv[1]=='rm1' else 0
rm(2,rm1,evaluate)