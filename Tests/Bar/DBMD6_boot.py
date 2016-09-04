execfile ("C:\DBMD6-github\init.py")
def main():
    COM = sys.argv[1]
    #config the UART
    SerialConfig_1 (COM ,BAUD_RATE)
    
    #open a new log file
    Open_log(Character1 + sys.argv[2])
    #Open_log(Log_Name)
    
    #load the boot file
    load_boot_file ('C:\DBMD6-github\Tests\Bar\VT_D6_ver_293_Sen333.bin')
    
    
    #FW_write_register_short("24","f048") #Configure digital microphone 1MHz  //f043
    # ('4000008')
    #FW_write_IO_port ('3000020', reg_value)
main()