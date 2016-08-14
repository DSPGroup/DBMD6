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

#checkSum()
#load_file ('C:\Users\erans\Documents\Validation\Python\Production_Test_File\VT_D6_ver_285_Sen333.bin' , 4 ,1)
#load_file ('C:\Users\erans\Documents\Validation\Python\Production_Test_File\prod_min_leakage_ext.bin' ,0,1)
#load_file ('C:\Users\erans\Documents\Validation\Python\Production_Test_File\D6_prod_dynamic_power_ext.bin' ,0,1)
#load_file ('C:\Users\erans\Documents\Validation\Python\Production_Test_File\D4_prod_dynamic_power_ext.bin' ,0,1)
#load_file ('C:\Users\erans\Documents\Validation\Python\Production_Test_File\dbmd6_dynamic_power_ext_no_dtcm.bin' ,0,1)
#load_file ('C:\Users\erans\Documents\Validation\Python\Production_Test_File\dbmd4_dynamic_power_ext_no_dtcm.bin' ,0,1)
######## Last File ############
#load_file ('C:\Users\erans\Documents\Validation\Python\Production_Test_File\D4_3_7_2016_dbmd4_dynamic_power_ext_no_dtcm.bin',0,1)
load_file ('C:\Users\erans\Documents\Validation\Python\Production_Test_File\D6_3_7_2016_dbmd6_dynamic_power_ext_no_dtcm.bin',0,1)


# read_apb_reg ("3000000")
# read_apb_reg ("3000004")
# read_apb_reg ("3000008")
#time.sleep(5)
#exeBootFile()
#read_apb_reg ("3000000")