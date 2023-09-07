import numpy as np
import merge 
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
    #-----declare
    total_img_num = 100
    filter_num = 56
    
    #-----loading data
    weight = []
    for i in range(filter_num):
        weight.append(np.loadtxt('C:/Users/a2008/Desktop/deconv/data/weight/filter_'+str(i)+'.txt'))
        weight[i] = weight[i].reshape((9,9))
        weight[i] =  weight[i][::-1,::-1] #transpose & inverse
        
    
    input_map =[]
    for i in range(total_img_num):
        input_map.append(np.load('C:/Users/a2008/Desktop/deconv/data/input/input_'+str(i)+'.npy'))
    
    print(input_map[0].shape)
    print(len(input_map))
    #print(input_map[99][18])
    
    input_map = np.array(input_map).reshape(total_img_num, filter_num, 6,6) #(100,56,6,6)
    
    #-----stride padding : renew feature map
    new_map = []
    for i in range(total_img_num):
        for j in range(filter_num):
            axis0_stride_padding=0
            axis1_stride_padding=0
            temp = np.insert(input_map[i][j],3*[1,2,3,4,5],np.array(axis0_stride_padding),0)
            temp = np.insert(temp,3*[1,2,3,4,5],np.array(axis0_stride_padding),1)
            new_map.append(temp)

    
    new_map = np.array(new_map).reshape(total_img_num, filter_num, 21,21)    
    
    
    #-----zero padding
    zero_padding_map = []
    for i in range(total_img_num):
        for j in range(filter_num):
            zero_padding_map.append(np.pad(new_map[i][j], pad_width = (4,4)))

            
    zero_padding_map = np.array(zero_padding_map).reshape(total_img_num, filter_num, 29,29)
    
    #-----convolution
    output_map = [] 
    for i in range(total_img_num):
        for j in range(filter_num):
            output_map.append(conv(zero_padding_map[i,j] , 29 , 29 , weight[j]))

    output_map = np.array(output_map).reshape(total_img_num, filter_num, 21,21)
    
    #-----output_padding 
    op_map = []
    for i in range(100):
        for j in range(56):
            temp = output_map[i][j]
            
            axis0_output_padding= temp[20,:]
            for k in range(3):
                temp = np.insert(temp,21,axis0_output_padding,0)
            
            axis1_output_padding= temp[:,20]
            for k in range(3):
                temp = np.insert(temp,21,axis1_output_padding,1)

            op_map.append(temp)
                
   
    print(op_map)
    op_map = np.array(op_map).reshape(100,56,24,24)
    

    #np.save('batch.npy',op_map)
    
    #-----overlap all channel feature map    
    temp = np.zeros((24,24))
    final_out = []
    for i in range(total_img_num):
        for j in range(filter_num):
            temp = temp + op_map[i][j]

        final_out.append(temp)
        temp = np.zeros((24,24))
    
    print(len(final_out))
    
    for i in range(total_img_num):
        final_out[i] = final_out[i] *255 
    

    #-----generate .jpg to visiualize 
    ycrcb_1 =[]
    ycrcb_2 =[]
    for i in range(total_img_num):
        ycrcb_1.append(np.loadtxt('C:/Users/a2008/Desktop/deconv/data/ycrcb_1/ycrcb_'+str(i)+'.txt'))
        ycrcb_1[i] = ycrcb_1[i].reshape((24,24))
        #ycrcb_1[i] = np.delete(ycrcb_1[i],[21,22,23,24],axis = 0)
        #ycrcb_1[i] = np.delete(ycrcb_1[i],[21,22,23,24],axis = 1)
        
        ycrcb_2.append(np.loadtxt('C:/Users/a2008/Desktop/deconv/data/ycrcb_2/ycrcb_'+str(i)+'.txt'))
        ycrcb_2[i] = ycrcb_2[i].reshape((24,24))
        #ycrcb_2[i] = np.delete(ycrcb_2[i],[21,22,23,24],axis = 0)
        #ycrcb_2[i] = np.delete(ycrcb_2[i],[21,22,23,24],axis = 1)
    
    
    for i in range(total_img_num):
        output = np.array([final_out[i], ycrcb_1[i], ycrcb_2[i]]).transpose([1, 2, 0])
        output = np.clip(convert_ycbcr_to_rgb(output), 0.0, 255.0).astype(np.uint8)
        output = pil_image.fromarray(np.uint8(output))
        output.save('C:/Users/a2008/Desktop/deconv/data/final_out/final_'+str(i)+'.jpg')
    
    #-----merge
    merge.merge()
    
    
         