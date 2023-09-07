import os

mkdir_name = "example" #rename your design 
path = "C://Users//a2008//Desktop//"+ mkdir_name

if(os.path.exists(path)):
    os.mkdir(path)
    open(path + "//Makefiile","a+")
    os.mkdir(path + "//src")                            #rtl file
    os.mkdir(path + "//define")                         #define file
    open(path + "//define//define.v","a+")
    os.mkdir(path + "//tb")                             #tb file
    os.mkdir(path + "//spy")                            #spyglass tcl file
    open(path + "//spy//spy.tcl","a+")
    os.mkdir(path + "//syn")                            #design compiler tcl file
    open(path + "//syn//syn.tcl","a+")
    open(path + "//syn//.synopsys_dc.setup","a+")
    os.mkdir(path + "//software")                       #which to generate golden.dat 
    os.mkdir(path + "//golden")                         #golden.dat file
else:
    os.mkdir(path)
    open(path + "//Makefiile","a+")
    os.mkdir(path + "//src")                            #rtl file
    os.mkdir(path + "//define")                         #define file
    open(path + "//define//define.v","a+")
    os.mkdir(path + "//tb")                             #tb file
    os.mkdir(path + "//spy")                            #spyglass tcl file
    open(path + "//spy//spy.tcl","a+")
    os.mkdir(path + "//syn")                            #design compiler tcl file
    open(path + "//syn//syn.tcl","a+")
    open(path + "//syn//.synopsys_dc.setup","a+")
    os.mkdir(path + "//software")                       #which to generate golden.dat 
    os.mkdir(path + "//golden")                         #golden.dat file
    
    
    