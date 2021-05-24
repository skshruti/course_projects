import numpy as np
from matplotlib import pyplot as plt
import cv2
import os
import math

string="colored.jpg"

image = cv2.imread(string)
image=cv2.resize(image,(50,50)) 

colorsFound=[]
colorsFoundMedian=[]
redMin=256
blueMin=256
greenMin=256
redMax=-1
blueMax=-1
greenMax=-1

for x in range(image.shape[0]):
	for y in range(image.shape[1]):
		print(x,y)
		pixel=image[x,y]
		index=-1
		for i in range(len(colorsFound)):
			if((colorsFound[i][0]==pixel).all()):
				index=i
				value=colorsFound[i][1]+1
				colorsFound[i]=(pixel,value)
		if index==-1:
			colorsFound.append((image[x,y],1))
			colorsFoundMedian.append(image[x,y])
			if(pixel[0]>blueMax): blueMax=pixel[0]
			if(pixel[1]>greenMax): greenMax=pixel[1]
			if(pixel[2]>redMax): redMax=pixel[2]
			if(pixel[0]<blueMin): blueMin=pixel[0]
			if(pixel[1]<greenMin): greenMin=pixel[1]
			if(pixel[2]<redMin): redMin=pixel[2]

print(len(colorsFound))
print(len(colorsFoundMedian))

def sortHelpPopularity(e):
	return e[1]

def closestColor(color, colors):
	minDist=999999999
	closestOne=color
	for i in range(len(colors)):
		dist=math.sqrt((int(colors[i][0])-int(color[0]))**2 + (int(colors[i][1])-int(color[1]))**2 + (int(colors[i][2])-int(color[2]))**2)
		if(dist<minDist):
			minDist=dist
			closestColor=colors[i]
	return closestColor



def popularity(k):
	image = cv2.imread(string)
	#image=cv2.resize(image,(50,50)) 
	colorsFound.sort(key=sortHelpPopularity)
	i=len(colorsFound)
	selectedColors=[]
	for j in range(k):
		i=i-1
		color=(colorsFound[i][0][0],colorsFound[i][0][1],colorsFound[i][0][2])
		print(color)
		selectedColors.append(color)

	for x in range(image.shape[0]):
		for y in range(image.shape[1]):
			temp=image[x,y]
			color=(temp[0],temp[1],temp[2])
			image[x,y]=closestColor(color,selectedColors)

	cv2.imshow("img",image)
	cv2.waitKey(0)
	name = string.split('.')
	finalName=name[0]+str(k)+'Popularity.jpg'
	cv2.imwrite(finalName, image)



def sortHelpMedian(e):
	rangeBlue=blueMax-blueMin
	rangeGreen=greenMax-greenMin
	rangeRed=redMax-redMin
	if((rangeBlue>rangeGreen) and (rangeBlue>rangeRed)): return e[0]
	elif(rangeGreen>rangeBlue and rangeGreen>rangeRed): return e[1]
	else: return e[2]

def medianCut(k):
	image = cv2.imread(string)
	image=cv2.resize(image,(50,50)) 

	colorsFoundMedian.sort(key=sortHelpMedian)
	nBuckets=1
	buckets=[colorsFoundMedian]
	while nBuckets<k:
		current=len(buckets)
		for i in range(current):
			popped=buckets.pop(0)
			buckets.append(popped[:int(len(popped)/2)])
			buckets.append(popped[int(len(popped)/2):])
		nBuckets*=2

	selectedColors=[]
	for i in range(len(buckets)):
		blue=0
		green=0
		red=0
		for j in range(len(buckets[i])):
			blue+=buckets[i][j][0]**2
			green+=buckets[i][j][1]**2
			red+=buckets[i][j][2]**2
		average=(int(math.sqrt(blue/len(buckets[i]))),int(math.sqrt(green/len(buckets[i]))),int(math.sqrt(red/len(buckets[i]))))
		selectedColors.append(average)

	print(len(selectedColors))
	for x in range(image.shape[0]):
		for y in range(image.shape[1]):
			temp=image[x,y]
			color=(temp[0],temp[1],temp[2])
			image[x,y]=closestColor(color,selectedColors)

	cv2.imshow("img",image)
	cv2.waitKey(0)
	name = string.split('.')
	finalName=name[0]+str(k)+'medianCut.jpg'
	cv2.imwrite(finalName, image)



def floyd(k):
	image = cv2.imread(string)
	image=cv2.resize(image,(50,50)) 

	colorsFoundMedian.sort(key=sortHelpMedian)
	nBuckets=1
	buckets=[colorsFoundMedian]
	while nBuckets<k:
		current=len(buckets)
		for i in range(current):
			popped=buckets.pop(0)
			buckets.append(popped[:int(len(popped)/2)])
			buckets.append(popped[int(len(popped)/2):])
		nBuckets*=2

	selectedColors=[]
	for i in range(len(buckets)):
		blue=0
		green=0
		red=0
		for j in range(len(buckets[i])):
			blue+=buckets[i][j][0]**2
			green+=buckets[i][j][1]**2
			red+=buckets[i][j][2]**2
		average=(int(math.sqrt(blue/len(buckets[i]))),int(math.sqrt(green/len(buckets[i]))),int(math.sqrt(red/len(buckets[i]))))
		selectedColors.append(average)

	print(len(selectedColors))
	for x in range(image.shape[0]):
		for y in range(image.shape[1]):
			temp=image[x,y]
			color=(temp[0],temp[1],temp[2])
			image[x,y]=closestColor(color,selectedColors)
			error=((image[x,y][0]-color[0]),(image[x,y][1]-color[1]),(image[x,y][2]-color[2]))
			for i in range(3):
				try:
					image[x,y+1][i]=(image[x,y+1][i]+(error[i]*5/16))
				except IndexError:
					pass
				try:
					image[x+1,y][i]=image[x+1,y][i]+(error[i]*7/16)
				except IndexError:
					pass
				try:
					image[x+1,y+1][i]=image[x+1,y+1][i]+(error[i]*3/16)
				except IndexError:
					pass
				try:
					image[x-1,y+1][i]=image[x+1,y][i]+(error[i]/16)
				except IndexError:
					pass
		
	#cv2.imshow("img",image)
	#cv2.waitKey(0)
	changedimg = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
	image=cv2.resize(image,(300,300)) 
	cv2.imshow("img",image)
	cv2.waitKey(0)
	name = string.split('.')
	finalName=name[0]+str(k)+'floyd.jpg'
	cv2.imwrite(finalName, image)


popularity(4)
medianCut(256)
floyd(256)
