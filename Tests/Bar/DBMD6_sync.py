execfile ("C:\DBMD6-github\init.py")
def main():  #args need to be: COM TEST_NUMBER STRAP VOLTAGE TEMP   
    COM = sys.argv[1]
    #config the UART
    SerialConfig_1 (COM ,BAUD_RATE)
    #open a new log file
    Open_log(Log_Name)

    write_to_log('========================')
    write_to_log('Test Number: '+ str(sys.argv[2]) +' ; Strap Mode: '+str(sys.argv[3]) + ' ; Voltage: ' + str(sys.argv[4]) + ' ; Temp: '+ str(sys.argv[5]))

    #sync with the DBMD6 
    Sync()
    #load_boot_file ('C:\DBMD6-github\VT_D6_ver_293_Sen333.bin')
    #FW_init()
    
main()