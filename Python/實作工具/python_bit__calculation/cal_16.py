mask = 0xfff0
enb = 0xeeee

ans = mask | enb

#print(hex(ans),'\n')

#print(bin(0x7),'\n')

      
two=2**14
#print(two,'\n')


hex32 = 0xffffffff
bin32 = list(bin(hex32))
bin32 = bin32[2:]
bin_int_32=''



for i in range(len(bin32)):
    bin32[i] = int(bin32[i])

print(bin32)

if(bin32[0] == 1) :
    for i in range(len(bin32) - 1):
        if (bin32[i] == 1):
            bin32[i] = bin32[i] - 1
        elif (bin32[i] == 0) :
            bin32[i] = bin32[i] + 1
        else :
            print('type_error','\n')

print(bin32)
            
for i in range (len(bin32)):
    bin_int_32 = bin_int_32 + str(bin32[i])
            

bin32 = bin(int(bin_int_32))
decial32 = int(bin_int_32)

print(decial32)



    

