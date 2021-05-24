import numpy as np
from matplotlib import pyplot as plt
import cv2
import os
import math
import dlib

def gaussian_value(x, sigma):
    return (1.0 / (math.sqrt(2 * math.pi * (sigma * 2)))) * math.exp(- (x * 2) / (2 * (sigma ** 2)))
  
#loading images
string="subject.jpg"
sub_img = cv2.imread(string)
image_show=cv2.cvtColor(sub_img,cv2.COLOR_BGR2RGB)
plt.imshow(image_show)
plt.show()
sub_img

string="example.jpg"
ex_img = cv2.imread(string)
image_show=cv2.cvtColor(ex_img,cv2.COLOR_BGR2RGB)
plt.imshow(image_show)
plt.show()


#sub_dict={'a':[25,83],'b':[29,125],'c':[53,192],'d':[74,227],'e':[126,251],'f':[171,229],'g':[197,196],'h':[218,119],'i':[219,78],'j':[38,76],'k':[52,62],'l':[90,73],'m':[122,61],'n':[153,75],'o':[188,63],'p':[205,69],'q':[77,95],'r':[124,92],'s':[173,95],'t':[124,149],'u':[105,158],'v':[146,159],'w':[125,180],'x':[91,190],'y':[157,190],'z':[127,207],'1':[107,203],'2':[145,200],'tl':[0,0],'bl':[0,253],'tr':[256,253],'br':[256,0],'tm':[122,0],'bm':[122,253]}
#ex_dict={'a':[30,77],'b':[35,127],'c':[48,184],'d':[78,226],'e':[131,253],'f':[180,231],'g':[208,198],'h':[232,128],'i':[235,77],'j':[54,66],'k':[67,57],'l':[105,63],'m':[134,54],'n':[166,64],'o':[187,58],'p':[217,68],'q':[86,92],'r':[131,89],'s':[182,93],'t':[134,143],'u':[111,156],'v':[159,157],'w':[134,180],'x':[99,188],'y':[164,188],'z':[133,208],'1':[113,201],'2':[156,203],'tl':[0,0],'bl':[0,253],'tr':[256,253],'br':[256,0],'tm':[134,0],'bm':[134,253]}
sub_dict={'a':[21,106],'b':[34,145],'c':[53,196],'d':[59,202],'e':[126,251],'f':[194,204],'g':[194,196],'h':[214,145],'i':[222,106],'j':[38,76],'k':[52,62],'l':[90,74],'m':[122,68],'n':[153,74],'o':[188,62],'p':[205,69],'q':[77,95],'r':[124,92],'s':[173,95],'t':[124,149],'u':[105,158],'v':[146,159],'w':[125,180],'x':[91,190],'y':[157,190],'z':[127,207],'1':[107,201],'2':[145,201],'tl':[0,0],'bl':[0,253],'br':[256,253],'tr':[256,0],'tm':[122,0],'bm':[122,253],'h1':[17,25],'h2':[24,0],'h3':[28,48],'h4':[33,20],'h5':[47,0],'h6':[189,0],'h7':[205,20],'h8':[213,48],'h9':[228,25],'h10':[220,0],'n1':[59,253],'n2':[193,253],'e1':[20,86],'e2':[10,70],'e3':[5,89],'e4':[7,119],'e5':[19,140],'e6':[226,85],'e7':[237,69],'e8':[245,88],'e9':[243,118],'e10':[231,140]}
ex_dict={'a':[27,98],'b':[44,160],'c':[48,190],'d':[70,218],'e':[131,253],'f':[196,218],'g':[208,190],'h':[222,160],'i':[239,96],'j':[54,66],'k':[67,58],'l':[105,64],'m':[134,56],'n':[166,64],'o':[187,58],'p':[217,68],'q':[86,93],'r':[131,89],'s':[182,93],'t':[134,143],'u':[111,156],'v':[159,157],'w':[134,180],'x':[99,188],'y':[164,188],'z':[133,208],'1':[113,203],'2':[156,203],'tl':[0,0],'bl':[0,253],'br':[256,253],'tr':[256,0],'tm':[134,0],'bm':[134,253],'h1':[25,35],'h2':[34,0],'h3':[33,62],'h4':[43,39],'h5':[52,0],'h6':[209,0],'h7':[227,39],'h8':[234,62],'h9':[247,35],'h10':[239,0],'n1':[70,253],'n2':[198,253],'e1':[25,97],'e2':[18,88],'e3':[18,109],'e4':[19,133],'e5':[27,145],'e6':[243,96],'e7':[248,89],'e8':[251,106],'e9':[250,128],'e10':[241,147]}
triangles=[['a','j','q'],['j','k','l'],['j','q','l'],['q','l','r'],['k','m','o'],['k','l','m'],['l','m','n'],['l','r','n'],['m','n','o'],['r','n','s'],['n','o','p'],['n','s','p'],['s','p','i'],['a','q','b'],['b','q','r'],['r','s','h'],['h','s','i'],['r','t','u'],['r','t','v'],['u','t','v'],['b','r','u'],['v','h','r'],['v','h','g'],['u','b','c'],['c','x','d'],['c','x','u'],['v','y','g'],['y','f','g'],['d','1','e'],['1','e','z'],['e','z','f'],['f','z','2'],['2','f','y'],['u','v','w'],['u','x','w'],['v','w','y'],['x','1','w'],['1','w','z'],['z','w','2'],['2','w','y'],['d','x','1'],['d','bl','n1'],['d','e','n1'],['e','n2','n1'],['f','e','n2'],['f','n2','br'],['a','e1','e2'],['a','e3','e2'],['a','e3','e4'],['a','e5','e4'],['a','b','e5'],['i','e6','e7'],['i','e8','e7'],['i','e9','e8'],['i','e10','e9'],['i','h','e10'],['a','h3','h1'],['h2','h3','h1'],['h4','h3','h2'],['h5','h4','h2'],['i','h8','h9'],['h10','h8','h9'],['h7','h8','h10'],['h10','h6','h7'],['a','j','h3'],['k','j','h3'],['k','h4','h3'],['k','h4','h5'],['k','h5','h6'],['k','o','h6'],['o','h6','h7'],['o','h8','h7'],['o','p','h8'],['i','p','h8'],['tl','h2','h1'],['tl','e2','h1'],['e1','e2','h1'],['e3','e2','tl'],['e3','bl','tl'],['e3','bl','e4'],['e4','bl','e5'],['b','bl','e5'],['b','bl','c'],['c','bl','d'],['h10','h9','tr'],['h10','e7','tr'],['h10','e7','e6'],['e7','e8','tr'],['br','e8','tr'],['br','e8','e9'],['br','e10','e9'],['br','h','e10'],['br','h','g'],['br','f','g'],['i','e7','h8']]#           ,['a','j','tl'],['k','j','tl'],['tl','k','tr'],['o','k','tr'],['o','p','tr'],['i','p','tr'],['bl','tl','a'],['bl','b','a'],['bl','b','c'],['bl','d','c'],['bl','e','d'],['bl','br','e'],['br','e','f'],['br','g','f'],['br','g','h'],['br','h','i'],['br','i','tr']]


def area(x1,y1,x2,y2,x3,y3):
    return abs((x1*(y2-y3)+(x2*(y3-y1))+(x3*(y1-y2)))/2.0)
    
src = cv2.imread("example.jpg")
ex_warped=np.ones([254,257,3], dtype=np.uint8)*255
for tri in triangles:
    tri0=tri[0]
    tri1=tri[1]
    tri2=tri[2]
    srcTri=np.array( [ex_dict[tri0], ex_dict[tri1], ex_dict[tri2]] ).astype(np.float32)
    dstTri=np.array( [sub_dict[tri0], sub_dict[tri1], sub_dict[tri2]] ).astype(np.float32)
    warp_mat = cv2.getAffineTransform(srcTri, dstTri)
    warp_dst = cv2.warpAffine(src, warp_mat, (src.shape[1], src.shape[0]))
    A=area(dstTri[0][0], dstTri[0][1], dstTri[1][0], dstTri[1][1], dstTri[2][0], dstTri[2][1])
    minx=min(dstTri[0][0], dstTri[1][0], dstTri[2][0])
    maxx=max(dstTri[0][0], dstTri[1][0], dstTri[2][0])
    miny=min(dstTri[0][1], dstTri[1][1], dstTri[2][1])
    maxy=max(dstTri[0][1], dstTri[1][1], dstTri[2][1])
    for i in range(int(minx),int(maxx+1)):
        for j in range(int(miny),int(maxy+1)):
            A1=area(dstTri[0][0], dstTri[0][1], dstTri[1][0], dstTri[1][1], i, j)
            A2=area(dstTri[2][0], dstTri[2][1], dstTri[1][0], dstTri[1][1], i, j)
            A3=area(dstTri[2][0], dstTri[2][1], dstTri[0][0], dstTri[0][1], i, j)
            if((A1+A2+A3)==A):
                ex_warped[j,i]=warp_dst[j,i]
    image_show=cv2.cvtColor(ex_warped,cv2.COLOR_BGR2RGB)
    #plt.imshow(image_show)
    #plt.show()
image_show=cv2.cvtColor(ex_warped,cv2.COLOR_BGR2RGB)
plt.imshow(image_show)
plt.show()
final_wrapped = ex_warped
final_wrapped_lab = cv2.cvtColor(final_wrapped, cv2.COLOR_BGR2LAB)

#convert to lab space
sub_lab = cv2.cvtColor(sub_img, cv2.COLOR_BGR2LAB)
#cv2.imwrite("lab.jpg", sub_lab)
image_show=cv2.cvtColor(sub_lab,cv2.COLOR_LAB2RGB)
#plt.imshow(image_show)
#plt.show()

ex_lab = cv2.cvtColor(ex_warped, cv2.COLOR_BGR2LAB)
#cv2.imwrite("lab.jpg", sub_lab)
image_show=cv2.cvtColor(ex_lab,cv2.COLOR_LAB2RGB)
#plt.imshow(image_show)
#plt.show()


#lightness channel
sub_lightness = cv2.cvtColor(sub_img, cv2.COLOR_BGR2GRAY)
i=0
for row in sub_lightness:
    j=0
    for value in row:
        sub_lightness[i][j]=sub_lab[i][j][0]
        j+=1
    i+=1
image_show=cv2.cvtColor(sub_lightness,cv2.COLOR_GRAY2RGB)
#plt.imshow(image_show)
#plt.show()

ex_lightness = cv2.cvtColor(ex_img, cv2.COLOR_BGR2GRAY)
i=0
for row in ex_lightness:
    j=0
    for value in row:
        ex_lightness[i][j]=ex_lab[i][j][0]
        j+=1
    i+=1
image_show=cv2.cvtColor(ex_lightness,cv2.COLOR_GRAY2RGB)
#plt.imshow(image_show)
#plt.show()


#largescale
sub_largescale = cv2.bilateralFilter(sub_lightness,15,10,60)
#cv2.imwrite("blurred.jpg", sub_largescale)
image_show=cv2.cvtColor(sub_largescale,cv2.COLOR_GRAY2RGB)
#plt.imshow(image_show)
#plt.show()

ex_largescale = cv2.bilateralFilter(ex_lightness,15,10,60)
#cv2.imwrite("blurred.jpg", ex_largescale)
image_show=cv2.cvtColor(ex_largescale,cv2.COLOR_GRAY2RGB)
#plt.imshow(image_show)
#plt.show()
#sub_largescale

#detail
sub_detail = cv2.cvtColor(sub_img, cv2.COLOR_BGR2GRAY)
i=0
for row in sub_detail:
    j=0
    for value in row:
        sub_detail[i][j]= int(sub_lightness[i][j])- int(sub_largescale[i][j])-150
        #print(sub_lightness[i][j], sub_largescale[i][j], sub_detail[i][j])
        j+=1
    i+=1
image_show=cv2.cvtColor(sub_detail,cv2.COLOR_GRAY2RGB)
#plt.imshow(image_show)
#plt.show()

ex_detail = cv2.cvtColor(ex_img, cv2.COLOR_BGR2GRAY)
i=0
for row in ex_detail:
    j=0
    for value in row:
        ex_detail[i][j]= int(ex_lightness[i][j])-int(ex_largescale[i][j])-150
        #print(sub_lightness[i][j], sub_largescale[i][j], sub_detail[i][j])
        j+=1
    i+=1
image_show=cv2.cvtColor(ex_detail,cv2.COLOR_GRAY2RGB)
#plt.imshow(image_show)
#plt.show()


#skin
res_detail=ex_detail
image_show=cv2.cvtColor(res_detail,cv2.COLOR_GRAY2RGB)
#plt.imshow(image_show)
#plt.show()

res_largescale=sub_largescale
res_largescale

"""
image_show=cv2.cvtColor(sub_lab,cv2.COLOR_LAB2RGB)
cv2.imshow(winname="doll1", mat=image_show)
cv2.waitKey(3000)
image_show=cv2.cvtColor(ex_lab,cv2.COLOR_LAB2RGB)
cv2.imshow(winname="doll1", mat=image_show)
cv2.waitKey(3000)
"""

#HELPER

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
img = cv2.imread("subject.jpg")
gray = cv2.cvtColor(src=img, code=cv2.COLOR_BGR2GRAY)
faces = detector(gray)
for face in faces:
    x1 = face.left() # left point
    y1 = face.top() # top point
    x2 = face.right() # right point
    y2 = face.bottom() # bottom point

    landmarks = predictor(image=gray, box=face)

    all_points = []
    #Loop through all points
    for n in range(0, 68):
        x = landmarks.part(n).x
        y = landmarks.part(n).y

        # Draw a circle
        cv2.circle(img=img, center=(x, y), radius=1, color=(0, 255, 0), thickness=-1)
        all_points.append((x,y))

# show the image
#cv2.imshow(winname="Face", mat=img)

# Delay between every frame
cv2.waitKey(1000)

left_eye=[]
right_eye=[]
mouth = []
lips = []
skin = []
left_eyebrow=[]
right_eyebrow=[]

ptr = 0
for point in all_points:
   if(ptr >= 17 and ptr <= 21):
       left_eyebrow.append(point)
       ptr += 1
   elif(ptr >= 22 and ptr <= 26):
       right_eyebrow.append(point)
       ptr += 1
   elif(ptr >= 48 and ptr <= 59):
       lips.append(point)
       ptr += 1
   elif(ptr >= 36 and ptr <= 41):
       left_eye.append(point)
       ptr += 1
   elif(ptr >= 42 and ptr <= 47):
       right_eye.append(point)
       ptr += 1
   elif(ptr >= 60 and ptr <= 67):
       mouth.append(point)
       ptr += 1
   else:
       skin.append(point)
       ptr += 1

regions_of_subject = [left_eye, right_eye, mouth, lips, skin, left_eyebrow, right_eyebrow]

rows = img.shape[0]
cols = img.shape[1]
areas_of_face = []

for i, region in enumerate(regions_of_subject):
    hull_contours = cv2.convexHull(np.vstack(np.array(region)))
    hull = np.vstack(hull_contours)
    # black image
    mask = np.zeros((rows, cols), dtype=np.uint8)
    # blit our contours onto it in white color
    cv2.drawContours(mask, [hull], 0, (255,0,0), -1)
    #cv2.imshow(winname="Face", mat=mask)
    #cv2.waitKey(1000)
    areas_of_face.append(mask)

areas_of_face[3] = areas_of_face[3]-areas_of_face[2]
areas_of_face[4] = areas_of_face[4] - (areas_of_face[0]+ areas_of_face[1]+ areas_of_face[2]+ areas_of_face[3]+ areas_of_face[5]+ areas_of_face[6])

#########################################################################################

img_ex = cv2.cvtColor(ex_lab,cv2.COLOR_LAB2RGB)
gray_ex = cv2.cvtColor(src=img_ex, code=cv2.COLOR_BGR2GRAY)
faces_ex = detector(gray)
for face in faces_ex:
    x1 = face.left() # left point
    y1 = face.top() # top point
    x2 = face.right() # right point
    y2 = face.bottom() # bottom point

    landmarks = predictor(image=gray, box=face)

    all_points_ex = []
    #Loop through all points
    for n in range(0, 68):
        x = landmarks.part(n).x
        y = landmarks.part(n).y

        # Draw a circle
        cv2.circle(img=img, center=(x, y), radius=1, color=(0, 255, 0), thickness=-1)
        all_points_ex.append((x,y))

# show the image
#cv2.imshow(winname="Face", mat=img_ex)

# Delay between every frame
cv2.waitKey(1000)

left_eye_ex=[]
right_eye_ex=[]
mouth_ex = []
lips_ex = []
skin_ex = []
left_eyebrow_ex=[]
right_eyebrow_ex=[]

ptr = 0
for point in all_points_ex:
   if(ptr >= 17 and ptr <= 21):
       left_eyebrow_ex.append(point)
       ptr += 1
   elif(ptr >= 22 and ptr <= 26):
       right_eyebrow_ex.append(point)
       ptr += 1
   elif(ptr >= 48 and ptr <= 59):
       lips_ex.append(point)
       ptr += 1
   elif(ptr >= 36 and ptr <= 41):
       left_eye_ex.append(point)
       ptr += 1
   elif(ptr >= 42 and ptr <= 47):
       right_eye_ex.append(point)
       ptr += 1
   elif(ptr >= 60 and ptr <= 67):
       mouth_ex.append(point)
       ptr += 1
   else:
       skin_ex.append(point)
       ptr += 1

regions_of_example = [left_eye_ex, right_eye_ex, mouth_ex, lips_ex, skin_ex, left_eyebrow_ex, right_eyebrow_ex]

rows = img_ex.shape[0]
cols = img_ex.shape[1]
areas_of_face_ex = []

for i, region in enumerate(regions_of_subject):
    hull_contours = cv2.convexHull(np.vstack(np.array(region)))
    hull = np.vstack(hull_contours)
    # black image
    mask = np.zeros((rows, cols), dtype=np.uint8)
    # blit our contours onto it in white color
    cv2.drawContours(mask, [hull], 0, (255,0,0), -1)
    #cv2.imshow(winname="Nikita", mat=mask)
    #cv2.waitKey(1000)
    areas_of_face_ex.append(mask)

areas_of_face_ex[3] = areas_of_face_ex[3]-areas_of_face_ex[2]
areas_of_face_ex[4] = areas_of_face_ex[4] - (areas_of_face_ex[0]+ areas_of_face_ex[1]+ areas_of_face_ex[2]+ areas_of_face_ex[3]+ areas_of_face_ex[5]+ areas_of_face_ex[6])

###########################################################################################

#color
colored_subject_image = sub_lab
colored_example_image = ex_lab

"""
image_show=cv2.cvtColor(sub_lab,cv2.COLOR_LAB2RGB)
cv2.imshow(winname="doll1", mat=image_show)
cv2.waitKey(3000)
image_show=cv2.cvtColor(ex_lab,cv2.COLOR_LAB2RGB)
cv2.imshow(winname="doll1", mat=image_show)
cv2.waitKey(3000)
"""

gamma = 0.8
mask_color = areas_of_face[0] + areas_of_face[1] + areas_of_face[2]
for i in range(colored_subject_image.shape[0]):
   for j in range(colored_subject_image.shape[1]):
      if(mask_color[i,j] == 0):
         colored_subject_image[i,j][1] = (1-gamma)*colored_subject_image[i,j][1] + gamma*colored_example_image[i,j][1]
         colored_subject_image[i,j][2] = (1-gamma)*colored_subject_image[i,j][2] + gamma*colored_example_image[i,j][2]
      else:
         colored_subject_image[i,j][1] = colored_subject_image[i,j][1]
         colored_subject_image[i,j][2] = colored_subject_image[i,j][2]


stringg="example.jpg"
ex_imgg = cv2.imread(string)
ex_labb = cv2.cvtColor(sub_img, cv2.COLOR_BGR2LAB)

#lip color


mask_lip_subject = areas_of_face[3]
mask_lip_example = areas_of_face_ex[3]
for i in range(colored_subject_image.shape[0]):
    for j in range(colored_subject_image.shape[1]):
        if(mask_lip_subject[i,j] == 0):
            pass
        else:
            #colored_subject_image[i,j][0] =  final_wrapped_lab[i,j][0]  #colored_example_image[i,j][0]
            colored_subject_image[i,j][1] =  final_wrapped_lab[i,j][1] #final_wrapped_lab[i,j][1] #colored_example_image[i,j][1]
            colored_subject_image[i,j][2] =  final_wrapped_lab[i,j][2] #final_wrapped_lab[i,j][2] #colored_example_image[i,j][2]
            pass

#higlights

#cv2.imshow(winname="Pehle hu bhai", mat=res_largescale)
#cv2.waitKey(3000)
"""
mask_highlight = areas_of_face[4]
row = res_largescale.shape[0]
col = res_largescale.shape[1]
for i in range(row):
   for j in range(col):
       if(abs(int(ex_largescale[i,j]*mask_highlight[i,j])) <= abs(int(res_largescale[i,j]))):
           res_largescale[i,j] = res_largescale[i,j]
       else:
           res_largescale[i,j] = ex_largescale[i,j]
           
   #res_largescale = res_largescale + cv2.GaussianBlur(res_largescale,(5,5),0)
   
#image_niks=cv2.cvtColor(res_largescale,cv2.COLOR_LAB2RGB)
#cv2.imshow(winname="Me hu bhai", mat=res_largescale)
#cv2.waitKey(3000)
"""

#layer composition.

new_img=sub_img
i=0
for row in ex_detail:
     j=0
     for value in row:
        new_img[i][j][0]= int(res_detail[i][j])+int(res_largescale[i][j])+150+0.5
        new_img[i][j][1]=colored_subject_image[i][j][1]+0.5
        new_img[i][j][2]=colored_subject_image[i][j][2]+0.5
        #print(sub_lightness[i][j], sub_largescale[i][j], sub_detail[i][j])
        j+=1
     i+=1

image_show=cv2.cvtColor(new_img,cv2.COLOR_LAB2RGB)
sub2=cv2.cvtColor(new_img,cv2.COLOR_LAB2BGR)
#cv2.imwrite("sub_changed.jpg", image_show)
cv2.imwrite("sub_changed.jpg", sub2)
plt.imshow(image_show)
plt.show()

#xdog
def dog(img,size,sigma1,sigma2,gamma):
  blurred1 = cv2.GaussianBlur(img,size,sigma1)
  blurred2 = cv2.GaussianBlur(img,size,sigma2)
  return blurred1-gamma*blurred2

def xdog(img,sigma1,sigma2,gamma,threshold,phi,p,size):
    blurred1 = cv2.GaussianBlur(img,size,sigma1)
#     blurred2 = cv2.GaussianBlur(img,size,sigma2)
#     sharpened = (((1+p)*blurred1 - p*blurred2)/255)*img
    dog_img = dog(img,size,sigma1,sigma2,gamma)
    sharpened_init = ((blurred1+p*dog_img)/255)
    sharpened = sharpened_init*img
    for i in range(sharpened.shape[0]):
        for j in range(sharpened.shape[1]):
            if(sharpened[i,j] >= threshold):
                sharpened[i,j] = 1*255
            else:
                sharpened[i,j] = 255*(1 + np.tanh(phi*(sharpened[i,j]-threshold)))
    return sharpened


img = cv2.imread("subject.jpg")
img_gray=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
xdog_img=np.uint8(xdog(img_gray,1,1.6,1,30,0.1,65,(5,5)))
cv2.imwrite("xdog.jpg",xdog_img)
plt.imshow(cv2.cvtColor(xdog_img, cv2.COLOR_GRAY2RGB))
plt.show()

#makeup transfer on xdog
temp=cv2.cvtColor(xdog_img, cv2.COLOR_GRAY2RGB)
i=0
for row in temp:
    j=0
    for value in row:
        temp[i][j][1]=colored_subject_image[i][j][1]+0.5
        temp[i][j][2]=colored_subject_image[i][j][2]+0.5
        #print(sub_lightness[i][j], sub_largescale[i][j], sub_detail[i][j])
        j+=1
    i+=1

plt.imshow(cv2.cvtColor(temp, cv2.COLOR_LAB2RGB))
plt.show()
