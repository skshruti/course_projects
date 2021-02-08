#!/usr/bin/env python
from socket import *
import threading
import time
from operator import itemgetter
import hashlib
import csv
import matplotlib.pyplot as plt


start_time=time.time()
def collect(l, index):
   return list(map(itemgetter(index), l))

originalMD5="70a4b9f4707d258f559f91615297a3ec"
serverName='vayu.iitd.ac.in'
serverPort=80

sentOrder=[]
receivedData=[]
outfile=open("5.txt","w")

class threads(threading.Thread):
	def __init__(self, threadNo, startByte, destByte, host, fileName, no_requests):
		threading.Thread.__init__(self)
		self.threadNo=threadNo
		self.startByte=startByte
		self.destByte=destByte
		self.socket=socket(AF_INET,SOCK_STREAM)
		self.socket.settimeout(9)
		self.host=host
		self.fileName=fileName
		self.no_requests=0
	def run(self):
		self.socket.connect((self.host,serverPort))
		sentOrder.append(self.threadNo)
		response=""
		while self.startByte<self.destByte:
			try:
				if(self.no_requests<50):
					sentence="GET /"+self.fileName+" HTTP/1.1\r\nHost: "+self.host+"\r\nConnection: keep-alive\r\nRange: bytes="+str(self.startByte)+"-"+str(self.startByte+10000)+"\r\n\r\n"
					if(self.startByte+10000>=self.destByte):
						sentence="GET /"+self.fileName+" HTTP/1.1\r\nHost: "+self.host+"\r\nConnection: keep-alive\r\nRange: bytes="+str(self.startByte)+"-"+str(self.destByte-1)+"\r\n\r\n"
					#print(self.threadNo)
					#print(sentence)
					self.socket.send(sentence.encode())
					self.no_requests+=1
					self.startByte+=10001
					counter=0
					modifiedSentence=self.socket.recv(4096)
					if(modifiedSentence.decode()==''):
						self.socket.close()
						self.socket=socket(AF_INET,SOCK_STREAM)
						self.socket.connect((self.host,serverPort))
						self.no_requests-=1
						self.startByte-=10001
						continue
					while counter<=10000 and modifiedSentence.decode()!='':
						#print("ACHHA", modifiedSentence)
						splitResponse=modifiedSentence.decode().split('\r\n\r\n')
						if(len(splitResponse)==2):
							response=response+splitResponse[1]
							counter+=len(splitResponse[1])
							outfile.write(splitResponse[1])
						else:
							response=response+splitResponse[0]
							counter+=len(splitResponse[0])
							outfile.write(splitResponse[0])
						modifiedSentence=self.socket.recv(4096)
				else:
					self.socket.close()
					self.socket=socket(AF_INET,SOCK_STREAM)
					self.socket.settimeout(9)
					self.socket.connect((self.host,serverPort))
					self.no_requests=0
					#print("OOH")
			except:
				continue
		receivedData.append((self.threadNo,response))
		self.socket.close()

urls=[]
no_threads=0
inpFile=input("Enter csv filename::\n")
with open(inpFile, newline='') as csvfile:
	csv_reader=csv.reader(csvfile)
	for line in csv_reader:
		no_threads+=int(line[1])
		urls.append(line)

threadList=[]
startByte=0
bytes_per_thread=int(6488666/no_threads)+1
lock=threading.Lock()

j=0
current=0
for i in range(no_threads):
	startByte=i*bytes_per_thread
	if j<int(urls[current][1]):
		j+=1
	else:
		current+=1
		j=0
	url=urls[current][0]
	content=(url.split('//'))[1]
	host=content.split('/')[0]
	fileName=content.split('/')[1]
	thread=threads(i,startByte,startByte+bytes_per_thread,host,fileName,0)
	thread.start()
	threadList.append(thread)

for i in range(len(threadList)):
	threadList[i].join()

outfile.close()
writeTo=open("6.txt","w")
#for sentNumber in sentOrder:
for threadID in range(no_threads):
	number=(collect(receivedData,0).index(threadID))
	writeTo.write(receivedData[number][1])
writeTo.close()

checkfile=open("6.txt")
downloadedMD5=hashlib.md5()
portion=checkfile.read(4096)
while portion:
	for data in portion:
		downloadedMD5.update(data.encode())
	portion=checkfile.read(4096)
print(downloadedMD5.hexdigest())
if originalMD5==downloadedMD5.hexdigest():
	print("Correct MD5 downloaded.")
else:
	print("oops! something is wrong")
checkfile.close()
#10->360
#100->