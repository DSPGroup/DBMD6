##########################
#Script identification Function Script
##########################
#Author : Eran Simoni
#Start Date : 8-3-2016
#Script change By : xxxx

########################################################################################################################
##Hello

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
    print 'ser = \n\n', ser
print '##################################'
print 'Function  SerialConfig_1 load !!'
print '##################################'

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
    print 'ser_2 = \n\n', ser_2

print ''
print 'Function  SerialConfig_2 load !!'
print '##################################'
    
    
####################################################################################################################################
#SYNC withloaded
def Sync (): 
    D4_received_word = ''
    timeout_start = time.time()
    timeout = 10
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
        print "#################################"
        #log.write("No Sync\n")
    time.sleep(0.5)
    
    # Check Checksum
    ser.write(chr(0x5A))
    ser.write(chr(0x0E))
    ## FW send echo + Checksum(4 bytes)
    ser.flushInput()
    ReadSerial = ser.read(8)
    time.sleep(0.1)
print ''
print 'Function  Sync load !!'
print ''

####################################################################################################################################
#read APB Address
#################################

def read_apb_reg(addr):
    global apb_reg
    if len(addr)<8:
        addr = addr.zfill(8)
        
    addr6="0x"+addr[6]+addr[7]
    addr4="0x"+addr[4]+addr[5]
    addr2="0x"+addr[2]+addr[3]
    addr0="0x"+addr[0]+addr[1]
    #print addr6
    #print addr4
    #print addr2
    #print addr0
    asciiaddr6=binascii.unhexlify(addr[6]+addr[7])
    asciiaddr4=binascii.unhexlify(addr[4]+addr[5])
    asciiaddr2=binascii.unhexlify(addr[2]+addr[3])
    asciiaddr0=binascii.unhexlify(addr[0]+addr[1])
    
    ser.write(chr(0x5A)+chr(0x07)+asciiaddr6+asciiaddr4+asciiaddr2+asciiaddr0)
    time.sleep(0.2)
    
    reg=ser.read(6)
    apb_reg =binascii.hexlify(reg[5])+binascii.hexlify(reg[4])+binascii.hexlify(reg[3])+binascii.hexlify(reg[2])
    print '#################################'
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

    if len(value)<8:
        value = value.zfill(8)
    if len(addr)<8:
        addr = addr.zfill(8)

    value6="0x"+value[6]+value[7]
    value4="0x"+value[4]+value[5]
    value2="0x"+value[2]+value[3]
    value0="0x"+value[0]+value[1]
    #print value6
    #print value4
    #print value2
    #print value0
    asciivalue6=binascii.unhexlify(value[6]+value[7])
    asciivalue4=binascii.unhexlify(value[4]+value[5])
    asciivalue2=binascii.unhexlify(value[2]+value[3])
    asciivalue0=binascii.unhexlify(value[0]+value[1])
    
    addr6="0x"+addr[6]+addr[7]
    addr4="0x"+addr[4]+addr[5]
    addr2="0x"+addr[2]+addr[3]
    addr0="0x"+addr[0]+addr[1]
    #print addr6
    #print addr4
    #print addr2
    #print addr0
    asciiaddr6=binascii.unhexlify(addr[6]+addr[7])
    asciiaddr4=binascii.unhexlify(addr[4]+addr[5])
    asciiaddr2=binascii.unhexlify(addr[2]+addr[3])
    asciiaddr0=binascii.unhexlify(addr[0]+addr[1])
    time.sleep(0.2)
    ser.write(chr(0x5A)+chr(0x04)+asciiaddr6+asciiaddr4+asciiaddr2+asciiaddr0+asciivalue6+asciivalue4+asciivalue2+asciivalue0)
    
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
# createe a new dir 
#################################
def Make_Dir(Dir_Name):
    
    if not os.path.exists(Dir_Name):
        os.makedirs(Dir_Name)


def Open_log(Log_Name):
    Make_Dir(Dir_Name) # call to the make dir funcation
    
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

#Tzvika







