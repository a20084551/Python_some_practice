import numpy as np
import cv2
import matplotlib.pyplot as plt
from PIL import Image
import os
import PIL.Image as pil_image

def read_picture(address):
    image = []
    imgList = os.listdir(address)
    imgList.sort(key=lambda x: int(x.replace("final_","").split('.')[0]))#按照数字进行排序后按顺序读取文件夹下的图片
    for img in imgList:
        imag = cv2.imread(address + '/' + img)
        #imag = pil_image.open(address+'/'+img).convert('RGB')
        image.append(imag)
    return image

def merge():
    img = read_picture('C:/Users/a2008/Desktop/deconv/data/final_out')
    #print(img[0].shape)
    #print(img[0])
    
    shape = 24
    
    imag = []
    for i in range(100):
        imag.append(np.array(img[i]))
           
    merge = np.zeros((shape*10, shape*10, 3))
    for i in range(10):
        for j in range(10):
            merge[0+i*shape : shape+i*shape , 0+j*shape : shape+j*shape ] = imag[i*10+j]
                 
    #print(merge.shape)
    cv2.imwrite('C:/Users/a2008/Desktop/deconv/result/final_outputpadding.jpg', merge)
                
            