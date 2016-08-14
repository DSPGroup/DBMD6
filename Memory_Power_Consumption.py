##########################
#Script identification Main Script
##########################
#Author : Eran.S
#Start Date : 13-3-2016
#Script change By : xxxx

###############################
#Eran Path File
###############################
execfile ("C:\Users\erans\Documents\Validation\Python\Git\DBMD6\init.py")
#################
# Main Start He
#################
# configure the correct com and baud rate :: default, COM = 6 and baudrate 3000000

SerialConfig_1 (COM ,BAUD_RATE)
# connect and sync to the D6

Open_log(Log_Name)
Sync ()
#checkSum()

#read_apb_reg ("3000000")
#Clock_Out ("Global")
#time.sleep(1)
#System_Clock_PLL ("32" ,"32","D6")
#read_apb_reg ("3000084")
#read_apb_reg("030000cc")
#time.sleep(2)

#Can Select the following memory name :
#PTCM = 0 to 7
#DTCM = 0 to 9
#TAG = 0 to 1
#CACHE = 0 to 3
#PAHB = 0 to 9
# shut_down , deep_sleep , light_sleep
#All_Memory_Power_Mode ("light_sleep" ,1)
#read_apb_reg("030000cc")
time.sleep(7)
#All_Memory_Power_Mode ("deep_sleep" ,1)
#time.sleep(7)
All_Memory_Power_Mode ("shut_down" ,1)
#time.sleep(7)
#time.sleep(5)
#read_apb_reg (MEM_PWR_MD_SD1)
#Memory_Block_Select (PTCM , 7 , "shut_down")
#time.sleep(5)
#Memory_Block_Select (TAG , 1 , "shut_down")
#time.sleep(5)
#Memory_Block_Select (PAHB , 9 , "shut_down")
#time.sleep(5)
#Memory_Block_Select (CACHE , 3, "shut_down")
#time.sleep(5)
#read_apb_reg (MEM_PWR_MD_SD1)




