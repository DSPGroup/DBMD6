##########################
#Script identification Main Script
##########################
#Author : Eran Simoni
#Start Date : 8-3-2016
#Script change By : xxxx

#######################################################################################


execfile ("G:\Chip_Validation\Python\Zvi\infrastructure\init.py")

#################
# Main Start He
#################
# configure the correct com and baud rate :: default, COM = 6 and baudrate 3000000
SerialConfig_1 (COM ,BAUD_RATE)

# connect and sync to the D6

Open_log(Log_Name)
Sync ()                                   


read_apb_reg ("0300004c")
time.sleep(1)
write_apb_reg ("0300004c", "0000001")
time.sleep(1)
read_apb_reg ("0300004c")

