import os
from bs4 import BeautifulSoup as bs
import re
import json
import snappy
from stemmer import *

def indexing(directoryFiles, stopwords, xmltags, tempDir):
    p = PorterStemmer()
    inverted_index = {}
    docidint = 0
    docid_map = {}
    tags = []
    with open(xmltags, 'r') as tagsFile:
        tag = tagsFile.readline()
        tag = tagsFile.readline()
        while tag:
            tags.append(tag.split('\n')[0])
            tag = tagsFile.readline()
    docnotag = "DOCNO"
    
    if not os.path.isdir(tempDir):
        os.mkdir(tempDir)
    else:
        for f in os.listdir(tempDir):
            os.remove(os.path.join(tempDir, f))

    mapping = {}
    #1 lac
    threshold= 250*100
    #threshold = 10000000
    idxfilecounter = 0
    for filename in os.listdir(directoryFiles):
        #print(filename)
        lines = []      
        if(filename[0] != '.'):
            with open(os.path.join(directoryFiles, filename), 'r') as file:
                lines = file.readlines()
                lines = "".join(lines)
                lines = "<TEMP>"+lines+"</TEMP>"
                content = bs(lines, "xml")
                indexsize = 0
                docs=content.find_all(docnotag)
                for doc in docs:
                    docidint+=1
                    docid = doc.contents[0].strip()
                    docid_map[docidint]=docid
                    for tag in tags:
                        texts = doc.parent.find_all(tag)
                        for text in texts:
                            if(len(text.contents)>0):
                                indexed_terms = re.split(r'[\n`;,\s.:"\'\[\](){}]\s*', text.contents[0])   
                                for term in indexed_terms:
                                    if term not in stopwords:  #stopwords
                                        term = p.stem(term, 0,len(term)-1).lower()
                                        if term in inverted_index:
                                            if docidint not in inverted_index[term]:
                                                inverted_index[term].append(docidint)  
                                                indexsize += 1
                                        else:
                                            inverted_index[term]=[docidint]
                                            indexsize += 1
                                    if indexsize>threshold:
                                        indexsize = 0
                                        idxfilecounter += 1
                                        with open(tempDir+'/'+str(idxfilecounter)+".idx",'wb+') as plist:
                                            start_byte = 0
                                            for term in sorted(inverted_index):
                                                bytes_used = 0
                                                for entry in inverted_index[term]:
                                                    docidbin = entry.to_bytes(4, byteorder = "big")
                                                    plist.write(docidbin)
                                                    bytes_used+=4
                                                if term in mapping:
                                                    mapping[term].append((str(idxfilecounter), start_byte, bytes_used))  
                                                else:
                                                    mapping[term] = [(str(idxfilecounter), start_byte, bytes_used)]
                                                start_byte+=bytes_used
                                        inverted_index = {} 

    with open("indexfileTemp.dict", "w+") as dictionary:
        finalDict = {} 
        finalDict['mapping'] = mapping
        finalDict['docidmap'] = docid_map
        
        dictionary.write(json.dumps((finalDict)))

def mergePlists(plistsfile, tempDir, stopwords):
    files={}
    for filename in os.listdir(tempDir):
        if(len(filename.split(' '))==1):
                files[filename.split('.')[0]]=open(os.path.join(tempDir, filename), 'rb')
    with open(plistsfile + ".idx", "wb+") as plist, open(plistsfile + ".dict", "w+") as dictfile, open("indexfileTemp.dict", "r") as dictionary:
        startByte = 0
        bytesWritten = 0
        finalDict = {}
        oriDict = json.load(dictionary)
        dictionary = oriDict['mapping']
        docidmap = oriDict['docidmap']
        for term in sorted(dictionary):
            for lists in dictionary[term]:
                files[lists[0]].seek(lists[1])
                bytesToWrite = lists[2]
                toWrite = files[lists[0]].read(bytesToWrite)
                plist.write(toWrite)
                bytesWritten += bytesToWrite
            finalDict[term] = [startByte, bytesWritten]
            startByte += bytesWritten
            bytesWritten = 0
        nestedDict = {} 
        nestedDict['mapping'] = finalDict
        nestedDict['docidmap'] = docidmap
        nestedDict['stopwords'] = stopwords
        nestedDict['compression'] = '0'
        dictfile.write(json.dumps(nestedDict))

#c1
def compressC1(plistsfile, indexfile):
    with open(plistsfile+".idx",'rb') as binary, open(plistsfile+".dict",'r') as mapping, open(indexfile+".idx",'wb+') as c1, open(indexfile+".dict",'w+') as compressedmap:
        oriDict = json.load(mapping)
        mapping = oriDict['mapping']
        docidmap = oriDict['docidmap']
        stopwords = oriDict['stopwords']
        values = mapping.values()
        keys = mapping.keys()
        value_iterator = iter(values)
        key_iterator = iter(keys)
        val = next(value_iterator)
        key = next(key_iterator)
        previous = b'0'
        byte = binary.read(4)
        bytesRead = 0
        compressed_dict = {}
        startBit = 0
        bitsWritten = 0
        while byte:
            bytesRead += 4
            if bytesRead == val[1] + 4: 
                bytesRead = 4
                previous = b'0'
                compressed_dict[key]=[startBit,bitsWritten]
                startBit += bitsWritten
                bitsWritten = 0
                val = next(value_iterator)
                key = next(key_iterator)
            
            byte = "{:032b}".format(int.from_bytes(byte,"big"))
            s = "{:032b}".format(int(byte, 2) - int(previous, 2)).encode()
            s = s.decode()
            s = s.lstrip("0")
            if(s == ''): s = '0'
            first = 1
            while s[-7:]:
                toWrite = s[-7:]
                if first:
                    toWrite = int((("0" * (8-len(toWrite)))+ toWrite), 2)
                    c1.write(toWrite.to_bytes(1, byteorder="big"))
                    first=0
                    bitsWritten += 8
                else:
                    toWrite = int(("1" + ("0" * (7-len(toWrite)))+ toWrite), 2)
                    c1.write(toWrite.to_bytes(1, byteorder="big"))
                    bitsWritten += 8
                s=s[:-7]
            previous = byte
            byte = binary.read(4)
        nestedDict = {} 
        nestedDict['mapping'] = compressed_dict
        nestedDict['docidmap'] = docidmap
        nestedDict['stopwords'] = stopwords
        nestedDict['compression'] = '1'
        compressedmap.write(json.dumps(nestedDict))

#c2
def compressC2(plistsfile, indexfile):
    with open(plistsfile+".idx",'rb') as binary, open(plistsfile+".dict",'r') as mapping, open(indexfile+".idx",'wb+') as c2, open(indexfile+".dict",'w+') as compressedmap:
        oriDict = json.load(mapping)
        mapping = oriDict['mapping']
        docidmap = oriDict['docidmap']
        stopwords = oriDict['stopwords']
        values = mapping.values()
        keys = mapping.keys()
        value_iterator = iter(values)
        key_iterator = iter(keys)
        val = next(value_iterator)
        key = next(key_iterator)
        previous = b'0'
        byte = binary.read(4)
        bytesRead = 0
        compressed_dict = {}
        startBit = 0
        bitsWritten = 0
        while byte:
            bytesRead += 4
            if bytesRead == val[1] + 4: 
                bytesRead = 4
                previous = b'0'
                compressed_dict[key]=[startBit,bitsWritten]
                startBit += bitsWritten
                bitsWritten = 0
                val = next(value_iterator)
                key = next(key_iterator)
            
            byte = "{:032b}".format(int.from_bytes(byte,"big"))
            s = "{:032b}".format(int(byte, 2) - int(previous, 2)).encode()
            s = s.decode()
            s = s.lstrip("0")
            lensbin="{:b}".format(len(s))
            toWrite = "1"*(len(lensbin)-1)+"0"+lensbin[-(len(lensbin)-1):]+s[1:]
            if(len(toWrite) % 8 != 0): 
                toWrite = ('0'*(8 - (len(toWrite) % 8)))+toWrite
            
            bytetoWrite=toWrite[:8]
            while bytetoWrite:
                c2.write(int(bytetoWrite, 2).to_bytes(1, byteorder='big'))
                bitsWritten += 8
                toWrite=toWrite[8:]
                bytetoWrite = toWrite[:8]
            previous = byte
            byte = binary.read(4)
        nestedDict = {} 
        nestedDict['mapping'] = compressed_dict
        nestedDict['docidmap'] = docidmap
        nestedDict['stopwords'] = stopwords
        nestedDict['compression'] = '2'
        compressedmap.write(json.dumps(nestedDict))


#c3
def compressC3(decompressed, compressed):
    command = 'python -m snappy -c ' + decompressed+ '.idx ' + compressed +'.idx'
    os.system(command)
    with open(compressed+'.dict', 'w+') as dictionaryFinal, open(decompressed+'.dict', 'r') as dictori:
        dictionary = {}
        dictori = json.load(dictori)
        dictionary['compression']='3'
        dictionary['mapping'] = dictori['mapping']
        dictionary['docidmap'] = dictori['docidmap']
        dictionary['stopwords'] = dictori['stopwords']
        dictionaryFinal.write(json.dumps(dictionary))


def invidx(directoryFiles, indexfile, stopwordfile, compression, xmltags):
    tempDir = "tempFiles"
    
    stopwords = ['']
    with open(stopwordfile, 'r') as stopwordfile:
        sw = stopwordfile.readline()
        while sw:
            stopwords.append((sw.split('\n')[0]).lower())
            sw = stopwordfile.readline()
    
    indexing(directoryFiles, stopwords, xmltags, tempDir)
    plistsfile = 'plistsfile'
    
    if(compression == '0'): plistsfile = indexfile
    mergePlists(plistsfile, tempDir, stopwords)
    if(compression == '1'): compressC1(plistsfile, indexfile)
    elif(compression == '2'): compressC2(plistsfile, indexfile)
    elif(compression == '3'): compressC3(plistsfile, indexfile)
    elif(compression == '4'): print("not implemented")   
    elif(compression == '5'): print("not implemented")       

invidx(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])