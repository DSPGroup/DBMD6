##########################
#Script identification Main Script
##########################
#Author : HEN LANGE
#Start Date : 13-3-2016
#Script change By : xxxx

###############################
#Hen Path File
###############################
execfile ("C:\Users\henl\Documents\D6\PROJ\DBMD6\init.py")
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
Sync (10)
print os.getcwd()
#checkSum()
#reset
#Sync () 
#checkSum()


read_apb_reg ("03000000")
Clock_Out ("Global")

#MEM_BIST(test_name,write_val,status_reg,result_val,LDO,Chiptype,Voltage,Temperature)
Voltage="0.9"
STRAP="STRAP10"
Temperature="-40C"
Chiptype="SS2"
Chip_No="1"
name_columnA='Chip No.'
name_columnB='Chip Type'
name_columnC='Memory'
name_columnD='Temperature [C]'
name_columnE='STRAP configuration'
name_columnF='Voltage[V]'
name_columnG='Frequency[MHz]'
name_columnH='Result'
name_columnI='Pass/Fail'
name_columnJ='Status Register Value'

Sheet_Name="Results"

######
#  only if First run, call create excel log function!!!!
######
create_excel_log(Log_Name_Excel,Sheet_Name,name_columnA,name_columnB,name_columnC,name_columnD,name_columnE,name_columnF,name_columnG,name_columnH,name_columnI,name_columnJ)
call_excel_file(Current_File_Name_xls,Sheet_Name)
#wb = openpyxl.load_workbook(Current_File_Name_xls)
#ws = wb.get_sheet_by_name(Sheet_Name)
#index_1=ws.max_row

Frequency="25"

System_Clock_PLL (Frequency,"32","D6")

MEM_BIST("PRAM012","e0080","030000D4","3f","0",Chip_No,Chiptype,Temperature,STRAP,Voltage,Frequency,Sheet_Name)
MEM_BIST("PRAM34","300100","030000D4","3c0","0",Chip_No,Chiptype,Temperature,STRAP,Voltage,Frequency,Sheet_Name)
kill
MEM_BIST("PRAM34","300100","030000D4","3c0","0",Chiptype,Voltage,Temperature)
MEM_BIST("DTCM2","2010","030000D0","1e00","0",Chiptype,Voltage,Temperature)
MEM_BIST("DTCM1","1008","030000D0","1e0","0",Chiptype,Voltage,Temperature)
#MEM_BIST("DTCM0","804","030000D0","1e","0","1.1V","-40",Voltage,Temperature)
MEM_BIST("PTCM","c020","030000D0","1fe000","0",Chiptype,Voltage,Temperature)
#MEM_BIST("CACHE","10040","030000D4","fc00","0",Voltage,Temperature)
MEM_BIST("HWVAD","201","030000D0","0001","0",Chiptype,Voltage,Temperature)
MEM_BIST("ROM","402","0","0","0",Chiptype,Voltage,Temperature)


System_Clock_PLL ("49","32","D6")
MEM_BIST("PRAM012","e0080","030000D4","3f","0",Chiptype,Voltage,Temperature)
MEM_BIST("PRAM34","300100","030000D4","3c0","0",Chiptype,Voltage,Temperature)
MEM_BIST("DTCM2","2010","030000D0","1e00","0",Chiptype,Voltage,Temperature)
MEM_BIST("DTCM1","1008","030000D0","1e0","0",Chiptype,Voltage,Temperature)
#MEM_BIST("DTCM0","804","030000D0","1e","0","1.1V","-40",Voltage,Temperature)
MEM_BIST("PTCM","c020","030000D0","1fe000","0",Chiptype,Voltage,Temperature)
#MEM_BIST("CACHE","10040","030000D4","fc00","0",Voltage,Temperature)
MEM_BIST("HWVAD","201","030000D0","0001","0",Chiptype,Voltage,Temperature)
MEM_BIST("ROM","402","0","0","0",Chiptype,Voltage,Temperature)

System_Clock_PLL ("73","32","D6")
MEM_BIST("PRAM012","e0080","030000D4","3f","0",Chiptype,Voltage,Temperature)
MEM_BIST("PRAM34","300100","030000D4","3c0","0",Chiptype,Voltage,Temperature)
MEM_BIST("DTCM2","2010","030000D0","1e00","0",Chiptype,Voltage,Temperature)
MEM_BIST("DTCM1","1008","030000D0","1e0","0",Chiptype,Voltage,Temperature)
#MEM_BIST("DTCM0","804","030000D0","1e","0","1.1V","-40",Voltage,Temperature)
MEM_BIST("PTCM","c020","030000D0","1fe000","0",Chiptype,Voltage,Temperature)
#MEM_BIST("CACHE","10040","030000D4","fc00","0",Voltage,Temperature)
MEM_BIST("HWVAD","201","030000D0","0001","0",Chiptype,Voltage,Temperature)
MEM_BIST("ROM","402","0","0","0",Chiptype,Voltage,Temperature)

System_Clock_PLL ("82","32","D6")
MEM_BIST("PRAM012","e0080","030000D4","3f","0",Chiptype,Voltage,Temperature)
MEM_BIST("PRAM34","300100","030000D4","3c0","0",Chiptype,Voltage,Temperature)
MEM_BIST("DTCM2","2010","030000D0","1e00","0",Chiptype,Voltage,Temperature)
MEM_BIST("DTCM1","1008","030000D0","1e0","0",Chiptype,Voltage,Temperature)
#MEM_BIST("DTCM0","804","030000D0","1e","0","1.1V","-40",Voltage,Temperature)
MEM_BIST("PTCM","c020","030000D0","1fe000","0",Chiptype,Voltage,Temperature)
#MEM_BIST("CACHE","10040","030000D4","fc00","0",Voltage,Temperature)
MEM_BIST("HWVAD","201","030000D0","0001","0",Chiptype,Voltage,Temperature)
MEM_BIST("ROM","402","0","0","0",Chiptype,Voltage,Temperature)

System_Clock_PLL ("98","32","D6")
MEM_BIST("PRAM012","e0080","030000D4","3f","0",Chiptype,Voltage,Temperature)
MEM_BIST("PRAM34","300100","030000D4","3c0","0",Chiptype,Voltage,Temperature)
MEM_BIST("DTCM2","2010","030000D0","1e00","0",Chiptype,Voltage,Temperature)
MEM_BIST("DTCM1","1008","030000D0","1e0","0",Chiptype,Voltage,Temperature)
#MEM_BIST("DTCM0","804","030000D0","1e","0","1.1V","-40",Voltage,Temperature)
MEM_BIST("PTCM","c020","030000D0","1fe000","0",Chiptype,Voltage,Temperature)
#MEM_BIST("CACHE","10040","030000D4","fc00","0",Voltage,Temperature)
MEM_BIST("HWVAD","201","030000D0","0001","0",Chiptype,Voltage,Temperature)
MEM_BIST("ROM","402","0","0","0",Chiptype,Voltage,Temperature)
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
#MEM_BIST("ROM","402","0","0")

