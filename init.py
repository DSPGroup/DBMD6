##########################
#Script identification :: init Script
##########################
#Author : Eran Simoni
#Start Date : 8-3-2016
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

execfile("G:\Chip_Validation\Python\Zvi\infrastructure\Init_Configuration.py")
execfile("G:\Chip_Validation\Python\Zvi\infrastructure\Function.py")
