import os
from bs4 import BeautifulSoup as bs
import re
import json
import snappy
from stemmer import *

p = PorterStemmer()

#c1 decoding
def findDocsC0(queryfile, resultfile, indexfile, dictfile):
    with open(queryfile,'r') as queries, open(resultfile,'w+') as outfile, open(indexfile,'rb') as c0, open(dictfile,'r') as compressedmap:
        oriDict = json.load(compressedmap)
        mapping = oriDict['mapping']
        docid_map = oriDict['docidmap']
        stopwords = oriDict['stopwords']
        query = queries.readline()
        qid = -1
        while query:
            qid += 1
            termlisttemp = (query.split('\n')[0]).split(' ')
            termlist = []
            for term in termlisttemp:
                if term not in stopwords: termlist.append(term)
            termlist = [p.stem(termlist[i], 0,len(termlist[i])-1).lower() for i in range(len(termlist))]
            doclists = []
            intList = []
            for term in termlist:
                if term in mapping.keys():
                    startBit = mapping[term][0]
                    bytesToRead = (mapping[term][1])/4
                    c0.seek(startBit)
                    for i in range(int(bytesToRead)):
                        value = int.from_bytes(c0.read(4), "big")
                        intList.append(value)
                    intList = [docid_map[str(intList[i])] for i in range(0, len(intList))]
                    doclists.append(intList)
                    intList=[]
                else:
                    doclists.append([])
            queryresult = list(set(doclists[0]).intersection(*doclists)) if len(doclists)>0 else []
            for doc in queryresult:
                outfile.write('Q'+str(qid)+' '+doc+' 1.0\n')
            query = queries.readline()

#c1 decoding
def findDocsC1(queryfile, resultfile, indexfile, dictfile):
    p = PorterStemmer()
    with open(queryfile,'r') as queries, open(resultfile,'w+') as outfile, open(indexfile,'rb') as c1, open(dictfile,'r') as compressedmap:
        oriDict = json.load(compressedmap)
        mapping = oriDict['mapping']
        docid_map = oriDict['docidmap']
        stopwords = oriDict['stopwords']
        query = queries.readline()
        qid = -1
        while query:
            qid += 1
            termlisttemp = (query.split('\n')[0]).split(' ')
            termlist = []
            for term in termlisttemp:
                if term not in stopwords: termlist.append(term)
            termlist = [p.stem(termlist[i], 0,len(termlist[i])-1).lower() for i in range(len(termlist))]
            doclists = []
            intList = []
            for term in termlist:
                if term in mapping.keys():
                    startByte = mapping[term][0] / 8
                    bitsLength = mapping[term][1]
                    c1.seek(int(startByte))
                    bytesToRead = bitsLength/8
                    binary = ''
                    for i in range(int(bytesToRead)):
                        byte = c1.read(1)
                        byte = "{:08b}".format(int.from_bytes(byte,"big"))
                        if(byte[0] == '0'):
                            binary = binary + byte[1:]
                            intList.append(int(binary,2))
                            binary = ''
                        else:
                            binary = binary + byte[1:]
                    intList = [sum(intList[:i+1]) for i in range(0, len(intList))]
                    intList = [docid_map[str(intList[i])] for i in range(0, len(intList))]
                    doclists.append(intList)
                    intList=[]
                else:
                    doclists.append([])
            queryresult = list(set(doclists[0]).intersection(*doclists)) if len(doclists)>0 else []
            for doc in queryresult:
                outfile.write('Q'+str(qid)+' '+doc+' 1.0\n')
            query = queries.readline()

#c1 decoding
def findDocsC2(queryfile, resultfile, indexfile, dictfile):
    p = PorterStemmer()
    with open(queryfile,'r') as queries, open(resultfile,'w+') as outfile, open(indexfile,'rb') as c1, open(dictfile,'r') as compressedmap:
        oriDict = json.load(compressedmap)
        mapping = oriDict['mapping']
        docid_map = oriDict['docidmap']
        stopwords = oriDict['stopwords']
        query = queries.readline()
        qid = -1
        while query:
            qid += 1
            termlisttemp = (query.split('\n')[0]).split(' ')
            termlist = []
            for term in termlisttemp:
                if term not in stopwords: termlist.append(term)
            termlist = [p.stem(termlist[i], 0,len(termlist[i])-1).lower() for i in range(len(termlist))]
            doclists = []
            intList = []
            for term in termlist:
                if term in mapping.keys():
                    startByte = mapping[term][0] / 8
                    bitsLength = mapping[term][1]
                    c1.seek(int(startByte))
                    bytesToRead = bitsLength/8
                    startByte = mapping[term][0] / 8
                    bytesToRead = mapping[term][1] / 8
                    c1.seek(int(startByte))
                    plist = ''
                    for i in range(int(bytesToRead)):
                        byte = c1.read(1)
                        plist=plist+("{:08b}".format(int.from_bytes(byte, "big")))
                    postingsList = plist
                    
                    while postingsList:
                        if(postingsList[:9] == '000000010'): 
                            intList.append(1)
                            postingsList = postingsList[8:]
                        else:
                            postingsList = postingsList.lstrip("0")
                            unary = postingsList.split('0')[0]
                            binary = "0".join(postingsList.split('0')[1:])
                            lenlenx = len(unary)+1
                            lenxbin = "1"+binary[:(lenlenx-1)]
                            lenx = int(lenxbin, 2)
                            xbin = "1"+binary[(lenlenx-1):lenlenx-1+lenx-1]
                            x = int(xbin,2)
                            postingsList = binary[lenlenx-1+lenx-1:]
                            intList.append(x)
                    intList = [sum(intList[:i+1]) for i in range(0, len(intList))]
                    intList = [docid_map[str(intList[i])] for i in range(0, len(intList))]
                    doclists.append(intList)
                    intList=[]
                else:
                    doclists.append([])
            queryresult = list(set(doclists[0]).intersection(*doclists)) if len(doclists)>0 else []
            for doc in queryresult:
                outfile.write('Q'+str(qid)+' '+doc+' 1.0\n')
            query = queries.readline()

def decompressC3(decompressed, compressed):
    command = 'python -m snappy -d ' + compressed+ '.idx ' + decompressed +'.idx'
    os.system(command)

def findDocsC3(queryfile, resultfile, indexfile, dictfile):
    indexfilename = indexfile.split('.')[0]
    decompressC3('decompressed', indexfilename)
    findDocsC0(queryfile, resultfile, 'decompressed.idx', dictfile)

def searchquery(queryfile, resultfile, indexfile, dictfile):
    dictionary = open(dictfile, 'r')
    dictionary = json.load(dictionary)
    compression = int(dictionary['compression'])
    if compression == 0: findDocsC0(queryfile,resultfile,indexfile,dictfile)
    elif compression == 1: findDocsC1(queryfile,resultfile,indexfile,dictfile)
    elif compression == 2: findDocsC2(queryfile,resultfile,indexfile,dictfile)
    elif compression == 3: findDocsC3(queryfile,resultfile,indexfile,dictfile)

searchquery(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])