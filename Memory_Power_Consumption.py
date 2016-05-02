##########################
#Script identification Main Script
##########################
#Author : HEN LANGE
#Start Date : 13-3-2016
#Script change By : xxxx

###############################
#Hen Path File
###############################
#execfile ("G:\Chip_Validation\Python\Hen\infrastructure\init.py")

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
checkSum()

read_apb_reg ("03000000")
Clock_Out ("Global")
time.sleep(3)
read_apb_reg ("3000084")

System_Clock_PLL ("32")


