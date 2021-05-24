import numpy as np
from matplotlib import pyplot as plt
import cv2
import os
import math
import random

def printt(a):
 for i in range(len(a)):
   print(a[i])

def ispresent(a,x):
  for i in range(len(a)):
     if(a[i] == x):
       return True
  return False

def find_stddev(arr,rowstart,rowend,colstart,colend,num):
  sum = 0
  num = 0
  for i in range(rowstart,rowend+1):
     for j in range(colstart,colend+1):
        sum += (arr[i][j][0]-num)**2
        num += 1
  if(num == 0):
     return 0
  else:
     std_dev = math.sqrt(sum/num)
     return std_dev
     
def convert_to_labspace(bgr_colorspresent):
  root2 = math.sqrt(2)
  root3 = math.sqrt(3)
  root6 = math.sqrt(6)
  height = len(bgr_colorspresent)
  width = len(bgr_colorspresent[0])
  lab_space = []
  for i in range(height):
    row = []
    for j in range(width):
       B = bgr_colorspresent[i][j][0]
       G = bgr_colorspresent[i][j][1]
       R = bgr_colorspresent[i][j][2]
       L = (0.3811)*R + (0.5783)*G + (0.0402)*B
       M = (0.1967)*R + (0.7244)*G + (0.0782)*B
       S = (0.0241)*R + (0.1288)*G + (0.8444)*B
       l = (L+M+S)/root3
       alpha = (L+M-2*S)/root6
       beta = (L-M)/root2
       row.append((l,alpha,beta))
    lab_space.append(row)
  return lab_space
  
"""
def convert_to_labspace(bgr_colorspresent):
  root2 = math.sqrt(2)
  root3 = math.sqrt(3)
  root6 = math.sqrt(6)
  lab_space = []
  for i in range(len(bgr_colorspresent)):
     B = bgr_colorspresent[i][0]
     G = bgr_colorspresent[i][1]
     R = bgr_colorspresent[i][2]
     L = (0.3811)*R + (0.5783)*G + (0.0402)*B
     M = (0.1967)*R + (0.7244)*G + (0.0782)*B
     S = (0.0241)*R + (0.1288)*G + (0.8444)*B
     
     if(L<1) : L = 1
     if(M<1) : M = 1
     if(S<1) : S = 1
     #L = math.log10(L)
     #M = math.log10(M)
     #S = math.log10(S)
     l = (L+M+S)/root3
     alpha = (L+M-2*S)/root6
     beta = (L-M)/root2
     lab_space.append((l,alpha,beta))
  return lab_space
"""

def finding_colors(source):
  height = source.shape[0]
  width = source.shape[1]
  colorspresent = []
  for i in range(height):
     row = []
     for j in range(width):
        color = source[i,j]
        row.append((color[0],color[1],color[2]))
     colorspresent.append(row)
  return colorspresent
  
"""
def finding_colors(source):
  height = source.shape[0]
  width = source.shape[1]
  cellrow = 18
  partitionrow = height//cellrow
  cellcol = 16
  partitioncol = width//cellcol
  colorspresent = []
  for i in range(cellrow):
    for j in range(cellcol):
       if(i==cellrow-1 and j==cellcol-1):
          row = random.randint(i*partitionrow, height-1)
          col = random.randint(j*partitioncol, width-1)
          color = source[row,col]
          if(not ispresent(colorspresent, (color[0],color[1],color[2]))):
              colorspresent.append((color[0],color[1],color[2]))
       elif(i==cellrow-1):
          row = random.randint(i*partitionrow, height-1)
          col = random.randint(j*partitioncol, (j+1)*partitioncol-1)
          color = source[row,col]
          if(not ispresent(colorspresent, (color[0],color[1],color[2]))):
              colorspresent.append((color[0],color[1],color[2]))
       elif(j==cellcol-1):
          row = random.randint(i*partitionrow, (i+1)*partitionrow-1)
          col = random.randint(j*partitioncol, width-1)
          color = source[row,col]
          if(not ispresent(colorspresent, (color[0],color[1],color[2]))):
              colorspresent.append((color[0],color[1],color[2]))
       else:
          row = random.randint(i*partitionrow, (i+1)*partitionrow-1)
          col = random.randint(j*partitioncol, (j+1)*partitioncol-1)
          color = source[row,col]
          if(not ispresent(colorspresent, (color[0],color[1],color[2]))):
              colorspresent.append((color[0],color[1],color[2]))
  return colorspresent
"""

def jittered_sample(lab_space_colored):
   height = len(lab_space_colored)
   width = len(lab_space_colored[0])
   cellrow = 18
   partitionrow = height//cellrow
   cellcol = 18
   partitioncol = width//cellcol
   jittered_sample = []
   for i in range(cellrow):
     for j in range(cellcol):
       if(i==cellrow-1 and j==cellcol-1):
         row = random.randint(i*partitionrow, height-1)
         col = random.randint(j*partitioncol, width-1)
         color = lab_space_colored[row][col]
         rowstart = max(0,row-2)
         rowend = min(row+2,height-1)
         colstart = max(0,col-2)
         colend = min(col+2,width-1)
         std_dev = find_stddev(lab_space_colored,rowstart,rowend,colstart,colend,color[0])
         jittered_sample.append((color,std_dev))
       elif(i==cellrow-1):
         row = random.randint(i*partitionrow, height-1)
         col = random.randint(j*partitioncol, (j+1)*partitioncol-1)
         color = lab_space_colored[row][col]
         rowstart = max(0,row-2)
         rowend = min(row+2,height-1)
         colstart = max(0,col-2)
         colend = min(col+2,width-1)
         std_dev = find_stddev(lab_space_colored,rowstart,rowend,colstart,colend,color[0])
         jittered_sample.append((color,std_dev))
       elif(j==cellcol-1):
         row = random.randint(i*partitionrow, (i+1)*partitionrow-1)
         col = random.randint(j*partitioncol, width-1)
         color = lab_space_colored[row][col]
         rowstart = max(0,row-2)
         rowend = min(row+2,height-1)
         colstart = max(0,col-2)
         colend = min(col+2,width-1)
         std_dev = find_stddev(lab_space_colored,rowstart,rowend,colstart,colend,color[0])
         jittered_sample.append((color,std_dev))
       else:
         row = random.randint(i*partitionrow, (i+1)*partitionrow-1)
         col = random.randint(j*partitioncol, (j+1)*partitioncol-1)
         color = lab_space_colored[row][col]
         rowstart = max(0,row-2)
         rowend = min(row+2,height-1)
         colstart = max(0,col-2)
         colend = min(col+2,width-1)
         std_dev = find_stddev(lab_space_colored,rowstart,rowend,colstart,colend,color[0])
         jittered_sample.append((color,std_dev))
   return jittered_sample
   
def find_min_difference(lab_space_colored, l, std_dev):
   minn = 9999999
   min_color = (0,0,0)
   for i in range(len(lab_space_colored)):
      diff = abs(int(lab_space_colored[i][0][0])-int(l)) + abs(int(lab_space_colored[i][1])-std_dev)
      if(diff < minn):
         minn = diff
         min_color = lab_space_colored[i][0]
   return min_color

"""
def find_min_difference(lab_space_colored, l):
   min = 9999999
   min_color = (0,0,0)
   for i in range(len(lab_space_colored)):
      diff = abs(lab_space_colored[i][0]-l)
      if(diff<min):
         min = diff
         min_color = lab_space_colored[i]
   return min_color
"""
def find_stddevv(target,rowstart,rowend,colstart,colend,l):
   sum = 0
   num = 0
   for i in range(rowstart,rowend+1):
     for j in range(colstart,colend+1):
         pixel = target[i,j]
         sum += (int(pixel[0])-int(l))**2
         num += 1
   if(num == 0):
      return 0
   else:
      std_dev = math.sqrt(sum/num)
      return std_dev
      
def lab_space_noncolor(target, lab_space_colored):
   height = target.shape[0]
   width = target.shape[1]
   final_lab_space_noncolor = []
   for i in range(height):
     row = []
     for j in range(width):
        pixel = target[i,j]
        l = pixel[0]
        rowstart = max(0,i-2)
        rowend = min(i+2,height-1)
        colstart = max(0,j-2)
        colend = min(j+2,width-1)
        std_dev = find_stddevv(target,rowstart,rowend,colstart,colend,l)
        color = find_min_difference(lab_space_colored, l, std_dev)
        row.append((l,color[1],color[2]))
        #row.append((color[0],color[1],color[2]))
     final_lab_space_noncolor.append(row)
   return final_lab_space_noncolor
"""
def lab_space_noncolor(target, lab_space_colored):
    root2 = math.sqrt(2)
    root3 = math.sqrt(3)
    root6 = math.sqrt(6)
    height = target.shape[0]
    width = target.shape[1]
    final_lab_space_noncolor = []
    for i in range(height):
      row = []
      for j in range(width):
         pixel = target[i,j]
         B = pixel[0]
         G = pixel[1]
         R = pixel[2]
         L = (0.3811)*R + (0.5783)*G + (0.0402)*B
         M = (0.1967)*R + (0.7244)*G + (0.0782)*B
         S = (0.0241)*R + (0.1288)*G + (0.8444)*B
         if(L<1) : L = 1
         if(M<1) : M = 1
         if(S<1) : S = 1
         l = (L+M+S)/root3
         color = find_min_difference(lab_space_colored, l)
         row.append((l,color[1],color[2]))
         #row.append((color[0],color[1],color[2]))
      final_lab_space_noncolor.append(row)
    return final_lab_space_noncolor
 """
        
def changing_to_bgr(target, final_lab_space_noncolor):
   root2 = math.sqrt(2)
   root3 = math.sqrt(3)
   root6 = math.sqrt(6)
   height = len(final_lab_space_noncolor)
   width = len(final_lab_space_noncolor[0])
   
   for i in range(height):
      for j in range(width):
          l = final_lab_space_noncolor[i][j][0]
          alpha = final_lab_space_noncolor[i][j][1]
          beta = final_lab_space_noncolor[i][j][2]
          L = l/root3 + alpha/root6 + beta/root2
          M = l/root3 + alpha/root6 - beta/root2
          S = l/root3 - 2*(alpha/root6)
          R = (4.4679)*L + (-3.5873)*M + (0.1193)*S
          G = (-1.2186)*L + (2.3809)*M + (-0.1624)*S
          B = (0.0497)*L + (-0.2439)*M + (1.2045)*S
          pixel = target[i,j]
          pixel[0] = int(B)
          pixel[1] = int(G)
          pixel[2] = int(R)
   
   
#############################################################
  
#source_image = "colored.jpg"
source_image = "aaa.jpg"
source = cv2.imread(source_image)
#print(source.shape)
#target_image = "noncolored.jpg"
target_image = "ggg.jpg"
target = cv2.imread(target_image)
#print(target.shape)

bgr_colored = finding_colors(source)
lab_space_colored = convert_to_labspace(bgr_colored)
jittered_samples = jittered_sample(lab_space_colored)
lab_space_noncolored = lab_space_noncolor(target,jittered_samples)
changing_to_bgr(target,lab_space_noncolored)
cv2.imwrite("result.jpg",target)
cv2.waitKey(15000)
cv2.destroyAllWindows()
"""
bgr_colored = finding_colors(source)
bgr_noncolored = finding_colors(target)
lab_space_colored = convert_to_labspace(bgr_colored)
lab_space_noncolored = convert_to_labspace(bgr_noncolored)
print("Length "+ str(len(lab_space_colored)))
print("Length "+ str(len(lab_space_noncolored)))
"""

