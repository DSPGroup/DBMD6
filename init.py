##########################
#Script identification :: init Script
##########################
#Author : HEN LANGE
#Start Date : 13-3-2016
#Script change By : xxxx

#######################################################################################

import serial # for the RS232 function
import time # for the time and sleep command
import datetime # for revived the windows time signature  
import binascii # for convert from UART answer to bin

import os.path # for the make dir option
import sys
import select
import shlex
import datetime
import shutil
import binascii
import openpyxl

##########################################################
#Hen File Configuration
##########################################################
execfile("C:\Users\henl\Documents\D6\PROJ\DBMD6\Init_Configuration.py")
execfile("C:\Users\henl\Documents\D6\PROJ\DBMD6\Function.py")

##########################################################
#Eran File Configuration
##########################################################
#execfile("C:\Users\erans\Documents\Validation\Python\Git\DBMD6\Init_Configuration.py")
#execfile("C:\Users\erans\Documents\Validation\Python\Git\DBMD6\Function.py")
