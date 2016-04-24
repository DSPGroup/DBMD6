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

#################
# Main Start He
#################
# configure the correct com and baud rate :: default, COM = 6 and baudrate 3000000

SerialConfig_1 (COM ,BAUD_RATE)
# connect and sync to the D6

Open_log(Log_Name)
Sync ()
checkSum()
reset
Sync () 
checkSum()
read_apb_reg ("03000000")
Clock_Out ("Global")
System_Clock_PLL ("49")
System_Clock_PLL ("32")
System_Clock_PLL ("73")
System_Clock_PLL ("82")
System_Clock_PLL ("92")
System_Clock_PLL ("98")
#	time.sleep(0.1)
#	GPIO.output(Reset_GPIO,True)
#	time.sleep(0.1)	

#read_apb_reg(addr)
#write_apb_reg(addr,value)
#clear_bit(addr,bit_no)
#set_bit(addr,bit_no)

#reset ()

#MEM_BIST("PRAM012","103c0","030000D4","3c0")
#MEM_BIST("PRAM34","e0080","030000D4","3f")
#MEM_BIST("DTCM2","2010","030000D0","1e00")
#MEM_BIST("DTCM1","1008","030000D0","1e0")
#MEM_BIST("DTCM0","804","030000D0","1e")
#MEM_BIST("PTCM","c020","030000D0","1fe000")
#MEM_BIST("CACHE","10040","030000D4","fc00")
#MEM_BIST("HWVAD","201","030000D0","0001")
MEM_BIST("ROM","402","0","0")

