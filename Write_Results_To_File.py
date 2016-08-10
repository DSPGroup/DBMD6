execfile ("C:\DBMD6-github\init.py")
def main():
    COM = sys.argv[1]
    #config the UART
    SerialConfig_1 (COM ,BAUD_RATE)
    #open a new log file
    Open_log(Character1 + sys.argv[3])
    
    write_to_log('Max voltage measured: '+ str(sys.argv[2]))
    write_to_log("\n")
    if (float(sys.argv[2]) > 1.5):
        write_to_log('VT status: PASS\n') 
    else:
        write_to_log('VT status: FAIL\n')
main()