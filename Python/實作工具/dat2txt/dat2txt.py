# -*- coding: utf8 -*-
import os
import sys
path0=r"C:\Users\a2008\Desktop\dat2txt"# 文件路径  下句是下面包括的子目录
path1=r"C:\Users\a2008\Desktop\dat2txt"+'\\'
sys.path.append(path1)


files = os.listdir(path0)
print('files',files)# 打印当下目录下的文件

for filename in files:
   portion = os.path.splitext(filename)

   if portion[1] == ".dat":  
      newname = portion[0] + ".txt" 
      filenamedir=path1 +filename
      newnamedir=path1+newname
      os.rename(filenamedir,newnamedir)