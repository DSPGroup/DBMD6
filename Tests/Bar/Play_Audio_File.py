execfile ("C:\DBMD6-github\init.py")

def main():
    COM = sys.argv[1]
    #config the UART
    SerialConfig_1 (COM ,BAUD_RATE)    
    #open a new log file
    #Open_log(Log_Name)
    Open_log(Character1 + sys.argv[2])
    
    #configure gpio5 to get interupts from gpio14 that it is connected to
    FW_write_IO_port ('300004C', 'C00')      #set into gpio mode
    FW_write_IO_port ('4000014', '20')       #direction-input
    FW_write_IO_port ('40002A0', '000C')     #configure interrupt- edge, high
    
    #read gpio5's interupt, to make sure its clear before the voice triggering
    interupt1=FW_read_IO_port('40002A8')
    interupt1=int(interupt1,16)&2

    #play 'Hello Blue Genie'
    playAudioFile('C:\DBMD6-github\Tests\Bar\HBG1.wav')
    time.sleep(3)
    
    #check gpio5's interupt register
    interupt2=FW_read_IO_port('40002A8')
    interupt2=int(interupt2,16)&2
    if ((interupt2 == 2) and (interupt1 == 0)):
        write_to_log('Pass')
    FW_write_IO_port ('40002AC', '2')
main()