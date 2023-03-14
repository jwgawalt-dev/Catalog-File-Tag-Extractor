def GET_MODULE_LOCATIONS():
    #Acceptable module names, to clear unneccessary entries from module list
    MODULE_FAMILIES_LIST = ['FEN','TB','FXEN','BL','TBIP','TBPN']
    with open(file) as catalogfile:
        i=0
        for line in catalogfile:
            i = i + 1
            if "MODULE" in line:
                try:                
                    module_name = line.split(" ")[1]
                    for prefix in MODULE_FAMILIES_LIST:
                        if prefix in module_name:
                            module_list.append(module_name)
                            module_locations.append((module_name,i))
                except IndexError:
                    continue
        catalogfile.close()
    return module_locations

def GET_MODULE_INFO(module_name,module_list):
    
    import csv
    for module in module_list:
        if desired_module in module[0]:
            startpoint = module[1]
    try:
        with open(myfile,'w',newline='') as csvfile:
            writer= csv.writer(csvfile,delimiter = ',')
            with open(file) as catalogfile:
                
                j=0
                module_found = 0
                I_Data_Found = 0
                O_Data_Found = 0
                C_Data_Found = 0
                for line in catalogfile:
                    j+=1
                    
                    if j >= startpoint and "END_MODULE" not in line:
                        module_found = 1
                        #print(line)
                        if "ConfigData" in line:
                            C_Data_Location = j
                            C_Data_Found = 1
                            I_Data_Found = 0
                            O_Data_Found = 0
                            writer.writerow(('Configuration Data',' '))
                        if "InputData (" in line:
                            I_Data_location = j
                            I_Data_Found = 1
                            O_Data_Found = 0
                            C_Data_Found = 0
                            writer.writerow(('Input Data',' '))

                        if "OutputData (" in line:
                            O_Data_Location = j
                            O_Data_Found = 1
                            I_Data_Found = 0
                            writer.writerow(('Output_Data',' '))

                        if C_Data_Found == 1 or I_Data_Found or O_Data_Found:
                            #print(line)
                            try:
                                offset = line.split(':=')[0].split("COMMENT.DATA")[1]
                                description = line.split(':=')[1]
                            except IndexError:
                                offset = line.split(':=')[0]
                                description = ""
                            new_row = (offset,description)
                            #print(offset,description)
                            try:
                                writer.writerow(new_row)
                            except Exception:
                                print('exception')
                                
                               
                    elif module_found and "END_MODULE" in line:
                        print('Complete. A CSV File has been created in your current working directory')
                        print(myfile)
                        break
    except Exception:
        print("File in use")
                

###############********HERE STARTS MAIN PROGRAM*********#############
#Thoughts for improvement:
        #clean up trailing data
        #have optional user-defined offsets to match better with existing programs
        #maybe make a GUI with dropdown instead of CLI 
import tkinter as tk
from tkinter import Tk, filedialog
import time
import csv
import os
import sys

current_dir = os.getcwd()

#Ask user to open catalog file
root  = Tk()
root.withdraw()
file = filedialog.askopenfilename()
module_list = []
module_locations = []



#module list is a list of tuples : ("Module Name" (string),Starting Line in Catalog file (int))
module_list = GET_MODULE_LOCATIONS()

#iterate through module location list, display available modules
i=0
for module in module_list:
    
    if i==0:
        print('Available Modules')
        i+=1
    print(i,module[0])
    i+=1
    
#get user input, handle invalid entries
desired_module_index = int(input("Enter Module Number\n>"))
try:
    desired_module = module_list[desired_module_index-1][0]
except IndexError:
    print('invalid module id')
    sys.exit(1)
#generate new file name based on module selection    
myfile = current_dir+"/"+desired_module+" controller tags.csv" 
print("-"*50)
print("\n")


#get module information and write to csv
GET_MODULE_INFO(desired_module,module_list)
    
