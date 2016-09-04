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
    ser_2.open()
    #print "##################################''
    #print "Function  SerialConfig_2 load !!"
    #print "##################################"
       
####################################################################################################################################
#SYNC withloaded
def Sync (number_of_attampts): 
    D4_received_word = ''
    i=0
    while (i < number_of_attampts):
        ser.write(chr(0x0)+chr(0x0)+ chr(0x0)+ chr(0x0)+chr(0x0)+chr(0x0)+ chr(0x0)+ chr(0x0)
        +chr(0x0)+chr(0x0)+ chr(0x0)+ chr(0x0)+chr(0x0)+chr(0x0)+ chr(0x0)+ chr(0x0)+chr(0x0)+chr(0x0)+ chr(0x0)+ chr(0x0)
        +chr(0x0)+chr(0x0)+ chr(0x0)+ chr(0x0)+chr(0x0)+chr(0x0)+ chr(0x0)+ chr(0x0)+chr(0x0)+chr(0x0)+ chr(0x0)+ chr(0x0)
        +chr(0x0)+chr(0x0)+ chr(0x0)+ chr(0x0)+ chr(0x0)+ chr(0x0)+ chr(0x0)+ chr(0x0)+ chr(0x0)+ chr(0x0)+ chr(0x0)+ chr(0x0)) 
        time.sleep(0.3)
        D4_received_word = ser.read(2)
        if D4_received_word == "OK":
            time.sleep(0.1)
            Boot_Complete=1
            write_to_log("Synced!\n")
            break

        else:            
            write_to_log("Sync failed\n")
            write_to_log("Startover Sync function, loop number: "+str(i))
            write_to_log("Please restart D6")
            i=i+1
        

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

    write_to_log("Read Address ", addr ,"return value", apb_reg +'\n')
    

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
    
    write_to_log("Write Address: "+ addr +"with value"+ value + '\n')


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
   
    write_to_log("Checksun return: "+ ReadSerial + '\n')
    return ReadSerial
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
    openfile = open(temp , 'a')
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


def write_to_file(time, user_input):
	log_file = open(Current_File_Name, "a")
	log_file.write("%s\t" %time)
	log_file.write("%s\n" %user_input)
	log_file.close()

def write_to_log(user_input):
	time = datetime.datetime.today().strftime('%d/%m/%Y %H:%M:%S:%f')
	print time,'\t',user_input
	write_to_file(time, user_input)

    
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
    print "Please reset the D6 Board"
    
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
    write_to_log("Clear the following Address: "+ addr +" with value: " +hex_fin_reg)

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
    write_to_log("Set the following Address: " +addr +" with value: " +hex_fin_reg)

    write_apb_reg(addr,hex_fin_reg)

# MEM_BIST = function run the BIST test 
#################################
def MEM_BIST(test_name,write_val,status_reg,result_val,LDO,Voltage,Temperature):
    
    voltage=Voltage
    #voltage="1V"
    #voltage="1.1V"
    #voltage="1.21V"
    
    temperature=Temperature
    #temperature=-40C
    #temperature=25C
    #temperature=80C
    
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
    elif LDO=="bypass":
        set_bit("03000044","1")     #enable weak pull
        clear_bit("0300003c","0010")#LDO disable 
        clear_bit("03000044","1")   #disable weak pull
         
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
        Add_To_File("Temperature:  ")
        Add_To_File(temperature)
        Add_To_File(" , Voltage:  ")    
        Add_To_File(voltage)
        Add_To_File(' : ')
        Add_To_File(test_name)
        Add_To_File(': ')
        Add_To_File("fail")
        Add_To_File("\n\n")
        print "fail"
    else:

        Add_To_File("Temperature:  ")
        Add_To_File(temperature)
        Add_To_File(" , Voltage:  ")    
        Add_To_File(voltage)
        Add_To_File(' : ')
        Add_To_File(test_name)
        Add_To_File(': ')
        Add_To_File("pass")
        Add_To_File("\n\n")
        print "pass"


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
        time.sleep(1)
        # change the PLL  BWAJ
        if chip_type == "D4" :
            write_apb_reg("3000000", "1180")
            time.sleep(1)
        else :
            write_apb_reg("3000000", "4000000")
            write_apb_reg("3000004", "20030100")

        print "\n Return the system to PLL \n"
        write_apb_reg("3000000", "40000400")
        write_apb_reg ("3000008", "00000000")
        time.sleep(1)
        print "\nChange the COM Baudrate to 387670\n"
        SerialConfig_1(COM , 387670)
        print "\nChange the COM Baudrate to" , BaudRateCalculation (Integer,Frac,25198600.0)
        SerialConfig_1(COM , BaudRateCalculation (Integer,Frac,25198600.0))
        print "\nChange the COM Baudrate to" , BaudRateCalculation (Integer,Frac,25198600.0)
        SerialConfig_1(COM , BaudRateCalculation (Integer,Frac,25198600.0))
        time.sleep(1)
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
        time.sleep(1)
        # change the PLL  BWAJ
        if chip_type == "D4" :
            write_apb_reg("3000000", "11f3")
        else :
            write_apb_reg("3000000", "40000400")
            write_apb_reg("3000004", "2003e700")
        time.sleep(1)
        print "\n Return the system to PLL \n"
        write_apb_reg ("3000008", "00000000")
        time.sleep(1)
        print "\nChange the COM Baudrate to " ,BaudRateCalculation (Integer,Frac,32768000.0)
        SerialConfig_1(COM , BaudRateCalculation (Integer,Frac,32768000.0))
        time.sleep(1)
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
        time.sleep(1)
        # change the PLL  BWAJ
        if chip_type == "D4" :
            write_apb_reg("3000000", "12ed")
        else :
            write_apb_reg("3000000", "40000400")
            write_apb_reg("3000004", "2005db00")
        time.sleep(1)
        print "\n Return the system to PLL \n"
        write_apb_reg ("3000008", "00000000")
        time.sleep(1)
        print "\nChange the COM Baudrate to " ,BaudRateCalculation (Integer,Frac,49152000.0)
        SerialConfig_1(COM , BaudRateCalculation (Integer,Frac,49152000.0))
        time.sleep(1)
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
        time.sleep(1)
        # change the PLL  BWAJ
        if chip_type == "D4" :
            write_apb_reg("3000000", "1464")
            time.sleep(1)
        else:
            write_apb_reg("3000000", "40000400")
            write_apb_reg("3000004", "2008c900")
        print "\n Return the system to PLL \n"
        write_apb_reg ("3000008", "00000000")
        time.sleep(1)
        print "\nChange the COM Baudrate to" , BaudRateCalculation (Integer,Frac,73728000.0)
        SerialConfig_1(COM , BaudRateCalculation (Integer,Frac,73728000.0))
        time.sleep(1)
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
        time.sleep(1)
        # change the PLL  BWAJ
        if chip_type == "D4" :
            write_apb_reg("3000000", "14e6")
            time.sleep(1)
        else :
            write_apb_reg("3000000", "40000400")
            write_apb_reg("3000004", "2009cd00")
        print "\n Return the system to PLL \n"
        write_apb_reg ("3000008", "00000000")
        time.sleep(1)
        print "\nChange the COM Baudrate to " , BaudRateCalculation (Integer,Frac,82247680.0)
        SerialConfig_1(COM , BaudRateCalculation (Integer,Frac,82247680.0))
        time.sleep(1)
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
        time.sleep(1)
        # change the PLL  BWAJ
        if chip_type == "D4" :
            write_apb_reg("3000000", "157b")
            time.sleep(1)
        else :
            write_apb_reg("3000000", "40000400")
            write_apb_reg("3000004", "200af600")   
        print "\n Return the system to PLL \n"
        write_apb_reg ("3000008", "00000000")
        time.sleep(1)
        print "\nChange the COM Baudrate to " , BaudRateCalculation (Integer,Frac,91979776)
        SerialConfig_1(COM , BaudRateCalculation (Integer,Frac,91979776))
        time.sleep(1)
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
        time.sleep(1)
        # change the PLL  BWAJ
        if chip_type == "D4" :
            write_apb_reg("3000000", "15db")
            time.sleep(1)
        else :
            write_apb_reg("3000000", "40000400")
            write_apb_reg("3000004", "200bb700")   
        print "\n Return the system to PLL \n"
        write_apb_reg ("3000008", "00000000")
        time.sleep(1)
        print "\nChange the COM Baudrate to" , BaudRateCalculation (Integer,Frac,98304000.0)
        SerialConfig_1(COM , BaudRateCalculation (Integer,Frac,98304000.0))
        time.sleep(1)
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
 
def All_Memory_Power_Mode (power_mode):  #power_mode can get: atcive ; light_sleep ; deep_sleep ; shut_down
    if (power_mode == "light_sleep" ):
        #need to verify clear bit of the following modes := DEEP SLEEP and SHUT DOWN
        #clear bits of DEEP SLEEP:
        clear_bit (MEM_PWR_MD_DS1,"3ffffff")
        clear_bit (MEM_PWR_MD_DS2,"ffe")

        print"clear the bits of shut_down"
        clear_bit (MEM_PWR_MD_DS1,"3ffffff")
        clear_bit (MEM_PWR_MD_DS1,"ffe")
        if (on_off == 1):
            print" "
            print "\n\n######################\n\nAll the following block enter to light_sleep\n\n######################\n\n"
            set_bit (MEM_PWR_MD_LS2,"1FFF")
            # not include CHACHE 0&1 , DTCM 0,1,2,3
            set_bit (MEM_PWR_MD_LS1,"3FFFC3C")
        else :
            clear_bit (MEM_PWR_MD_LS1,"3FFFFFF")
            clear_bit (MEM_PWR_MD_LS2,"1fff")

        #clear bits of SHUT DOWN:
        clear_bit (MEM_PWR_MD_SD1,"3ffffff")
        clear_bit (MEM_PWR_MD_SD1,"ffe")
        #set the LIGHT SLEEP mode
        set_bit (MEM_PWR_MD_LS2,"1FFF")    # not include CHACHE 0&1 , DTCM 0,1,2,3
        set_bit (MEM_PWR_MD_LS1,"3FFFC3C")
        write_to_log("All memory blocks entered to LIGHT SLEEP mode")

        
    elif (power_mode == "deep_sleep" ):
        #clear the bits of SHUT DOWN:
        clear_bit (MEM_PWR_MD_SD1,"3ffffff")
        clear_bit (MEM_PWR_MD_SD2,"7fe")
        #clear the bits of LIGHT SLEEP:
        clear_bit (MEM_PWR_MD_LS2,"7fe")
        clear_bit (MEM_PWR_MD_LS1,"3ffffff")
        #set the DEEP SLEEP mode
        set_bit (MEM_PWR_MD_DS2,"7fe")
        set_bit (MEM_PWR_MD_DS1,"3FFfc3c")
        write_to_log("All memory blocks entered to DEEP SLEEP mode")

    elif (power_mode == "shut_down" ):
        #clear the bits of LIGHT SLEEP:
        clear_bit (MEM_PWR_MD_LS1,"3ffffff")
        clear_bit (MEM_PWR_MD_LS2,"7fe")
        #clear bits of DEEP SLEEP:
        clear_bit (MEM_PWR_MD_DS1,"3ffffff")
        clear_bit (MEM_PWR_MD_DS2,"ffe")
        #set the SHUT DOWN mode:
        set_bit (MEM_PWR_MD_SD2,"7fe")
        set_bit (MEM_PWR_MD_SD1,"3FFfc3c")
        write_to_log("All memory blocks entered to SHUT DOWN mode")

    elif (power_mode == "active"):
        #clear the bits of LIGHT SLEEP:
        clear_bit (MEM_PWR_MD_LS1,"3ffffff")
        clear_bit (MEM_PWR_MD_LS2,"7fe")
        #clear bits of DEEP SLEEP:
        clear_bit (MEM_PWR_MD_DS1,"3ffffff")
        clear_bit (MEM_PWR_MD_DS2,"ffe")
        #clear the bits of SHUT DOWN:
        clear_bit (MEM_PWR_MD_SD1,"3ffffff")
        clear_bit (MEM_PWR_MD_SD2,"7fe")
        write_to_log("All memory blocks entered to ACTIVE mode")
            
    write_to_log("power mode configure to "+ power_mode )     
###############################################################################################################################
###############################################################################################################################   
def Memory_Block_Select (memory_name , memory_section , mode):
    #All_Memory_Power_Mode_2 ("active")

    list1 = ['PTCM','DTCM','TAG','CACHE','PAHB']
    list2 = ['HWVAD0', 'HWVAD1','PAHB','ROM']
    
    if (mode == "active" ):
        if (memory_name in list1):
            clear_bit (MEM_PWR_MD_LS1,MEM_DICT[memory_name][memory_section])
            clear_bit (MEM_PWR_MD_DS1,MEM_DICT[memory_name][memory_section])
            clear_bit (MEM_PWR_MD_SD1,MEM_DICT[memory_name][memory_section])
        elif (memory_name in list2):
            clear_bit (MEM_PWR_MD_LS2,MEM_DICT[memory_name][memory_section])
            clear_bit (MEM_PWR_MD_DS2,MEM_DICT[memory_name][memory_section])
            clear_bit (MEM_PWR_MD_SD2,MEM_DICT[memory_name][memory_section])
        write_to_log (memory_name+ ' - section '+ memory_section + ', entered to ' + mode + ' mode')
    
    
    elif (mode == "light_sleep" ):
        if (memory_name in list1):
            clear_bit (MEM_PWR_MD_DS1,MEM_DICT[memory_name][int(memory_section)])
            clear_bit (MEM_PWR_MD_SD1,MEM_DICT[memory_name][int(memory_section)])
            set_bit (MEM_PWR_MD_LS1,MEM_DICT[memory_name][int(memory_section)])
        elif (memory_name in list2):
            clear_bit (MEM_PWR_MD_DS2,MEM_DICT[memory_name][int(memory_section)])
            clear_bit (MEM_PWR_MD_SD2,MEM_DICT[memory_name][int(memory_section)])
            set_bit (MEM_PWR_MD_LS2,MEM_DICT[memory_name][int(memory_section)])
        write_to_log (memory_name+ ' - section '+ memory_section + ', entered to ' + mode + ' mode')

    elif (mode == "deep_sleep" ):
        if (memory_name in list1):
            if ( (memory_name == 'DTCM') and (memory_section <= 3) ):
                write_to_log('Secions 0-3 of DTCM cannot enter DEEP SLEEP mode')
            elif ( (memory_name == 'CACHE') and (memory_section <= 1) ):
                write_to_log('Secions 0-1 of CACHE cannot enter DEEP SLEEP mode')
            else:
                clear_bit (MEM_PWR_MD_SD1,MEM_DICT[memory_name][int(memory_section)])
                set_bit (MEM_PWR_MD_DS1,MEM_DICT[memory_name][int(memory_section)])
                write_to_log (memory_name+ ' - section '+ memory_section + ', entered to ' + mode + ' mode')
        elif (memory_name in list2):
            if ((memory_name == 'HWVAD0') or (memory_name == 'HWVAD1') ):
                write_to_log('HWVAD0 and HWVAD1 cannot enter DEEP SLEEP mode')
            else:
                clear_bit (MEM_PWR_MD_SD2,MEM_DICT[memory_name][int(memory_section)])
                set_bit (MEM_PWR_MD_DS2,MEM_DICT[memory_name][int(memory_section)])
                write_to_log (memory_name+ ' - section '+ memory_section + ', entered to ' + mode + ' mode')

    elif (mode == "shut_down" ):
        if (memory_name in list1):
            if ( (memory_name == 'DTCM') and (memory_section <= 3) ):
                write_to_log('Secions 0-3 of DTCM cannot enter SHUT DOWN mode')
            elif ( (memory_name == 'CACHE') and (memory_section <= 1) ):
                write_to_log('Secions 0-1 of CACHE cannot enter SHUT DOWN mode')
            else:
                set_bit (MEM_PWR_MD_SD1,MEM_DICT[memory_name][int(memory_section)])
                write_to_log (memory_name+ ' - section '+ memory_section + ', entered to ' + mode + ' mode')
        elif (memory_name in list2):
            if ((memory_name == 'HWVAD0') or (memory_name == 'HWVAD1') ):
                write_to_log('HWVAD0 and HWVAD1 cannot enter SHUT DOWN mode')
            else:
                set_bit (MEM_PWR_MD_SD2,MEM_DICT[memory_name][int(memory_section)])
                write_to_log (memory_name+ ' - section '+ memory_section + ', entered to ' + mode + ' mode')
                
def BaudRateCalculation(Integer,Frac ,APB_Clock):
    
    buad_rate = (1.0/16.0*(APB_Clock/(Integer+Frac/16)))
    return int (buad_rate)

def exeBootFile():
    ser.write(chr(0x5A))
    ser.write(chr(0x0B))
    time.sleep(0.5)
    ser.write("19r")
    time.sleep(0.5)
    version = ser.read(5)
    write_to_log("Chip Type = " + str(version)[:4])
    # time.sleep(0.1)
    #write_to_log("\n")
    if (version[:3] == 'dbd'):
        Boot_Complete=1
        write_to_log("Boot Succeeded\n")
    else:
        write_to_log("Boot Failed\n")
 
def load_file(file_name, unsent_bytes):
    infile = open(file_name,"rb")
    bytes_to_send = infile.read()
    wakeup()
    if (unsent_bytes == 0):
        ser.write(str(bytes_to_send)) 
    else:
        ser.write((str(bytes_to_send))[:-unsent_bytes]) 
    time.sleep(1)
    ser.flushInput()
    
    #write_to_log("File load successful")

def load_boot_file(file_name):
    write_to_log('Baud Rate: '+str(BAUD_RATE))
    load_file(file_name, 0)
    exeBootFile()
    

def FW_init(): #loading a specific acoustic model- analog mic, VT interupt on GPIO14
    write_to_log("FW acoustic model configuration started")
    FW_read_register ("0")
    FW_write_register_short("29","0001") #close all interfaces except UART
    FW_write_register_short("22","1220") #configure HW VAD, LDO at 0.9v 11v-->0.9v, OSC
    FW_write_register_short("23","6022") #Configure MIPS to be: 12MHz
    # time.sleep (1)
    FW_write_register_short("10","6000") #AHB = APB = 12MHz  
    #FW_write_register_short("10","6015") #AHB = 2MHz, APB = 1MHZ
    # time.sleep (1)
    FW_write_register_short("15","8e8e") #Configure interrupt GPIO 14
    #FW_write_register_short("24","f043") #Configure digital microphone 1MHz 
    FW_write_register_short("24","0028")
    pre_load_trigger_model("C:\DBMD6-github\Tests\Bar\HBG_v332.bin") #Pre-Load acoustic model
    load_model ("C:\DBMD6-github\Tests\Bar\HBG_v332.bin",'0') #Load acoustic model
    FW_write_register_short("17","8") #Disable audio buffering
    FW_write_register_short("01","0001") #Enter 
    write_to_log("\n")
    write_to_log("Configuration ended\n")

def FW_init_strap10(): #loading a specific acoustic model- analog mic, VT interupt on GPIO14
    write_to_log("FW acoustic model configuration started")
    FW_read_register ("0")
    FW_write_register_short("29","0001") #close all interfaces except UART
    FW_write_register_short("22","1220") #configure HW VAD, LDO at 0.9v 11v-->0.9v, OSC
    FW_write_register_short("23","0022") #Configure MIPS to be: 12MHz    #for bypass mode: '0022'
    # time.sleep (1)
    FW_write_register_short("10","6015") #6015 for: AHB = 2MHz, APB = 1MHZ     #6005 for: AHB = 2MHz, APB = 2MHZ 
    # time.sleep (1)
    FW_write_register_short("15","8e8e") #Configure interrupt GPIO 14
    #FW_write_register_short("24","f043") #Configure digital microphone 1MHz 
    FW_write_register_short("24","0028")
    pre_load_trigger_model("C:\DBMD6-github\Tests\Bar\HBG_v332.bin") #Pre-Load acoustic model
    load_model ("C:\DBMD6-github\Tests\Bar\HBG_v332.bin",'0') #Load acoustic model
    FW_write_register_short("17","8") #Disable audio buffering
    FW_write_register_short("01","0001") #Enter 
    write_to_log("\n")
    write_to_log("Configuration ended\n")

def FW_write_register(reg_num, value):
	global write_in_progress
	ser.flushInput()
	while (1):
		if (write_in_progress == False):
			write_in_progress = True
			wakeup()
			value = str(value)
			if (value in LIST_OF_VALUES):
				value = LIST_OF_VALUES[value]
			value = value.zfill(4)
			reg_num = str(reg_num)
			reg_num = reg_num.zfill(3)
			
			ser.write(reg_num + "w" + value)
			time.sleep (0.01)
			FW_read_register(reg_num)

			write_in_progress = False
			break
		else:
			print "writing in use... please wait..."
			time.sleep(0.01)


#short- without reading the register after writing		
def FW_write_register_short(reg_num, value):
    global write_in_progress	
    ser.flushInput()
    while (1):
        if (write_in_progress == False):
            write_in_progress = True
            wakeup()
            value = str(value)
            if (value in LIST_OF_VALUES):
                value = LIST_OF_VALUES[value]
            value = value.zfill(4)
            reg_num = str(reg_num)
            reg_num = reg_num.zfill(3)
            ser.write(reg_num + "w" + value)
            write_in_progress = False
            time.sleep (0.5)
            #FW_read_register(reg_num)
            break
        else:
            print "writing in use... please wait..."
            time.sleep(0.01)

def FW_read_register(register_num):
	global read_in_progress	
	ser.flushInput()
	while (1):
		if (read_in_progress == False):
			read_in_progress = True
			wakeup()
			register_num = str(register_num)
			register_num = register_num.zfill(3)
			ser.write(register_num + "r")
			serRead = ser.read(5)[:4]
			write_to_log("reg: 0x" + register_num + " ; value: 0x" + str(serRead))
			read_in_progress = False
			break
		else:
			print "writing in use... please wait..."
			time.sleep(0.01)
		
def FW_read_register_return_value(register_num):
    global read_in_progress	
    ser.flushInput()
    while (1):
        if (read_in_progress == False):
            read_in_progress = True
            wakeup()
            register_num = str(register_num)
            register_num = register_num.zfill(3)
            ser.write(register_num + "r")
            serRead = ser.read(5)[:4]
            read_in_progress = False
            write_to_log("reg: 0x" + register_num + " ; value: 0x" + str(serRead))
            return serRead
        else:
            print "writing in use... please wait..."		
            time.sleep(0.01)			

def FW_read_register_loop(register_num):
	i=0
	print("reading register 0x" + str(register_num))
	while (i<100):
		read_register(register_num)
		time.sleep(0.1)
		i=i+1
	print("done loop reading") 

def FW_read_IO_port (reg_address):
    global read_in_progress	
    ser.flushInput()
    while (1):
        if (read_in_progress == False):
            read_in_progress = True
            reg_address = (str(reg_address)).zfill(8)		
            address_msb = reg_address [:4]
            address_lsb = reg_address [4:8]
            wakeup()
            ser.write("006w" + address_msb)
            time.sleep (0.001)
            ser.write("005w" + address_lsb)
            time.sleep (0.001)
            ser.write("007r")
            value_lsb = ser.read(5)[:4]
            ser.write("008r")
            value_msb = ser.read(5)[:4]
            write_to_log("reg: 0x" + reg_address + " ; value: 0x" + str(value_msb)+str(value_lsb))
            read_in_progress = False
            #break
            return str(value_msb)+str(value_lsb)
        else:
            print("reading in use... please wait...")			
            time.sleep(0.01)

def FW_write_IO_port (reg_address, reg_value):
	global write_in_progress	
	ser.flushInput()
	while (1):
		if (write_in_progress == False):
			write_in_progress = True
			reg_address = (str(reg_address)).zfill(8)		
			address_msb = reg_address [:4]
			address_lsb = reg_address [4:8]
			reg_value = (str(reg_value)).zfill(8)		
			value_msb = reg_value [:4]
			value_lsb = reg_value [4:8]
			wakeup()
			ser.write("006w" + address_msb)
			time.sleep (0.001)
			ser.write("005w" + address_lsb)
			time.sleep (0.001)
			ser.write("007w" + value_lsb)
			time.sleep (0.001)
			ser.write("008w" + value_msb)
			
			FW_read_IO_port (reg_address)
			write_in_progress = False
			break
		else:
			print("writing in use... please wait...")			
			time.sleep(0.01)

def pre_load_trigger_model(trigger_model):
	if os.path.isfile(trigger_model):
		FW_write_register(2, str(hex((os.path.getsize(trigger_model))/16+3).rstrip("L")[2:]))
	else:
		write_to_log("Acoustic model not found: " + trigger_model)

def load_model(model_filename, mode):
    if os.path.isfile(model_filename):
        FW_write_register_short ("f", mode)
        time.sleep(0.1)	
        wakeup()	
        load_file(model_filename,0)
    
        # # Checksum test
        # calculated_checksum = checkSum()
        # checksum_from_fw = read_checksum_from_fw()
        # write_to_log("The checksum for Acoustic model is: " + str(checksum_from_fw))
        # 
        # if (calculated_checksum == checksum_from_fw):
        # 	write_to_log ("Acoutic Model: Checksum test - Pass")
        # else:
        # 	write_to_log ("Acoutic Model: Checksum test - Fail")
        # 	sys.exit()
        
        #ser.write(chr(0x5A))
        #ser.write(chr(0x0B))
        
        
        # for trigger model only!
        mode = int(mode)
        if (mode == 0):
            time.sleep(0.05)
            reg_value=FW_read_register_return_value("41")
            if (reg_value == '0001'):
                write_to_log("Acoustic model loaded: " + model_filename)
                return
            else:
                write_to_log("Trigger acoustic model failed to load")
                return
    
    else:
        write_to_log("Acoustic model not found: " + model_filename)

        
def read_checksum_from_fw_file(file_name):
	infile = open(file_name, "rb")
	list_file = list(infile.read())
	j=len(list_file) - 4
	checksum_data = []
	for i in xrange(0, 4):
		checksum_data.append(str(hex(ord(list_file[j+i]))))
	return checksum_data

def wakeup():
    if ( (chip_type=="D4") or (chip_type=="D6") ):
        ser.write(chr(0x00))
        time.sleep(0.05)
        ser.write(chr(0x00))
        time.sleep(0.05)
        ser.write(chr(0x00))
        ser.flushInput()
        time.sleep(0.3)
    else:
        GPIO.output(WAKEUP_GPIO,True)
        time.sleep(0.1)
        

def playAudioFile(audio_file_name):
    winsound.PlaySound(audio_file_name, winsound.SND_FILENAME)
    write_to_log("playing audio file: "+audio_file_name)
    
    