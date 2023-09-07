import numpy as np
import PIL.Image as pil_image

def removepadding(src, pad):
    imarr = np.array(src)
    result = imarr[pad:imarr.shape[0] - pad, pad:imarr.shape[1] - pad]
    return result

def conv(img, H, W, kernel): 
    res = np.zeros([H-9+1,W-9+1])
    for i in range(H-9+1): #H - kernek size + 1
        for j in range(W-9+1): #W - kernek size + 1
            temp = img[i:i+9 , j:j+9] #stride = 1
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
    #np.set_printoptions(linewidth=80)
    #-----loading data
    golden = np.loadtxt('C:/Users/a2008/Desktop/deconv/data/output99/output.txt')
    golden = golden.reshape((24,24))
    
    weight = []
    input_map = []
    for i in range(56):
        weight.append(np.loadtxt('C:/Users/a2008/Desktop/deconv/data/weight/filter_'+str(i)+'.txt'))
        weight[i] = weight[i].reshape((9,9))
        weight[i] =  weight[i][::-1,::-1] #transpose & inverse
        input_map.append(np.loadtxt('C:/Users/a2008/Desktop/deconv/data/in99/input_'+str(i)+'.txt'))
        input_map[i] = input_map[i].reshape((6,6))
        
    #print(weight[18])
    print(input_map[18].shape)
    

    #-----stride padding : renew feature map
    for i in range(56):
        axis0_stride_padding=0
        axis1_stride_padding=0
        input_map[i] = np.insert(input_map[i],3*[1,2,3,4,5],np.array(axis0_stride_padding),0)
        input_map[i] = np.insert(input_map[i],3*[1,2,3,4,5],np.array(axis0_stride_padding),1)
    #print(input_map[0].shape)
    #print(input_map[55])
       
    #-----zero padding
    new_map = []
    for i in range(56):
        new_map.append(np.pad(input_map[i], pad_width = (4,4)))
    #print(new_map[55])
        
    #-----convolution
    output_map = []
    for i in range(56):
        output_map.append(conv(new_map[i] , 29 , 29 , weight[i]))
    
        
    #-----output_padding  
    output_padding_active = 1 #1 : final_out.shape = (24,24) ; 0 : final_out.shape = (21,21)
    
    if(output_padding_active):
        final_out_h = 24
        final_out_w = 24
        for i in range(56):

            axis1_output_padding = output_map[i][:,20]

            for j in range(3):
                output_map[i] = np.insert(output_map[i],21,axis1_output_padding,1)
            
            axis0_output_padding = output_map[i][20,:]
            for j in range(3):
                output_map[i]=np.insert(output_map[i],21,axis0_output_padding,0)
                
    else:
        final_out_h = 21
        final_out_w = 21 
        
   
    #print(output_map[0])
    #print(len(output_map))
    np.save('golden.npy',output_map)

     
        
    #-----overlap all channel feature map    
    final_out = np.zeros((final_out_h,final_out_w))
    for i in range(56):
        final_out = final_out + output_map[i]
        #if(i==3):print(final_out)
    #print(final_out)    
    
    #-----verify with golden
    if(output_padding_active):
        error=0
        accuracy=0.01
        for i in range(24):
            for j in range(24):
                if( abs(final_out[i][j] - golden[i][j]) > accuracy ) :
                    error +=1
                    print(final_out[i][j] ,':', golden[i][j])
        print('error : ',error)
        
    final_out = final_out * 255
    
    #-----generate .jpg to visiualize 
    
    ycbcr_1 = np.loadtxt('C:/Users/a2008/Desktop/deconv/data/ycrcb99/ycrcb_1.txt')
    ycbcr_1 = ycbcr_1.reshape((24,24))
    ycbcr_2 = np.loadtxt('C:/Users/a2008/Desktop/deconv/data/ycrcb99/ycrcb_2.txt')
    ycbcr_2 = ycbcr_2.reshape((24,24))
    
    if(output_padding_active):
        output = np.array([final_out, ycbcr_1, ycbcr_2]).transpose([1, 2, 0]) 
        output = np.clip(convert_ycbcr_to_rgb(output), 0.0, 255.0).astype(np.uint8)
        output = pil_image.fromarray(np.uint8(output))
        output.save('C:/Users/a2008/Desktop/deconv/result99/cut_out99.jpg')
    
        
            