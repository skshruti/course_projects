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

def is_in_swatch(row,col,swatches):
  for i in range(len(swatches)):
    swatchrange = swatches[i]
    if(row >= swatchrange[0][0] and row <= swatchrange[1][0]):
      if(col >= swatchrange[0][1] and col <= swatchrange[1][1]):
         return True
  return False
  
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

     l = (L+M+S)/root3
     alpha = (L+M-2*S)/root6
     beta = (L-M)/root2
     lab_space.append((l,alpha,beta))
  return lab_space

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

def find_min_difference(lab_space_colored, l):
   min = 9999999
   min_color = (0,0,0)
   for i in range(len(lab_space_colored)):
      diff = abs(lab_space_colored[i][0]-l)
      if(diff<min):
         min = diff
         min_color = lab_space_colored[i]
   return min_color

def lab_space_noncolor(target, lab_space_colored, swatches):
   height = target.shape[0]
   width = target.shape[1]
   final_lab_space_noncolor = []
   for i in range(height):
     row = []
     for j in range(width):
        if (is_in_swatch(i,j,swatches)):
           pixel = target[i,j]
           l = pixel[0]
           color = find_min_difference(lab_space_colored, l)
           row.append((l,color[1],color[2]))
        else:
           pixel = target[i,j]
           l = pixel[0]
           row.append((pixel[0],pixel[1],pixel[2]))
     final_lab_space_noncolor.append(row)
   return final_lab_space_noncolor


def matching_swatch(lab_space_noncolor,swatches,l):
  min_error = 99999999
  min_index = 0
  for i in range(len(swatches)):
    swatchrange = swatches[i]
    error = 0
    for r in range(swatchrange[0][0],swatchrange[1][0]+1):
       for c in range(swatchrange[0][1],swatchrange[1][1]+1):
           error += ((int(lab_space_noncolor[r][c][0])-int(l))**2)
    if(error < min_error):
       min_error = error
       min_index = i
  return i

def color_from_swatch(lab_space_noncolor, swatchrange, l):
   min = 9999999
   min_color = (0,0,0)
   for r in range(swatchrange[0][0],swatchrange[1][0]+1):
      for c in range(swatchrange[0][1],swatchrange[1][1]+1):
          diff = abs(int(lab_space_noncolor[r][c][0])-int(l))
          if(diff<min):
            min = diff
            min_color = lab_space_noncolor[r][c]
   return min_color
   
def swatch_algo(lab_space_noncolor, swatches):
  height = len(lab_space_noncolor)
  width = len(lab_space_noncolor[0])
  #print(lab_space_noncolor)
  new_lab_space = []
  for i in range(height):
    row = []
    for j in range(width):
        if (not is_in_swatch(i,j,swatches)):
           l = lab_space_noncolor[i][j][0]
           corresponding_swatch_index = matching_swatch(lab_space_noncolor, swatches,l)
           swatchrange = swatches[corresponding_swatch_index]
           corresponding_color = color_from_swatch(lab_space_noncolor, swatchrange, l)
           row.append((l,corresponding_color[1],corresponding_color[2]))
        else:
           row.append(lab_space_noncolor[i][j])
    new_lab_space.append(row)
  return new_lab_space

def changing_to_bgr(target, final_lab_space_noncolor):
   root2 = math.sqrt(2)
   root3 = math.sqrt(3)
   root6 = math.sqrt(6)
   height = len(final_lab_space_noncolor)
   width = len(final_lab_space_noncolor[0])
   #print(width)
   

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

patch1 = [(43,48),(73,78)]
patch2 = [(138,230),(0,100)]
patch3 = [(150,200),(200,250)]
swatches = [patch1,patch2,patch3]
#swatches = [patch1,patch2]
bgr_colored = finding_colors(source)
lab_space_colored = convert_to_labspace(bgr_colored)
lab_space_noncolored = lab_space_noncolor(target,lab_space_colored,swatches)
final_lab_space_noncolored  = swatch_algo(lab_space_noncolored, swatches)
changing_to_bgr(target,final_lab_space_noncolored)
cv2.imwrite("newimg.jpg",target)
cv2.waitKey(15000)
cv2.destroyAllWindows()


##############################################################################################



           
  


