#!/usr/bin/env python

#!/usr/bin/env python
##########################
#Script identification Main Script
##########################
#Author : Eran.S
#Start Date : 29-6-2016
#Script change By : xxxx


###############################
#Eran Path File
###############################
execfile ("C:\Users\erans\Documents\Validation\Python\Git\DBMD6\init.py")
#################
# Main Start He
#################
SerialConfig_1 (COM ,BAUD_RATE)
Open_log(Log_Name)
Sync ()
load_file ('C:\Users\erans\Documents\Validation\Python\Production_Test_File\VT_D6_ver_285_Sen333.bin',4,1)
FW_write_register_short("29","0001")
FW_read_register_short("29")

