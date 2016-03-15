##########################
#Script identification 
##########################
#Author : Eran Simoni
#Start Date : 8-3-2016
#Script change By : xxxx

#######################################################################################


#########################################
#####     Uart Basic Configuration
#########################################
COM = 'COM4'
BAUD_RATE = 3000000
BYTE_SIZE = 8
PARIT = 'N'
STOP_BITS = 1
TIME_SERIAL = 1
#########################################

#########################################
#####     Create Folder
#########################################
Path_Folder = r'C:\Users\valab\Documents\Validation\Python'
Folder_Name = "Test Result"
Folder_Date = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d')
Dir_Name = os.path.join(Path_Folder , Folder_Name , Folder_Date)

#########################################
#####     Log
#########################################

Test_Name = "BIST_TEST"

Character1 = "\\"
Character2 = "_" 
Test_Date = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d')
Test_Time = datetime.datetime.strftime(datetime.datetime.now(), '%H-%M-%S')
Log_Name = Character1 + Test_Name + Character2 + Test_Date + Character2 + Test_Time + '.txt'

