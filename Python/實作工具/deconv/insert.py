import numpy as np

def removepadding(src, pad):
    imarr = np.array(src)
    result = imarr[pad:imarr.shape[0] - pad, pad:imarr.shape[1] - pad]
    return result

def conv(img, H, W, kernel):
    res = np.zeros([H-9+1,W-9+1])
    for i in range(H-9+1): #H - kernek size + 1
        for j in range(W-9+1): #W - kernek size + 1
            temp = img[i:i+9 , j:j+9] #stride = 1
            temp = np.multiply(temp,kernel)
            res[i][j] = temp.sum()

    return res

np.set_printoptions(threshold=np.inf)

#insert
input_feature = np.loadtxt('C:/Users/a2008/Desktop/insert/deconv/in/input_0.txt')
kernel = np.loadtxt('C:/Users/a2008/Desktop/insert/deconv/weight/filter_0.txt')
golden = np.loadtxt('C:/Users/a2008/Desktop/insert/deconv/out/output.txt')

input_feature = np.array(input_feature).reshape((6,6))
kernel = np.array(kernel).reshape((9,9))
golden = np.array(golden).reshape(24,24)

input_feature = np.insert(input_feature,3*[1,2,3,4,5],np.array(6*(0)),0)
for i in range(3):
    input_feature = np.insert(input_feature,1,np.array(21*(0)),1)
    input_feature = np.insert(input_feature,3,np.array(21*(0)),1)
    input_feature = np.insert(input_feature,5,np.array(21*(0)),1)
    input_feature = np.insert(input_feature,7,np.array(21*(0)),1)
    input_feature = np.insert(input_feature,9,np.array(21*(0)),1)


#padding
new_feature = np.pad(input_feature, pad_width = (4,4))


#conv
'''
#proof conv
A = np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]])  
A=np.pad(A,pad_width = (1,1))
ken = np.array([[2,2],[2,2]])
print(A.shape)
print(ken.shape)
print(conv(A, 5, 5, ken))
print(conv(A, 5, 5, ken).shape)
'''

output_map = conv(new_feature,29,29,kernel)

#output_padding
for i in range(3):
    output_map=np.insert(output_map,21,np.array(21*(0)),1)
output_map=np.insert(output_map,21,np.array(24*(0)),0)
output_map=np.insert(output_map,21,np.array(24*(0)),0)
output_map=np.insert(output_map,21,np.array(24*(0)),0)
print(output_map.shape,'\n',output_map)


