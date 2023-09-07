import numpy as np

def removepadding(src, pad):
    imarr = np.array(src)
    result = imarr[pad:imarr.shape[0] - pad, pad:imarr.shape[1] - pad]
    return result

#not finish
def conv2(img, H, W, kernel, stride, padding): 
    output_h = int(((H-len(kernel[0]) + 2*padding)/stride) + 1)
    output_w = int(((H-len(kernel[1]) + 2*padding)/stride) + 1)
    print(output_h,output_w)
    print(len(kernel[1]))
    res = np.zeros([output_h,output_w]) 
    for i in range(output_h): #H - kernek size + 1
        for j in range(output_w): #W - kernek size + 1
            temp = img[i + (stride-1) : i + (stride-1) +len(kernel[0]) , j +(stride-1) : j +(stride-1) +len(kernel[1]) ] #stride = 1
            print(i,j,'tempe : ',temp.shape,temp)
            temp = np.multiply(temp,kernel) #點乘 ; np.dot才為矩陣相乘
            res[i][j] = temp.sum()

    return res

def conv(img, H, W, kernel): 
    res = np.zeros([6,6])
    for i in range(6): #H - kernek size + 1
        for j in range(6): #W - kernek size + 1
            temp = img[i:i+5 , j:j+5] #stride = 1
            temp = np.multiply(temp,kernel) #點乘 ; np.dot才為矩陣相乘
            res[i][j] = temp.sum()

    return res


def convert_ycbcr_to_rgb(img, dim_order='hwc'):
    if dim_order == 'hwc':
        r = 298.082 * img[..., 0] / 256. + 408.583 * img[..., 2] / 256. - 222.921
        g = 298.082 * img[..., 0] / 256. - 100.291 * img[..., 1] / 256. - 208.120 * img[..., 2] / 256. + 135.576
        b = 298.082 * img[..., 0] / 256. + 516.412 * img[..., 1] / 256. - 276.836
    else:
        r = 298.082 * img[0] / 256. + 408.583 * img[2] / 256. - 222.921
        g = 298.082 * img[0] / 256. - 100.291 * img[1] / 256. - 208.120 * img[2] / 256. + 135.576
        b = 298.082 * img[0] / 256. + 516.412 * img[1] / 256. - 276.836
    return np.array([r, g, b]).transpose([1, 2, 0])

if __name__ == '__main__':
    #-----verify output_padding stage
    batch = np.load('C:/Users/a2008/Desktop/deconv/batch.npy')
    #print(batch.shape)
    golden = np.load('C:/Users/a2008/Desktop/deconv/golden.npy')
    #print(golden.shape)
    
    new =[]
    for i in range(100):
        new.append(np.load('C:/Users/a2008/Desktop/deconv/input/input_'+str(i)+'.npy'))
        
    #print(len(new))    
    new = np.array(new).reshape(100,56,6,6)    
        
    #print(new.shape)
    #print(new[99][18])
    
    accuracy = 0.000002
    error=0
    for k in range(56):
        error = 0
        for i in range(24):
            for j in range(24):
                if( abs(batch[99][k][i][j] - golden[k][i][j]) > accuracy ) :
                    error +=1
                    #print(batch[99][k][i][j] ,':', golden[k][i][j])
        #print('\n----->%d error : '%k,error,'\n')
        
    test = np.array([ [1,2,3], [4,5,6], [7,8,9] ])
    print(test)
    
    
    t1 = test[:,2]
    print('t1 :',t1)
    
    for i in range(3):
        test = np.insert(test,3,t1,1)
    print(test)
    
    t0 = test[2,:]
    print('t0 :',t0)
    
    for i in range(3):
        test = np.insert(test,3,t0,0)
    print(test)
    
    

