##########################
#Script identification 
##########################
#Author : Eran.S
#Start Date : 13-3-2016
#Script change By : xxxx

#######################################################################################
chip_type = "D6"

#########################################
#####     Uart Basic Configuration
#########################################
COM = 'COM6'
BAUD_RATE = 921600
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
Path_Folder = r'C:\tmp\Python\\'

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

#########################################
#####     Memory address offset
#########################################
#light  sleep mode reg == 
MEM_PWR_MD_LS1 = "30000a0"
MEM_PWR_MD_LS2 = "30000a4"
MEM_PWR_MD_DS1 ="30000a8"
MEM_PWR_MD_DS2 = "30000ac"
MEM_PWR_MD_SD1 = "30000b0"
MEM_PWR_MD_SD2 = "30000b4"
#########################

PTCM_Start_Bit =18
DTCM_Start_Bit =6
TAG_Start_Bit = 4
CACHE_Start_Bit =0
PAHB_Start_Bit =1
HWVAD_Start_Bit = 1

PTCM = [ "40000" ,"C0000","1C0000","3C0000",	"7C0000","FC0000",	"1FC0000", "3FC0000"]
DTCM = ["3C0",	"7C0",	"FC0", "1FC0", "3FC0", "7FC0", "FFC0", "1FFC0", "3FFC0"]
TAG = ["10" , "30"]
CACHE = ["1","3","7","F"]
PAHB = ["2","6","E","1E","3E","7E","FE","1FE", "3FE","7FE"]
ROM = [3]
# only can configure on the  "Light_sleep" mode !
HWVAD0 =[1000]
HWVAD1= [1]
