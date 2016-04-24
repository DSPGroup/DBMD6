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
    print "#####read:" 
    print ("address: ",addr)
    global apb_reg
    #fill with zero for 8 bit word
        
    #convert hexa value to ascii and divide to little indian
    #print addr6
    #print addr4
    asciiaddr6=binascii.unhexlify(addr[6]+addr[7])
    asciiaddr4=binascii.unhexlify(addr[4]+addr[5])
    asciiaddr2=binascii.unhexlify(addr[2]+addr[3])
    asciiaddr0=binascii.unhexlify(addr[0]+addr[1])
    #read apb register- command to D4
    #read apb register- command to D4
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
    print "#####write:" 
    
    #fill with zero for 8 bit word
    if len(value)<8:
        value = value.zfill(8)
    if len(addr)<8:
        addr = addr.zfill(8)
    print ("address: ",addr, "value: ",value)
    
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
    print ("addr:  ",addr,"clear value:  ",bits_clr_hex)
   
    #get current value and change it to binary
    read_apb_reg(addr)
    reg=int(apb_reg,16)
    binReg=bin(reg).zfill(32)
    print ("bin reg:       ", binReg[2:])
    
    #change the bits clear value from hex to binary
    int_bits_clr=int(bits_clr_hex,16)
    bin_bits_clr=bin(int_bits_clr).zfill(32)
    print ("bin bits clr:  ",bin_bits_clr[:])
    
    #execute set by using (A and not(B)) operator between current value to the wanted bits to be set
    fin_reg=0
    int_fin_reg=0
    int_fin_reg=(~(int_bits_clr) & reg)
    bin_fin_reg=bin(int_fin_reg).zfill(32)
    print ("bin final:     ", bin_fin_reg[2:])
    
    #change the value of the register, after set was done, to hex
    hex_1=hex(int_fin_reg)
    hex_2=hex_1[2:]
    hex_fin_reg=hex_2[:8]
    print ("hex final:  ",hex_fin_reg)
    
    #write the new value to the register
    write_apb_reg(addr,hex_fin_reg)

#########################################################################################################################################################
# set_bit = set the wanted bits in the register 
#################################
def set_bit(addr,bits_set_hex):
    if len(bits_set_hex)<8:
        bits_set_hex = bits_set_hex.zfill(8)
    if len(addr)<8:
       addr = addr.zfill(8)
    print ("address:  ",addr,"set value:  ",bits_set_hex)   
    
    #get current value and change it to binary
    read_apb_reg(addr)
    reg=int(apb_reg,16)
    binReg=bin(reg).zfill(32)
    print ("bin reg:       ", binReg[2:])
    
    #change the bits_set value from hex to binary
    int_bits_set=int(bits_set_hex,16)
    bin_bits_set=bin(int_bits_set).zfill(32)
    print ("bin bits set:  ", bin_bits_set[:])
    
    #execute set by using OR operator between current value to the wanted bits to be set
    fin_reg=0
    int_fin_reg=0
    int_fin_reg=(int_bits_set | reg)
    bin_fin_reg=bin(int_fin_reg).zfill(32)
    print ("bin final:     ", bin_fin_reg[2:])
    
    #after set was done, change the value to hex before calling write_apb_reg function
    hex_1=hex(int_fin_reg)
    hex_2=hex_1[2:]
    hex_fin_reg=hex_2[:8]
    print ("hex final:  ",hex_fin_reg)
    
    #write the new value to the register
    write_apb_reg(addr,hex_fin_reg)

# MEM_BIST = function run the BIST test 
#################################
def MEM_BIST(test_name,write_val,status_reg,result_val,PLL,LDO):
   
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
        set_bit("0300003c","000f")  #LC=15, LDO level in VDD =15
        set_bit("0300003c","0010")  #LDO enable 
    elif LDO=="bypass":
        set_bit("03000044","1")     #enable weak pull
        clear_bit("0300003c","0010")#LDO disable 
        clear_bit("03000044","1")   #disable weak pull
    
    #configure PLL frequency and the UART new frequency
   # if PLL=="25":
        
    if PLL=="49":
        write_apb_reg("03000084","80032b02")
        write_apb_reg("03000008","8000000")
        write_apb_reg("0300004c","88025614")
        
       #uart 1418345
       # SerialConfig_1('COM9' , 1418345)
        
        read_apb_reg("03000000")
        write_apb_reg("030000ec","2280")
        write_apb_reg("0300004c","88025614")
        write_apb_reg("03000000","fff")
        write_apb_reg("03000004","5db00")
        write_apb_reg("03000008","0")
        #SerialConfig_1('COM9' , 754974)
        #uart 754974
        sync()
        checkSum()
    elif PLL=="73":
        write_apb_reg("03000084","80032b02")
        write_apb_reg("0300004c","88025614")
        #uart 1418345
        
        read_apb_reg("03000000")
        write_apb_reg("030000ec","2280")
        write_apb_reg("0300004c","88025614")
        write_apb_reg("03000000","fff")
        write_apb_reg("03000004","8c900")
        write_apb_reg("03000008","0")
        #uart 1132462
        
    elif PLL=="86":
        write_apb_reg("3000084","80032B02")
        write_apb_reg("3000008","8000000")
        write_apb_reg("300004c","88025614")
       
        #uart 1418345
        read_apb_reg("3000000")
        write_apb_reg("30000ec","2280")
        write_apb_reg("300004c","88025614")
        write_apb_reg("3000000","fff")
        write_apb_reg("3000004","a4000")
        write_apb_reg("3000008","0")
        #uart 1320000
 
    elif PLL=="98":
        write_apb_reg("3000084","80032B02")
        write_apb_reg("3000008","8000000")
        write_apb_reg("300004c","88025614")
       
        #uart 1418345
        read_apb_reg("3000000")
        write_apb_reg("30000ec","2280")
        write_apb_reg("300004c","88025614")
        write_apb_reg("3000000","fff")
        write_apb_reg("3000004","bb700")

    elif PLL=="122":
        write_apb_reg("3000084","80032B02")
        write_apb_reg("3000008","8000000")
        write_apb_reg("300004c","88025614")
       
        #uart 1418345
        read_apb_reg("3000000")
        write_apb_reg("30000ec","2280")
        write_apb_reg("300004c","88025614")
        write_apb_reg("3000000","fff")
        write_apb_reg("3000004","ea500")
        write_apb_reg("3000008","0")
        #uart 1870000
        
        
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
        print "fail"
    else:
        print "pass"


#########################################################################################################################################################
# Clock out for D4 - D6
#################################
def Clock_Out (clock_source):
    print ("\n\n selected clock source out on GPIO4 = " , clock_source, "\n\n")
    # set GPIO4 to clock P function , reg IOM1
    write_apb_reg ("0300004c","88025215")
    # set GPIO4 to clock P function , reg IOM1
    write_apb_reg ("030000ec","2100")
    time.sleep(1)
    # we have bug hear 
    # set GPIO4 to clock P function , reg IOM1
    #set_bit ("0300001c", "10")
    #time.sleep(0.5)
    # set GPIO4 to correct direction , reg GP_DIR_OUT
    #set_bit("03000010", "10")
    #time.sleep(0.5)
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
# change the PLL system clock for D4 - D6
#################################

def System_Clock_PLL (freq):
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
    print "\n\n Change the COM Baudrate to 1418345 \n\n"
    SerialConfig_1(COM , 1418345)
    time.sleep(2)
    read_apb_reg ("3000084")
    print "\n\n System successfully moved to OSC!!! \n\n"
    ##################################
    if freq == "32": #32.768MHz
        print "\n\n start to configure the System_Clock_PLL to " ,freq ,"MHz\n\n"
        Add_To_File("Start to Configure the System_Clock_PLL to = ")
        Add_To_File(freq)
        Add_To_File("\n\n")
        # change the PLL  div reg
        write_apb_reg("3000004", "003e700") 
        time.sleep(2)
        # change the PLL  BWAJ
        write_apb_reg("3000000", "11f3")
        time.sleep(2)
        print "\n Return the system to PLL \n"
        write_apb_reg ("3000008", "00000000")
        time.sleep(2)
        print "\nChange the COM Baudrate to 504123\n"
        SerialConfig_1(COM , 504123)
        time.sleep(2)
        read_apb_reg ("3000004")
        print" \n\n configure System_Clock_PLL to " ,freq ,"MHz Completed !!!"
        Add_To_File(" configure System_Clock_PLL to ")
        Add_To_File(freq)
        Add_To_File("MHz Completed !!!\n\n")
    ##################################
    elif freq == "49": #49.152MHz
        print"\n\n start to configure the System_Clock_PLL to " ,freq ,"MHz\n\n"
        Add_To_File("Start to Configure the System_Clock_PLL to = ")
        Add_To_File(freq)
        Add_To_File("\n\n")
        # change the PLL  div reg
        write_apb_reg("3000004", "005db00") 
        time.sleep(2)
        # change the PLL  BWAJ
        write_apb_reg("3000000", "12ed")
        time.sleep(2)
        print "\n Return the system to PLL \n"
        write_apb_reg ("3000008", "00000000")
        time.sleep(2)
        print "\nChange the COM Baudrate to 756184 \n"
        SerialConfig_1(COM , 756184)
        time.sleep(2)
        read_apb_reg ("3000004")
        print" \n\n configure System_Clock_PLL to " ,freq ,"MHz Completed !!!"
        Add_To_File(" configure System_Clock_PLL to ")
        Add_To_File(freq)
        Add_To_File("MHz Completed !!!\n\n")
        ##################################
    elif freq == "73": #73.728Mhz
        print"\n\n start to configure the System_Clock_PLL to " ,freq ,"MHz\n\n"
        Add_To_File("Start to Configure the System_Clock_PLL to = ")
        Add_To_File(freq)
        Add_To_File("\n\n")
        # change the PLL  div reg
        write_apb_reg("3000004", "008c900") 
        time.sleep(2)
        # change the PLL  BWAJ
        write_apb_reg("3000000", "1464")
        time.sleep(2)
        print "\n Return the system to PLL \n"
        write_apb_reg ("3000008", "00000000")
        time.sleep(2)
        print "\nChange the COM Baudrate to 1134276 \n"
        SerialConfig_1(COM , 1134276)
        time.sleep(2)
        read_apb_reg ("3000004")
        print" \n\n configure System_Clock_PLL to " ,freq ,"MHz Completed !!!"
        Add_To_File(" configure System_Clock_PLL to ")
        Add_To_File(freq)
        Add_To_File("MHz Completed !!!\n\n")
        ##################################
    elif freq == "82": # 82,247,680 hz
        print"\n\n start to configure the System_Clock_PLL to " ,freq ,"MHz\n\n"
        Add_To_File("Start to Configure the System_Clock_PLL to = ")
        Add_To_File(freq)
        Add_To_File("\n\n")
        # change the PLL  div reg
        write_apb_reg("3000004", "009cd00") 
        time.sleep(2)
        # change the PLL  BWAJ
        write_apb_reg("3000000", "14e6")
        time.sleep(2)
        print "\n Return the system to PLL \n"
        write_apb_reg ("3000008", "00000000")
        time.sleep(2)
        print "\nChange the COM Baudrate to 1265348 \n"
        SerialConfig_1(COM , 1265348)
        time.sleep(2)
        read_apb_reg ("3000004")
        print" \n\n configure System_Clock_PLL to " ,freq ,"MHz Completed !!!"
        Add_To_File(" configure System_Clock_PLL to ")
        Add_To_File(freq)
        Add_To_File("MHz Completed !!!\n\n")
        ##################################
    elif freq == "92": #49.152MHz
        print"\n\n start to configure the System_Clock_PLL to " ,freq ,"MHz\n\n"
        Add_To_File("Start to Configure the System_Clock_PLL to = ")
        Add_To_File(freq)
        Add_To_File("\n\n")
        # change the PLL  div reg
        write_apb_reg("3000004", "00af600") 
        time.sleep(2)
        # change the PLL  BWAJ
        write_apb_reg("3000000", "157b")
        time.sleep(2)
        print "\n Return the system to PLL \n"
        write_apb_reg ("3000008", "00000000")
        time.sleep(2)
        print "\nChange the COM Baudrate to 1415384 \n"
        SerialConfig_1(COM , 1415384)
        time.sleep(2)
        read_apb_reg ("3000004")
        print" \n\n configure System_Clock_PLL to " ,freq ,"MHz Completed !!!"
        Add_To_File(" configure System_Clock_PLL to ")
        Add_To_File(freq)
        Add_To_File("MHz Completed !!!\n\n")
        ##################################
    elif freq == "98": #98.304Mhz
        print"\n\n start to configure the System_Clock_PLL to " ,freq ,"MHz\n\n"
        Add_To_File("Start to Configure the System_Clock_PLL to = ")
        Add_To_File(freq)
        Add_To_File("\n\n")
        # change the PLL  div reg
        write_apb_reg("3000004", "00bb700") 
        time.sleep(2)
        # change the PLL  BWAJ
        write_apb_reg("3000000", "15db")
        time.sleep(2)
        print "\n Return the system to PLL \n"
        write_apb_reg ("3000008", "00000000")
        time.sleep(2)
        print "\nChange the COM Baudrate to 1512369 \n"
        SerialConfig_1(COM , 1512369)
        time.sleep(2)
        read_apb_reg ("3000004")
        print" \n\n configure System_Clock_PLL to " ,freq ,"MHz Completed !!!"
        Add_To_File(" configure System_Clock_PLL to ")
        Add_To_File(freq)
        Add_To_File("MHz Completed !!!\n\n")
        ##################################
###############################################################################################################################
    else :
            print "Error no legal freq selected"






