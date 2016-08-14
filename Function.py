##########################
#Script identification Function Script
##########################
#Author : Hen Lange
#Start Date : 27-3-2016
#Script change By : xxxx

########################################################################################################################

#################################
#Serial RS232 Configuration 
#################################

def SerialConfig_1(COM , BAUD_RATE):
    global ser
    ser = serial.Serial()
    ser.close()
    ser.port = COM
    ser.baudrate = BAUD_RATE
    ser.bytesize = BYTE_SIZE
    ser.parity = PARIT
    ser.stopbits = STOP_BITS
    ser.timeout = TIME_SERIAL
    ser.open()
    #print '##################################'
    #print 'Function  SerialConfig_1 load !!'
    #print '##################################'

def SerialConfig_2(COM , BAUD_RATE):
    global ser_2
    ser_2 = serial.Serial()
    ser_2.close()
    ser_2.port = COM
    ser_2.baudrate = BAUD_RATE
    ser_2.bytesize = BYTE_SIZE
    ser_2.parity = PARIT
    ser_2.stopbits = STOP_BITS
    ser_2.timeout = TIME_SERIAL
    ser.open()
    #print "##################################''
    #print "Function  SerialConfig_2 load !!"
    #print "##################################"
       
####################################################################################################################################
#SYNC withloaded
def Sync (): 
    D4_received_word = ''
    timeout_start = time.time()
    timeout = 10
    reset_time = 0
    while ((D4_received_word != "OK") and (time.time() < (timeout_start + timeout))):
        ser.write(chr(0x0)+chr(0x0)+ chr(0x0)+ chr(0x0)+chr(0x0)+chr(0x0)+ chr(0x0)+ chr(0x0)
                  +chr(0x0)+chr(0x0)+ chr(0x0)+ chr(0x0)+chr(0x0)+chr(0x0)+ chr(0x0)+ chr(0x0)
                  +chr(0x0)+chr(0x0)+ chr(0x0)+ chr(0x0)+chr(0x0)+chr(0x0)+ chr(0x0)+ chr(0x0)
                  +chr(0x0)+chr(0x0)+ chr(0x0)+ chr(0x0)+chr(0x0)+chr(0x0)+ chr(0x0)+ chr(0x0)) 
        D4_received_word = ser.read(2)
    if D4_received_word == "OK":
        time.sleep(0.1)
        Boot_Complete=1
        print "#################################"
        print "D4_received_word = " ,D4_received_word
        print "Got Sync"
        Add_To_File("Got Sync")
        Add_To_File("\n\n")
        print "#################################"

    else:
        print "#################################"
        print "D4_received_word = " ,D4_received_word
        print "NO Sync\n"
        Add_To_File("NO Sync")
        Add_To_File("\n\n")
        print "need Restart to the D6"
        Add_To_File("need Restart to the D6")
        reset ()
        time.sleep (1)
        
        print "#################################"
        print "call to the Sync function, loop number" ,reset_time
        print "\n\n"
        reset_time =  reset_time +1
        sync ()

####################################################################################################################################
#read APB Address
#################################
def read_apb_reg(addr):
    global apb_reg
    #fill with zero for 8 bit word
    if len(addr)<8:
        addr = addr.zfill(8)    
    #convert hexa value to ascii and divide to little indian
    asciiaddr6=binascii.unhexlify(addr[6]+addr[7])
    asciiaddr4=binascii.unhexlify(addr[4]+addr[5])
    asciiaddr2=binascii.unhexlify(addr[2]+addr[3])
    asciiaddr0=binascii.unhexlify(addr[0]+addr[1])

    ser.write(chr(0x5A)+chr(0x07)+asciiaddr6+asciiaddr4+asciiaddr2+asciiaddr0)
    time.sleep(0.1)
    reg=ser.read(20)
    
    #convert ascii to hex value
    apb_reg =binascii.hexlify(reg[5])+binascii.hexlify(reg[4])+binascii.hexlify(reg[3])+binascii.hexlify(reg[2])

    print "#################################"
    print "Read Address ", addr ,"return value", apb_reg
    Add_To_File("Read Address ")
    Add_To_File(addr)
    Add_To_File(' ')
    Add_To_File("return value ")
    Add_To_File(apb_reg)
    Add_To_File("\n\n")
    print "#################################"
    
print ''
print 'Function  read_apb_reg load !!'
print ''

#########################################################################################################################################################
#write APB Address
#################################
def write_apb_reg(addr,value):
    
    #fill with zero for 8 bit word
    if len(value)<8:
        value = value.zfill(8)
    if len(addr)<8:
        addr = addr.zfill(8)
    
    #convert hexa value to ascii and divide to little indian
    asciivalue6=binascii.unhexlify(value[6]+value[7])
    asciivalue4=binascii.unhexlify(value[4]+value[5])
    asciivalue2=binascii.unhexlify(value[2]+value[3])
    asciivalue0=binascii.unhexlify(value[0]+value[1])
    
    #convert hexa value to ascii and divide to little indian
    asciiaddr6=binascii.unhexlify(addr[6]+addr[7])
    asciiaddr4=binascii.unhexlify(addr[4]+addr[5])
    asciiaddr2=binascii.unhexlify(addr[2]+addr[3])
    asciiaddr0=binascii.unhexlify(addr[0]+addr[1])
    
    #write apb register- command to D4
    test = ser.write(chr(0x5A)+chr(0x04)+asciiaddr6+asciiaddr4+asciiaddr2+asciiaddr0+asciivalue6+asciivalue4+asciivalue2+asciivalue0)
    time.sleep(0.1)
    
    print '#################################'
    print "Write Address ", addr ,"with value", value
    Add_To_File("Write Address ")
    Add_To_File(addr)
    Add_To_File(' ')
    Add_To_File("with value ")
    Add_To_File(value)
    Add_To_File("\n\n")
    print "#################################"
    
print ''
print 'Function  read_apb_reg load !!'
print '##################################'

#########################################################################################################################################################
#checkSum
#################################
def checkSum():

    # Check Checksum
    ser.write(chr(0x5A))
    ser.write(chr(0x0E))
    ## FW send echo + Checksum(4 bytes)
    ser.flushInput()
    ReadSerial = ser.read(8)
    time.sleep(0.1)
    
    
    ser.flushInput()
    time.sleep(0.5)
    
    print '#################################'
    print "Check Checksum", ReadSerial 
    Add_To_File("Check Checksum")
    Add_To_File(ReadSerial)
    Add_To_File("\n\n")
    print "#################################"
    #print ''
    #print 'Function  checkSum load !!'
    #print '##################################'

    print ''
    print 'Function  checkSum load !!'
    print '##################################'

#########################################################################################################################################################
# create a new directory 
#################################
def Make_Dir(Dir_Name):
    
    if not os.path.exists(Dir_Name):
        os.makedirs(Dir_Name)

def Open_log(Log_Name):
    Make_Dir(Dir_Name) # call to the make dir function
    
    global Current_File_Name
    temp = Dir_Name + Log_Name
    Current_File_Name = temp
    print temp
    openfile = open(temp , 'w')
    openfile.write(Log_Name)
    openfile.write("\n")
    openfile.close()
    
#########################################################################################################################################################
# Add_To_File = Add content to the exists file 
#################################

def Add_To_File(Add_Line):
    
    f = open(Current_File_Name, 'a')
    f.write(Add_Line)
    #f.write("\n")
    f.close()

#########################################################################################################################################################
# reset = set GPIO 10 low for reset purpose
#GPIO10 must be physically connected to reset button (SW1-pin 3)!!!!!!!!
#################################
def reset():
    #GP_DIR_OUT configure GPIO10 to output
    write_apb_reg("04000010","0400")
    time.sleep (1)
    #GP_DATA_CLR configure GPIO10 to low (set to 0)
    write_apb_reg("04000008","0400")
    print "Reset the D6 Board"
    
#########################################################################################################################################################
# clear_bit = clear the wanted bits in the register
#################################
def clear_bit(addr,bits_clr_hex):
    if len(bits_clr_hex)<8:
        bits_clr_hex = bits_clr_hex.zfill(8)
    if len(addr)<8:
       addr = addr.zfill(8)

    #get current value and change it to binary
    read_apb_reg(addr)
    reg=int(apb_reg,16)
    binReg=bin(reg).zfill(32)
    #print ("bin reg:       ", binReg[2:])
    
    #change the bits clear value from hex to binary
    int_bits_clr=int(bits_clr_hex,16)
    bin_bits_clr=bin(int_bits_clr).zfill(32)
    #print ("bin bits clr:  ",bin_bits_clr[:])
    
    #execute set by using (A and not(B)) operator between current value to the wanted bits to be set
    fin_reg=0
    int_fin_reg=0
    int_fin_reg=(~(int_bits_clr) & reg)
    bin_fin_reg=bin(int_fin_reg).zfill(32)
    #print ("bin final:     ", bin_fin_reg[2:])
    
    #change the value of the register, after set was done, to hex
    hex_1=hex(int_fin_reg)
    hex_2=hex_1[2:]
    hex_fin_reg=hex_2[:8]
    #print ("hex final:  ",hex_fin_reg)
    
    #write the new value to the register
    print ""
    print " Clear the following Address : " ,addr ," with value " ,hex_fin_reg
    print ""
    write_apb_reg(addr,hex_fin_reg)

#########################################################################################################################################################
# set_bit = set the wanted bits in the register 
#################################
def set_bit(addr,bits_set_hex):
    if len(bits_set_hex)<8:
        bits_set_hex = bits_set_hex.zfill(8)
    if len(addr)<8:
       addr = addr.zfill(8)
    #print ("address:  ",addr,"set value:  ",bits_set_hex)   
    
    #get current value and change it to binary
    read_apb_reg(addr)
    reg=int(apb_reg,16)
    binReg=bin(reg).zfill(32)
    #print ("bin reg:       ", binReg[2:])
    
    #change the bits_set value from hex to binary
    int_bits_set=int(bits_set_hex,16)
    bin_bits_set=bin(int_bits_set).zfill(32)
    #print ("bin bits set:  ", bin_bits_set[:])
    
    #execute set by using OR operator between current value to the wanted bits to be set
    fin_reg=0
    int_fin_reg=0
    int_fin_reg=(int_bits_set | reg)
    bin_fin_reg=bin(int_fin_reg).zfill(32)
    #print ("bin final:     ", bin_fin_reg[2:])
    
    #after set was done, change the value to hex before calling write_apb_reg function
    hex_1=hex(int_fin_reg)
    hex_2=hex_1[2:]
    hex_fin_reg=hex_2[:8]
    #print ("hex final:  ",hex_fin_reg)
    
    #write the new value to the register
    print ""
    print " Set the following Address : " ,addr ," with value " ,hex_fin_reg
    print ""
    write_apb_reg(addr,hex_fin_reg)


#########################################################################################################################################################
# create_excel_log = create excel log file
#################################    
    
def create_excel_log(Log_Name_Excel,Sheet_Name,name_columnA,name_columnB,name_columnC,name_columnD,name_columnE,name_columnF,name_columnG,name_columnH,name_columnI,name_columnJ):
    Make_Dir(Dir_Name) # call to the make dir function
    global Current_File_Name_xls
    global wb
    global ws
    global index_1
    
    temp = Dir_Name + Log_Name_Excel
    Current_File_Name_xls = temp
    print temp
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = Sheet_Name
    print(wb.get_sheet_names())
    print os.getcwd()    
    #ws = wb.get_sheet_by_name("Results")
    #wb = openpyxl.load_workbook(Test_Name)
    #d = ws.cell(row = 4, column = 2)
    #c = ws.cell('A4')
    #c = ws['A4']
    #cell_range = ws['A1':'C2']
    #c.value = 'hello, world'
    #print(c.value)
    
    index_1=ws.max_row
    print index_1
   # index_2=ws.max_column
    if index_1==0:
        ws.cell(row=index_1+1, column=1).value=name_columnA
        ws.cell(row=index_1+1, column=2).value=name_columnB
        ws.cell(row=index_1+1, column=3).value=name_columnC
        ws.cell(row=index_1+1, column=4).value=name_columnD
        ws.cell(row=index_1+1, column=5).value=name_columnE
        ws.cell(row=index_1+1, column=6).value=name_columnF
        ws.cell(row=index_1+1, column=7).value=name_columnG
        ws.cell(row=index_1+1, column=8).value=name_columnH
        ws.cell(row=index_1+1, column=9).value=name_columnI
        ws.cell(row=index_1+1, column=10).value=name_columnJ
        #ws['A1']=name_columnA
        #ws['B1']=name_columnB
        #ws['C1']=name_columnC
        #ws['D1']=name_columnD
        #ws['E1']=name_columnE
        #ws['F1']=name_columnF
        #ws['G1']=name_columnG
        #ws['H1']=name_columnH
        #ws['I1']=name_columnI
        #ws['J1']=name_columnJ
    else:
        print "title row already exist"
    wb.save(Current_File_Name_xls)
    #Log_Name_Excel
   # Excel_Name=Log_Name_Excel
   # return Excel_Name
    #get_column_letter(sheet.max_column)
    #column_index_from_string('A')
    
    
#########################################################################################################################################################
# call_excel_file = call an existing excel file and give you the required work sheet
#################################   
def call_excel_file(Current_File_Name_xls,Sheet_Name):
    wb = openpyxl.load_workbook(Current_File_Name_xls)
    ws = wb.get_sheet_by_name(Sheet_Name)
    #ws=wb.active
   
    
# MEM_BIST = function run the BIST test 
#################################
def MEM_BIST(test_name,write_val,status_reg,result_val,LDO,Chip_No,Chiptype,Temperature,STRAP,Voltage,Frequency,Sheet_Name):
    chiptype=Chiptype
    voltage=Voltage
    temperature=Temperature
    
    call_excel_file(Current_File_Name_xls,Sheet_Name)
    index_1=ws.max_row
    print index_1

    ws.cell(row=index_1+1, column=3).value=test_name
    ws.cell(row=index_1+1, column=1).value=Chip_No
    ws.cell(row=index_1+1, column=2).value=Chiptype
    ws.cell(row=index_1+1, column=4).value=Temperature
    ws.cell(row=index_1+1, column=5).value=STRAP
    ws.cell(row=index_1+1, column=6).value=Voltage
    ws.cell(row=index_1+1, column=7).value=Frequency

    wb.save(Current_File_Name_xls)


    read_apb_reg("0300004c")
    write_apb_reg("0300004c","88025614")
    read_apb_reg("0300004c")
    write_apb_reg("030000ec","2100")
    read_apb_reg("030000ec")
    
    #print "D0"-BIST status register
    read_apb_reg("030000d0")
    #print "D4"-BIST status register
    read_apb_reg("030000d4")
    #print "CC"-BIST CNTRL register
    read_apb_reg("030000cc")
     
    #configure LDO supply
    #input voltage (VCC) is 1.1V 
    if LDO=="0.9":
        set_bit("0300003c","0008")  #LC=15, LDO level in VDD =15
        set_bit("0300003c","0070")  #LDO enable
        Add_To_File("\n\n")
        Add_To_File("LDO 0.9V")
        Add_To_File("\n\n")
    elif LDO=="0.855":
        #set_bit("0300003c","0006")  #LC=15, LDO level in VDD =15
        #set_bit("0300003c","0070")  #LDO enable
        write_apb_reg("0300003c","0077")
        Add_To_File("\n\n")
        Add_To_File("LDO 0.855V")
        Add_To_File("\n\n")
    elif LDO=="bypass":
        set_bit("03000044","1")     #enable weak pull
        clear_bit("0300003c","0010")#LDO disable 
        clear_bit("03000044","1")   #disable weak pull
        Add_To_File("\n\n")
        Add_To_File("LDO in Bypass")
        Add_To_File("\n\n")
    else:
        print "LDO not chosen"
        Add_To_File("\n\n")
        Add_To_File("LDO not chosen")
        Add_To_File("\n\n") 
         
    #added configuration for this two tests
    print "#######",test_name,"#######"
    if test_name=="HWVAD":
        write_apb_reg("03000020","500")
        time.sleep(0.5)
    if test_name=="PTCM":	
        write_apb_reg("030000cc","c000")
        time.sleep(0.5)
    
    #configure MEM GROUP SELECT + ENABLE BIST
    write_apb_reg("030000cc",write_val)
    time.sleep(2)
    
    #### Status Register Read
    #for ROM test compare signature value
    if test_name=="ROM":
        ROM_sig="0110100000111101000001101100000010111100011011100000011111111111"
        ROM_sig_LSB=ROM_sig[0:32]
        ROM_sig_MSB=ROM_sig[32:64]
        ROM_sig_LSB_addr="030000d8"
        ROM_sig_MSB_addr="030000dc"
        read_apb_reg("030000d8")
        ROM_sig_LSB_read=apb_reg
        reg=int(apb_reg,16)
        ROM_sig_LSB_read=bin(reg).zfill(32)
        print "LSB register -bin"
        print ROM_sig_LSB_read[2:33]
        read_apb_reg("030000dc")
        reg=int(apb_reg,16)
        ROM_sig_MSB_read=bin(reg).zfill(32)
        print "MSB register -bin"
        print ROM_sig_MSB_read[2:33]
        if ((ROM_sig_LSB_read[2:33]==ROM_sig_LSB)&(ROM_sig_MSB_read[2:33]==ROM_sig_MSB)):
            end_res=1
        else:
            end_res=0
    else:
        read_apb_reg(status_reg)
    
    #show read status register in Binary 32bit
    reg=int(apb_reg,16)
    binReg=bin(reg).zfill(32)
    print "status register -bin"
    print binReg[2:33]
    
    #show wanted result comparator in Binary 32bit
    result=int(result_val,16)
    print "comparator - bin"
    print bin(result).zfill(32)
    
    #show the result of comparison in Binary 32bit
    end_res=0
    end_res=reg & result
    print "end result after comparing"
    print bin(end_res).zfill(32)        
            
    #if the end-result 0 - pass, else - fail
    if end_res > 0 :
        Add_To_File("Chiptype:  ")
        Add_To_File(Chiptype)
        Add_To_File("  , Temperature:  ")
        Add_To_File(temperature)
        Add_To_File(" , Voltage:  ")    
        Add_To_File(voltage)
        Add_To_File(' : ')
        Add_To_File(test_name)
        Add_To_File(': ')
        Add_To_File("fail")
        Add_To_File("\n\n")
        pass_fail="fail"
        print "fail"
    else:

        Add_To_File("Chiptype:  ")
        Add_To_File(Chiptype)
        Add_To_File("  , Temperature:  ")
        Add_To_File(temperature)
        Add_To_File(" , Voltage:  ")    
        Add_To_File(voltage)
        Add_To_File(' : ')
        Add_To_File(test_name)
        Add_To_File(': ')
        Add_To_File("pass")
        Add_To_File("\n\n")
        pass_fail="pass"
        print "pass"
    
    ws.cell(row=index_1+1, column=9).value=pass_fail
    ws.cell(row=index_1+1, column=10).value=apb_reg
    wb.save(Current_File_Name_xls)
    return pass_fail

#########################################################################################################################################################
# Clock out for D4 - D6
#################################
def Clock_Out (clock_source):
    print ("/n/n selected clock source out on GPIO4 = " , clock_source, "\n\n")
    # set GPIO4 to clock P function , reg IOM1
    write_apb_reg ("0300004c","88025215")
    time.sleep(1)
    if  clock_source == "PLL":
            # set clock out ,reg TEST_MODES_CTRL1
            write_apb_reg("030000ec","2140")
            time.sleep(1)
    elif    clock_source == "Global":
                # set clock out ,reg TEST_MODES_CTRL1 tp OSC
                write_apb_reg("030000ec","20c0")
                time.sleep(1)
    elif    clock_source == "OSC":
                # set clock out ,reg TEST_MODES_CTRL1
                write_apb_reg("030000ec","2180")
                time.sleep(1)
                
#########################################################################################################################################################
# change the oscillator frequency for D4 - D6
########################################################################### 
    
def System_OSC_freq(freq):
    if freq== "32":
        Add_To_File("\n\n Switch to OSC , OSC freq = 32M \n\n")
        print "\n\n Switch to OSC , OSC freq = 32M \n\n"
        read_apb_reg ("3000084")
        print "\n\n set OSC to 32M \n\n"
        write_apb_reg("03000084","800323E8")
        time.sleep(2)
        read_apb_reg ("3000008")
        print "\n\n Move the system to OSC 32M \n\n"
        write_apb_reg("03000008","08000000")
        time.sleep(2)
        print "\n\n Change the COM Baudrate to" ,BaudRateCalculation (Integer,Frac,32768000.0)
        print "\n\n" 
        SerialConfig_1(COM , BaudRateCalculation (Integer,Frac,32768000.0))
        time.sleep(2)
        read_apb_reg ("3000084")
        print "\n\n System successfully moved to 32M OSC!!! \n\n"
        Add_To_File("\n\n System successfully moved to 32M OSC!!! \n\n")
    elif freq =="92":
        Add_To_File("\n\n Switch to OSC , OSC freq = 92M \n\n")
        print "\n\n Switch to OSC , OSC freq = 92M \n\n"
        read_apb_reg ("3000084")
        print "\n\n set OSC to 92M \n\n"
        write_apb_reg("03000084","80032b02")
        time.sleep(2)
        read_apb_reg ("3000008")
        print "\n\n Move the system to OSC 92M \n\n"
        write_apb_reg("03000008","8000000")
        time.sleep(2)
        print "\n\n Change the COM Baudrate to" , BaudRateCalculation (Integer,Frac,92340224.0)
        SerialConfig_1(COM ,  BaudRateCalculation (Integer,Frac,92340224.0))
        time.sleep(2)
        read_apb_reg ("3000084")
        print "\n\n System successfully moved to 92M OSC!!! \n\n"
        Add_To_File("\n\n System successfully moved to 92M OSC!!! \n\n")
    else:
        print "wrong oscillator frequency entered"
        Add_To_File("wrong oscillator frequency entered")
        
#########################################################################################################################################################
# change the PLL system clock for D4 - D6
#################################

def System_Clock_PLL (freq ,OSC_Freq,chip_type ):
    System_OSC_freq(OSC_Freq)
    ##################################
    if freq == "25": #25,1986MHz
        print "\n\n start to configure the System_Clock_PLL to " ,freq ,"MHz\n\n"
        Add_To_File("Start to Configure the System_Clock_PLL to = ")
        Add_To_File(freq)
        Add_To_File("\n\n")
        # change the PLL  div reg
        write_apb_reg("3000004", "30000000") 
        write_apb_reg("3000004", "30030100")
        time.sleep(2)
        # change the PLL  BWAJ
        if chip_type == "D4" :
            write_apb_reg("3000000", "1180")
            time.sleep(2)
        else :
            write_apb_reg("3000000", "4000000")
            write_apb_reg("3000004", "20030100")

        print "\n Return the system to PLL \n"
        write_apb_reg("3000000", "40000400")
        write_apb_reg ("3000008", "00000000")
        time.sleep(2)
        print "\nChange the COM Baudrate to 387670\n"
        SerialConfig_1(COM , 387670)
        print "\nChange the COM Baudrate to" , BaudRateCalculation (Integer,Frac,25198600.0)
        SerialConfig_1(COM , BaudRateCalculation (Integer,Frac,25198600.0))
        print "\nChange the COM Baudrate to" , BaudRateCalculation (Integer,Frac,25198600.0)
        SerialConfig_1(COM , BaudRateCalculation (Integer,Frac,25198600.0))
        time.sleep(2)
        read_apb_reg ("3000004")
        print" \n\n configure System_Clock_PLL to " ,freq ,"MHz Completed !!!"
        Add_To_File("\n\n")
        Add_To_File(" configure System_Clock_PLL to ")
        Add_To_File(freq)
        Add_To_File("MHz Completed !!!\n\n")
        Add_To_File("\n\n")
    ##################################
    elif freq == "32": #32.768MHz
        print"\n\n start to configure the System_Clock_PLL to " ,freq ,"MHz\n\n"
        Add_To_File("Start to Configure the System_Clock_PLL to = ")
        Add_To_File(freq)
        Add_To_File("\n\n")
        # change the PLL  div reg
        write_apb_reg("3000004", "30000000") 
        write_apb_reg("3000004", "3003e700") 
        time.sleep(2)
        # change the PLL  BWAJ
        if chip_type == "D4" :
            write_apb_reg("3000000", "11f3")
        else :
            write_apb_reg("3000000", "40000400")
            write_apb_reg("3000004", "2003e700")
        time.sleep(2)
        print "\n Return the system to PLL \n"
        write_apb_reg ("3000008", "00000000")
        time.sleep(2)
        print "\nChange the COM Baudrate to " ,BaudRateCalculation (Integer,Frac,32768000.0)
        SerialConfig_1(COM , BaudRateCalculation (Integer,Frac,32768000.0))
        time.sleep(2)
        read_apb_reg ("3000004")
        print" \n\n configure System_Clock_PLL to " ,freq ,"MHz Completed !!!"
        Add_To_File("\n\n")
        Add_To_File(" configure System_Clock_PLL to ")
        Add_To_File(freq)
        Add_To_File("MHz Completed !!!\n\n")
        Add_To_File("\n\n")
    ##################################
    elif freq == "49": #49.152MHz
        print"\n\n start to configure the System_Clock_PLL to " ,freq ,"MHz\n\n"
        Add_To_File("Start to Configure the System_Clock_PLL to = ")
        Add_To_File(freq)
        Add_To_File("\n\n")
        # change the PLL  div reg
        write_apb_reg("3000004", "30000000") 
        write_apb_reg("3000004", "3005db00") 
        time.sleep(2)
        # change the PLL  BWAJ
        if chip_type == "D4" :
            write_apb_reg("3000000", "12ed")
        else :
            write_apb_reg("3000000", "40000400")
            write_apb_reg("3000004", "2005db00")
        time.sleep(2)
        print "\n Return the system to PLL \n"
        write_apb_reg ("3000008", "00000000")
        time.sleep(2)
        print "\nChange the COM Baudrate to " ,BaudRateCalculation (Integer,Frac,49152000.0)
        SerialConfig_1(COM , BaudRateCalculation (Integer,Frac,49152000.0))
        time.sleep(2)
        read_apb_reg ("3000004")
        print" \n\n configure System_Clock_PLL to " ,freq ,"MHz Completed !!!"
        Add_To_File("\n\n")
        Add_To_File(" configure System_Clock_PLL to ")
        Add_To_File(freq)
        Add_To_File("MHz Completed !!!\n\n")
        Add_To_File("\n\n")
        ##################################
    elif freq == "73": #73.728Mhz
        print"\n\n start to configure the System_Clock_PLL to " ,freq ,"MHz\n\n"
        Add_To_File("Start to Configure the System_Clock_PLL to = ")
        Add_To_File(freq)
        Add_To_File("\n\n")
        # change the PLL  div reg
        write_apb_reg("3000004", "30000000") 
        write_apb_reg("3000004", "3008c900") 
        time.sleep(2)
        # change the PLL  BWAJ
        if chip_type == "D4" :
            write_apb_reg("3000000", "1464")
            time.sleep(2)
        else:
            write_apb_reg("3000000", "40000400")
            write_apb_reg("3000004", "2008c900")
        print "\n Return the system to PLL \n"
        write_apb_reg ("3000008", "00000000")
        time.sleep(2)
        print "\nChange the COM Baudrate to" , BaudRateCalculation (Integer,Frac,73728000.0)
        SerialConfig_1(COM , BaudRateCalculation (Integer,Frac,73728000.0))
        time.sleep(2)
        read_apb_reg ("3000004")
        print" \n\n configure System_Clock_PLL to " ,freq ,"MHz Completed !!!"
        Add_To_File("\n\n")
        Add_To_File(" configure System_Clock_PLL to ")
        Add_To_File(freq)
        Add_To_File("MHz Completed !!!\n\n")
        Add_To_File("\n\n")
        ##################################
    elif freq == "82": # 82,247,680 hz
        print"\n\n start to configure the System_Clock_PLL to " ,freq ,"MHz\n\n"
        Add_To_File("Start to Configure the System_Clock_PLL to = ")
        Add_To_File(freq)
        Add_To_File("\n\n")
        # change the PLL  div reg
        write_apb_reg("3000004", "30000000") 
        write_apb_reg("3000004", "3009cd00") 
        time.sleep(2)
        # change the PLL  BWAJ
        if chip_type == "D4" :
            write_apb_reg("3000000", "14e6")
            time.sleep(2)
        else :
            write_apb_reg("3000000", "40000400")
            write_apb_reg("3000004", "2009cd00")
        print "\n Return the system to PLL \n"
        write_apb_reg ("3000008", "00000000")
        time.sleep(2)
        print "\nChange the COM Baudrate to " , BaudRateCalculation (Integer,Frac,82247680.0)
        SerialConfig_1(COM , BaudRateCalculation (Integer,Frac,82247680.0))
        time.sleep(2)
        read_apb_reg ("3000004")
        print" \n\n configure System_Clock_PLL to " ,freq ,"MHz Completed !!!"
        Add_To_File("\n\n")
        Add_To_File(" configure System_Clock_PLL to ")
        Add_To_File(freq)
        Add_To_File("MHz Completed !!!\n\n")
        Add_To_File("\n\n")
        ##################################
    elif freq == "92": #91979776MHz
        print"\n\n start to configure the System_Clock_PLL to " ,freq ,"MHz\n\n"
        Add_To_File("Start to Configure the System_Clock_PLL to = ")
        Add_To_File(freq)
        Add_To_File("\n\n")
        # change the PLL  div reg
        write_apb_reg("3000004", "30000000") 
        write_apb_reg("3000004", "300af600") 
        time.sleep(2)
        # change the PLL  BWAJ
        if chip_type == "D4" :
            write_apb_reg("3000000", "157b")
            time.sleep(2)
        else :
            write_apb_reg("3000000", "40000400")
            write_apb_reg("3000004", "200af600")   
        print "\n Return the system to PLL \n"
        write_apb_reg ("3000008", "00000000")
        time.sleep(2)
        print "\nChange the COM Baudrate to " , BaudRateCalculation (Integer,Frac,91979776)
        SerialConfig_1(COM , BaudRateCalculation (Integer,Frac,91979776))
        time.sleep(2)
        read_apb_reg ("3000004")
        print" \n\n configure System_Clock_PLL to " ,freq ,"MHz Completed !!!"
        Add_To_File("\n\n")
        Add_To_File(" configure System_Clock_PLL to ")
        Add_To_File(freq)
        Add_To_File("MHz Completed !!!\n\n")
        Add_To_File("\n\n")
        ##################################
    elif freq == "98": #98.304Mhz
        print"\n\n start to configure the System_Clock_PLL to " ,freq ,"MHz\n\n"
        Add_To_File("Start to Configure the System_Clock_PLL to = ")
        Add_To_File(freq)
        Add_To_File("\n\n")
        # change the PLL  div reg
        write_apb_reg("3000004", "30000000") 
        write_apb_reg("3000004", "300bb700") 
        time.sleep(2)
        # change the PLL  BWAJ
        if chip_type == "D4" :
            write_apb_reg("3000000", "15db")
            time.sleep(2)
        else :
            write_apb_reg("3000000", "40000400")
            write_apb_reg("3000004", "200bb700")   
        print "\n Return the system to PLL \n"
        write_apb_reg ("3000008", "00000000")
        time.sleep(2)
        print "\nChange the COM Baudrate to" , BaudRateCalculation (Integer,Frac,98304000.0)
        SerialConfig_1(COM , BaudRateCalculation (Integer,Frac,98304000.0))
        time.sleep(2)
        read_apb_reg ("3000004")
        print" \n\n configure System_Clock_PLL to " ,freq ,"MHz Completed !!!"
        Add_To_File("\n\n")
        Add_To_File(" configure System_Clock_PLL to ")
        Add_To_File(freq)
        Add_To_File("MHz Completed !!!\n\n")
        Add_To_File("\n\n")
        ##################################
    else :
        print "Error no legal freq selected"
###############################################################################################################################
 
def All_Memory_Power_Mode (power_mode, on_off):
    if (power_mode == "light_sleep" ):
        #need to verify clear bit of the following modes := deep_sleep and  shut_down
        print"clear the bits of deep_sleep"
        clear_bit (MEM_PWR_MD_DS1,"3ffffff")
        clear_bit (MEM_PWR_MD_DS2,"ffe")
        print"clear the bits of shut_down"
        clear_bit (MEM_PWR_MD_SD1,"3ffffff")
        clear_bit (MEM_PWR_MD_DS1,"ffe")
        if (on_off == 1):
            #set the light_sleep mode
            set_bit (MEM_PWR_MD_LS1,"3ffffff")
            set_bit (MEM_PWR_MD_LS2,"1fff")
            print"all the following block enter to light_sleep"
            print"PTCM0_LS_EN , DTCM0_LS_EN , TAG0_LS_EN , CACHE0_LS_EN , HWVAD1 , ROM , PAHB0 , HWVAD0"
        else :
            clear_bit (MEM_PWR_MD_LS1,"3ffffff")
            clear_bit (MEM_PWR_MD_LS2,"1fff")
        
    elif (power_mode == "deep_sleep" ):
        #need to verify clear bit of the following modes := light_sleep and  shut_down
        print ""
        print "clear the bits of deep_sleep"
        print ""
        clear_bit (MEM_PWR_MD_LS1,"3ffffff")
        clear_bit (MEM_PWR_MD_LS2,"1fff")
        print ""
        print"clear the bits of shut_down"
        print ""
        clear_bit (MEM_PWR_MD_SD1,"3ffffff")
        clear_bit (MEM_PWR_MD_DS1,"ffe")
        if (on_off == 1):
            #set the deep_sleep mode
            set_bit (MEM_PWR_MD_DS1,"3ffffff")
            set_bit (MEM_PWR_MD_DS1,"ffe")
            print ""
            print"all the following block enter to deep_sleep \n\n"
            print"PTCM0_LS_EN , DTCM0_LS_EN , TAG0_LS_EN , CACHE0_LS_EN , PAHB0 "
            print ""
        else :
            print ""
            print"SET Momory in Active Mode"
            print ""
            clear_bit (MEM_PWR_MD_DS1,"3ffffff")
            clear_bit (MEM_PWR_MD_DS1,"ffe")
        
    elif (power_mode == "shut_down" ):
        if (on_off == 1):
            set_bit (MEM_PWR_MD_SD1,"3ffffff")
            set_bit (MEM_PWR_MD_DS1,"ffe")
            print ""
            print"all the following block enter to shut_down \n\n"
            print"PTCM0_LS_EN , DTCM0_LS_EN , TAG0_LS_EN , CACHE0_LS_EN , HWVAD1 , ROM , PAHB0 , HWVAD0"
            print ""
        else:
            print ""
            print"SET Memory in Active Mode"
            print ""
            clear_bit (MEM_PWR_MD_DS1,"3ffffff")
            clear_bit (MEM_PWR_MD_DS1,"ffe")
            print ""
            print"clear the bits of deep_sleep"
            print ""
            clear_bit (MEM_PWR_MD_LS1,"3ffffff")
            clear_bit (MEM_PWR_MD_LS2,"1fff")
            print ""
            print"clear the bits of shut_down"
            print ""
            clear_bit (MEM_PWR_MD_SD1,"3ffffff")
            clear_bit (MEM_PWR_MD_DS1,"ffe")
            
    print "power mode configure to " , power_mode        
###############################################################################################################################
###############################################################################################################################   
def  Memory_Block_Select (memory_name , memory_section , mode):
    All_Memory_Power_Mode ("light_sleep" , 0)

    list1 = [PTCM,DTCM,TAG,CACHE,PAHB]
    list2 = [HWVAD0, HWVAD1,PAHB,ROM]
    
    if (mode == "light_sleep" ):
        if (memory_name in list1):
            set_bit (MEM_PWR_MD_LS1,memory_name[memory_section])
        elif (memory_name in list2):
            set_bit (MEM_PWR_MD_LS2,memory_name[memory_section])
        print ""
        print "set bit for " , memory_name[memory_section] , ", on section = ", memory_section , ",  power mode = " , mode
        print ""
    elif (mode == "deep_sleep" ):
        if (memory_name in list1):
            set_bit (MEM_PWR_MD_DS1,memory_name[memory_section])
        elif (memory_name in list2):
            set_bit (MEM_PWR_MD_DS2,memory_name[memory_section])
        print ""
        print "set bit for " , memory_name[memory_section] , ", on section = ", memory_section , ",  power mode = " , mode
        print ""
    elif (mode == "shut_down" ):
        if (memory_name in list1):
            set_bit (MEM_PWR_MD_SD1,memory_name[memory_section])
        elif (memory_name in list2):
            set_bit (MEM_PWR_MD_SD2,memory_name[memory_section])
        print ""
        print "set bit for " , memory_name , memory_name[memory_section] , ", on section = ", memory_section , ", power mode = " , mode
        print ""          
def BaudRateCalculation(Integer,Frac ,APB_Clock):
    
    buad_rate = (1.0/16.0*(APB_Clock/(Integer+Frac/16)))
    return int (buad_rate)

    













