##########################
#Script identification 
##########################
#Author : Eran.S
#Start Date : 13-3-2016
#Script change By : xxxx


#######################################################################################
# FW Global variables setting
#######################################################################################
read_in_progress = False
write_in_progress = False
stop_streaming_flag = False
statistic = True
mic24 = '0000'
mic25 = '0000'
log_filename = ''
LIST_OF_VALUES = {}



#######################################################################################
chip_type = "D6"

#########################################
#####     Uart Basic Configuration
#########################################
COM = 'COM4'
BAUD_RATE = 57600 #115200
BYTE_SIZE = 8
PARIT = 'N'
STOP_BITS = 1
TIME_SERIAL = 1
#########################################
APB_Clock = 32768000.0
Integer =5.0
Frac =11.0
#########################################
#####     Hen Create Folder
#########################################
#Path_Folder = r'C:\Users\henl\Documents\D6\BIST_test_results'

#########################################
#####     Eran Create Folder
#########################################
#Path_Folder = r'C:\tmp\Python\\'

#Folder_Name = "Test Result"
#Folder_Date = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d')
#Dir_Name = os.path.join(Path_Folder , Folder_Name , Folder_Date)

#########################################
#####     Bar Create Folder
#########################################
Path_Folder = r'C:\python_scripts\\'
Folder_Name = "Test Result"
Folder_Date = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d')
Dir_Name = os.path.join(Path_Folder , Folder_Name , Folder_Date)
#########################################
#####     Log
#########################################

Test_Name = "HBG_Test"

Character1 = "\\"
Character2 = "_" 
Test_Date = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d')
Test_Time = datetime.datetime.strftime(datetime.datetime.now(), '%H-%M-%S')
Log_Name = Character1 + Test_Name + Character2 + Test_Date + Character2 + Test_Time + '.txt'
Log_Name_Excel = Character1 + Test_Name + Character2 + Test_Date + Character2 + Test_Time + '.xlsx'

#########################################
#####     Memory address offset
#########################################
#light  sleep mode reg == 

MEM_PWR_MD_LS1 = "30000a0"
MEM_PWR_MD_LS2 = "30000a4"
MEM_PWR_MD_DS1 = "30000A8"
MEM_PWR_MD_DS2 = "30000AC"
MEM_PWR_MD_SD1 ="30000B0"
MEM_PWR_MD_SD2 = "30000B4"
#########################

PTCM_Start_Bit =18
DTCM_Start_Bit =6
TAG_Start_Bit = 4
CACHE_Start_Bit =0
PAHB_Start_Bit =1
HWVAD_Start_Bit = 1

#PTCM = [ "40000" ,"80000","100000","200000", "400000", "800000","1000000", "2000000"]
##DTCM blocks 0-3 cannot been moved to DEEP_SLEEP and SHUT_DOWN modes
#DTCM = ["40", "80",	"100", "200", "400", "800", "1000", "2000", "4000", "8000", "10000", "20000"]
#TAG = ["10" , "20"]
##CACHE blocks 0-1 cannot been moved to DEEP_SLEEP and SHUT_DOWN modes
#CACHE = ["1","2","4","8"]
#PAHB = ["2","4","8","10","20","40","80","100", "200","400"]
#ROM = ["800"]
## only can configure on the  "Light_sleep" mode !
#HWVAD0 =["1000"]
#HWVAD1= ["1"]

MEM_DICT= {}
MEM_DICT['PTCM'] = [ "40000" ,"80000","100000","200000", "400000", "800000","1000000", "2000000"]
#DTCM blocks 0-3 cannot been moved to DEEP_SLEEP and SHUT_DOWN modes
MEM_DICT['DTCM'] = ["40", "80",	"100", "200", "400", "800", "1000", "2000", "4000", "8000", "10000", "20000"]
MEM_DICT['TAG'] = ["10" , "20"]
#CACHE blocks 0-1 cannot been moved to DEEP_SLEEP and SHUT_DOWN mode
MEM_DICT['CACHE'] = ["1","2","4","8"]
MEM_DICT['PAHB']= ["2","4","8","10","20","40","80","100", "200","400"]
MEM_DICT['ROM'] = ["800"]
# only can configure on the  "Light_sleep" mode !
MEM_DICT['HWVAD0'] = ["1000"]
MEM_DICT['HWVAD1'] = ["1"]
