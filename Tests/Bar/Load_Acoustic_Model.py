execfile ("C:\DBMD6-github\init.py")

def main():
    COM = sys.argv[1]
    #config the UART
    SerialConfig_1 (COM ,BAUD_RATE)
    
    #open a new log file
    Open_log(Character1 + sys.argv[2])
    #Open_log(Log_Name)
    
    #config and load acoustic model
    FW_init()
    #FW_init_strap10()
main()