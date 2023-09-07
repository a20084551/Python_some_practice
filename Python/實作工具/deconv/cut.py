import numpy as np
import cv2
import matplotlib.pyplot as plt
from PIL import Image

def sharpen(img, sigma=100):
    # sigma = 5、15、25
    blur_img = cv2.GaussianBlur(img, (0, 0), sigma)
    enhance_img = cv2.addWeighted(img, 1.5, blur_img, -0.5, 0)
    
    return enhance_img

#-----read picture
#-bmp to jpg
img = Image.open("C:/Users/a2008/Desktop/cut/butterfly_GT.bmp")
img.save("butterfly.jpg")
#-read img
original = cv2.imread('C:/Users/a2008/Desktop/cut/butterfly.jpg')

origi = sharpen(original)
#cv2.imwrite('origi.jpg',origi)

b,g,r = cv2.split(original)

'''
cv2.imshow('b',b)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.imshow('g',g)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.imshow('r',r)
cv2.waitKey(0)
cv2.destroyAllWindows()
'''

cut_b = []
cut_g = []
cut_r = []
for i in range(10):
    for j in range(10):
        cut_b.append(b[0+i*25 : 25+i*25 , 0+j*25 : 25+j*25])
        cut_g.append(g[0+i*25 : 25+i*25 , 0+j*25 : 25+j*25])
        cut_r.append(r[0+i*25 : 25+i*25 , 0+j*25 : 25+j*25])
        
cut_b = np.array(cut_b) #(100, 25, 25)
cut_g = np.array(cut_g) #(100, 25, 25)
cut_r = np.array(cut_r) #(100, 25, 25)

#bgr1 = cv2.merge([cut_b[0], cut_g[0], cut_r[0]])
#cv2.imwrite('bgr1.jpg' , bgr1)

#-----batch save
#print(cut_b.shape[0]) #100
for i in range(cut_b.shape[0]):
    temp = cv2.merge([cut_b[i], cut_g[i], cut_r[i]])
    cv2.imwrite('C:/Users/a2008/Desktop/cut/cut_file/cut_'+str(i)+'.jpg',temp)

#沒有分批做銳化
#cut_b = sharpen(cut_b)
#cut_g = sharpen(cut_g)
#cut_r = sharpen(cut_r)

for i in range(100):
    sharpen(cut_b[i,:,:])
    sharpen(cut_g[i,:,:])
    sharpen(cut_r[i,:,:])
    

#bgr0 = cv2.merge([cut_b[0], cut_g[0], cut_r[0]])
#cv2.imwrite('bgr0.jpg' , bgr0)

merge_b = np.zeros((250,250))
merge_g = np.zeros((250,250))
merge_r = np.zeros((250,250))
for i in range(10):
    for j in range(10):
        merge_b[0+i*25 : 25+i*25 , 0+j*25 : 25+j*25] = cut_b[i*10+j]
        merge_g[0+i*25 : 25+i*25 , 0+j*25 : 25+j*25] = cut_g[i*10+j]
        merge_r[0+i*25 : 25+i*25 , 0+j*25 : 25+j*25] = cut_r[i*10+j]
        
test_bgr = cv2.merge([merge_b,merge_g,merge_r])
cv2.imwrite('test_bgr.jpg',test_bgr)
#print(test_bgr.shape)


        
        







