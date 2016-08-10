#!/usr/bin/env python

# version 13-07-2016

import os.path
import sys
import time
import RPi.GPIO as GPIO
from smbus import SMBus
from subprocess import call
import serial
import datetime
from Parameters import *
import wave
import thread
import subprocess
import shlex
import gc


##########################################
##		Set Raspberry PI GPIO			##
##########################################
GPIO.setwarnings(False)
GPIO.setmode (GPIO.BCM)

if (CHIP_TYPE=="D2"):
	WAKEUP_GPIO = 24
 
RESET_GPIO = 17
INTERRUPT_TRIGGER_GPIO = 23
if (EVB_TYPE=="EVB_S"):
	LED_GPIO = 24
	FIRMWARE_LOADED_LED_GPIO = 20
elif (EVB_TYPE=="EVB_L"):
	LED_GPIO = 22

# Configure the state of the GPIO pins	
GPIO.setup(RESET_GPIO, GPIO.OUT)
GPIO.setup(LED_GPIO, GPIO.OUT)
GPIO.setup(INTERRUPT_TRIGGER_GPIO, GPIO.IN)

if (CHIP_TYPE=="D2"):
	GPIO.setup(WAKEUP_GPIO, GPIO.OUT)

if (EVB_TYPE=="EVB_S"):
	GPIO.setup(FIRMWARE_LOADED_LED_GPIO, GPIO.OUT)

# Global variables
read_in_progress = False
write_in_progress = False
stop_streaming_flag = False
statistic = True
mic24 = '0000'
mic25 = '0000'
log_filename = ''
LIST_OF_VALUES = {}

i2c = SMBus(1)
cpld_i2c_addr = 0x33

if ( (CHIP_TYPE=="D4") or (CHIP_TYPE=="D6") ):
	ser = serial.Serial(
		port='/dev/ttyAMA0',
		baudrate=460800,
		#baudrate=2000000,
		parity=serial.PARITY_NONE,
		stopbits=serial.STOPBITS_ONE,
		bytesize=serial.EIGHTBITS,
		timeout=0.01 
		)
else:
	ser = serial.Serial(
		port='/dev/ttyAMA0',
		baudrate=230400, 
		parity=serial.PARITY_EVEN,
		stopbits=serial.STOPBITS_TWO,
		bytesize=serial.EIGHTBITS,
		timeout=0.01
		)

##########################################
##			List of Functions			##
##########################################

# Log functions
def create_log_filename():
	global log_filename
	log_filename = "VT_UART_"+datetime.datetime.today().strftime('%d_%m_%Y__%H_%M_%S_%f')+'.txt'
	if not os.path.isdir ("/home/pi/Projects/Log") :
		os.makedirs ("/home/pi/Projects/Log")
		shell_command("sudo chown pi:pi /home/pi/Projects/Log")
		
	
def write_to_file(time, user_input):
	log_file = open('/home/pi/Projects/Log/'+log_filename, "a")
	log_file.write("%s\t" %time)
	log_file.write("%s\n" %user_input)
	log_file.close()

def write_to_log(user_input):
	time = datetime.datetime.today().strftime('%d/%m/%Y %H:%M:%S:%f')
	print time,'\t',user_input
	write_to_file(time, user_input)

def set_date_time(user_command):
	arr = user_command.split('_')
	arr= filter(None,arr)		# remove empty cells from array	
	for i in range (0,len(arr)):
		arr[i] = int(arr[i])

	current_date_time = datetime.datetime.today()
	new_date = current_date_time.replace(arr[2],arr[1],arr[0],arr[3],arr[4],arr[5],arr[6])
	new_date = new_date+ datetime.timedelta(seconds=1)
		
	subprocess.call (['sudo', 'date', '-s',new_date.ctime()])
	time.sleep(0.1)

	
# Statistics functions	
def enable_statistic():
	global statistic
	statistic = True
	write_to_log("Statistics enabled")

def disable_statistic():
	global statistic
	statistic = False
	write_to_log("Statistics disabled")


# Global functions	
def blink_LED(times, end):
	count = 0
	while count < times:
		GPIO.output(LED_GPIO,True)
		time.sleep(0.1)
		GPIO.output(LED_GPIO,False)
		time.sleep(0.1)
		count = count + 1
	if end == 1:
		GPIO.output(LED_GPIO,True)
	else:
		GPIO.output(LED_GPIO,False)

def shell_command(user_command):
	try:
		write_to_log ('About to run shell command: "' + user_command + '"')
		subprocess.Popen(shlex.split(user_command)).wait()
	except:
		write_to_log ('command "' + user_command + '" not found')

def create_acoustic_model():
	shell_command("python A-Model_Generation.py")
	write_to_log ("A new acoustic model \"A-Model.bin\" was generated. Type 'plt A-Model.bin' followed by 'lt A-Model.bin'  to load it")

def import_values_from_file(values_filename):
	# check if file exist
	if (os.path.isfile(values_filename) == False):
		write_to_log ("File "+ values_filename + " not exist !")
		return
	global LIST_OF_VALUES
	with open(values_filename) as f:
		for line in f:
			if line.strip() == '': # check if the line is empty
				continue
			line = line.rstrip('\n') # remove '\n'
			line = line.replace(' ', '') # remove blanks
			(key, val) = line.split('=')
			LIST_OF_VALUES[key] = val	
	write_to_log ("Loaded values from file " + values_filename + " successfully")

def show_values():
	write_to_log("{:<15} {:<12}".format('Register', 'Value'))
	for item in LIST_OF_VALUES.iteritems():
		reg, val = item
		write_to_log("{:<15} {:<12}".format(reg, val)) 

def get_value_from_bytes(list, start_location, number_of_bytes):
    string = ''
    counter=number_of_bytes-1
    while (counter >= 0):
        string += str(hex(ord(list[start_location+counter])))[2:].zfill(2)
        counter-=1
    return int(string, 16)
	
def calc_checksum(file_name, unsent_bytes):
	#open and read the file
	infile = open(file_name,"rb")
	list_file = list(infile.read())

	i=0
	sum_value=0
	while(i < len(list_file) - unsent_bytes) :
		current_byte = hex(ord(list_file[i]))
		next_byte = hex(ord(list_file[i+1]))

		if ((current_byte == '0x5a') and ((next_byte == '0x2') or (next_byte == '0x1'))):
			# header field
			for j in xrange(0, 2):
				header = ord(list_file[i+j])
				sum_value+=header
			i+=2

			# number of words field
			num_of_words = get_value_from_bytes(list_file, i, 4)
			sum_value += num_of_words
			i+=4

			# address field
			address = get_value_from_bytes(list_file, i, 4)
			sum_value += address
			i+=4

			# data words
			while (j < num_of_words*2):
				data = get_value_from_bytes(list_file, i, 2)
				sum_value += data
				j+=2
				i+=2
        
		else:
			break
    
	# add the checksum value to the total sum : 0x5A + 0x0E = 0x68 = 104
	sum_value += 104
	sum_value = str(hex(sum_value))[2:].zfill(8)
	
	sum_value_list = []
	j=8
	while (j>0):
		string = hex(int(sum_value [j-2:j] ,16))
		sum_value_list.append(string)
		j-=2

	return sum_value_list

		
# Load model\FW file
def load_file(file_name, unsent_bytes):
	infile = open(file_name, "rb")
	list_file = list(infile.read())
	
	i=0
	while (i < (len(list_file) - unsent_bytes)):
		current_byte = hex(ord(list_file[i]))
		next_byte = hex(ord(list_file[i+1]))
		
		if ((current_byte == '0x5a') and ((next_byte == '0x2') or (next_byte == '0x1'))):
			#send the header to the FW
			j=0
			while(j < 10) :
				ser.write(list_file[i+j])
				j += 1
			time.sleep(0.0001)
			
			i+=2
			# number of words field
			num_of_words = get_value_from_bytes(list_file, i, 4)
			num_of_bytes = 2*num_of_words
			i+=8
			
			j=0
			while (j < num_of_bytes):
				ser.write(list_file[i+j])
				j+=1			
			i+=num_of_bytes
		
		else:
			print "NOT HEADER !!!"
			return


def read_checksum_from_fw_file(file_name):
	infile = open(file_name, "rb")
	list_file = list(infile.read())
	j=len(list_file) - 4
	checksum_data = []
	for i in xrange(0, 4):
		checksum_data.append(str(hex(ord(list_file[j+i]))))
	return checksum_data
			
		
def load_model(model_filename, mode):
	if os.path.isfile(model_filename):
		write_register_short ("f", mode)
		time.sleep(0.1)	
		wakeup()	
		load_file(model_filename, 2)
	
		# Checksum test
		calculated_checksum = calc_checksum(model_filename, 2)
		checksum_from_fw = read_checksum_from_fw()
		write_to_log("The checksum for Acoustic model is: " + str(checksum_from_fw))
		
		if (calculated_checksum == checksum_from_fw):
			write_to_log ("Acoutic Model: Checksum test - Pass")
		else:
			write_to_log ("Acoutic Model: Checksum test - Fail")
			sys.exit()
		
		ser.write(chr(0x5A))
		ser.write(chr(0x0B))
		
		
		# for trigger model only!
		mode= int(mode)		
		if (mode == 0):
			time.sleep(0.05)
			reg_value = read_register_short("41")
			if (int(reg_value) == 1):
				write_to_log("Acoustic model loaded: " + model_filename)
				return
			else:
				write_to_log("Trigger acoustic model failed to load")
				return
		
		write_to_log("Acoustic model loaded: " + model_filename)
	else:
		write_to_log("Acoustic model not found: " + model_filename)


def pre_load_trigger_model(trigger_model):
	if os.path.isfile(trigger_model):
		write_register(2, str(hex((os.path.getsize(trigger_model))/16+3).rstrip("L")[2:]))
	else:
		write_to_log("Acoustic model not found: " + trigger_model)

def pre_load_command_model(command_model):
	if os.path.isfile(command_model):
		write_register(3, str(hex((os.path.getsize(command_model))/16+3).rstrip("L")[2:]))
	else:
		write_to_log("Acoustic model not found: " + command_model)

def load_fw(fw_filename):
	write_to_log("Booting Starts ...")
	Boot_Complete=0

	while (Boot_Complete == 0):
		ser.flushInput()
		received_word = ''
		timeout_start = time.time()
		timeout = 10
		while ((received_word != "OK") and (time.time() < (timeout_start + timeout))):
			if ( (CHIP_TYPE=="D4") or (CHIP_TYPE=="D6") ):
				ser.write(chr(0x0)+chr(0x0)+ chr(0x0)+ chr(0x0)+chr(0x0)+chr(0x0)+ chr(0x0)+ chr(0x0)+chr(0x0)+chr(0x0)+ chr(0x0)+ chr(0x0)+chr(0x0)+chr(0x0)+ chr(0x0)+ chr(0x0)) 
			else:
				ser.write("Ac")
			received_word = ser.read(2)

		if received_word == "OK":
			write_to_log("Got Sync")
		else:
			write_to_log("No Sync")
			sys.exit()
		
		# Download the FW file to the chip
		time.sleep(0.1)
		infile = open(fw_filename, "rb")
		list_file = list(infile.read())
		j=0
		while(j < len(list_file) - 4) :
			ser.write(str(list_file[j]))
			j = j + 1
		
		# Checksum test
		calculated_checksum = calc_checksum(fw_filename, 4)
		checksum_from_file = read_checksum_from_fw_file(fw_filename)
		checksum_from_fw = read_checksum_from_fw()
		write_to_log("The checksum for FirmWare is: " + str(checksum_from_fw))

		if ((checksum_from_file == checksum_from_fw) and (checksum_from_fw == calculated_checksum)):
			write_to_log ("FW: Checksum test - Pass")
		else:
			write_to_log ("FW: Checksum test - Fail")
			sys.exit()

		time.sleep(0.1)
		ser.write(chr(0x5A))
		ser.write(chr(0x0B))
		time.sleep(1)

		if (CHIP_TYPE=="D2"):
			change_interface_speed("1000000")
		
		# verify boot succeeded
		ser.flushInput()
		wakeup()
		ser.write("019r")	
		version = ser.read(5)
		write_to_log ("Chip Type = " + str(version)[:4])
		time.sleep(0.1)
		if (version[:3] == 'dbd'):
			Boot_Complete=1
			write_to_log("Boot Succeeded")
			if (EVB_TYPE=="EVB_S"):
				GPIO.output(FIRMWARE_LOADED_LED_GPIO,True)		
		else:
			write_to_log("Boot Failed")
	
		
def load_trigger_model(trigger_model):
	load_model(trigger_model, "0")
		
def load_command_model(command_model):
	load_model(command_model, "1")
		
def load_google_model(google_model):
	load_model(google_model, "4")
	
def load_asrp_param(asrp_param):
	load_model(asrp_param, "4")


# Change interface speed		
def change_interface_speed(interface_speed):
	#if (int(interface_speed) > 3000000):
	#	interface_speed = 3000000

	write_register_short("0c",str(hex(int(interface_speed)/100))[2:])

	ser = serial.Serial(
		port='/dev/ttyAMA0',
		baudrate=int(interface_speed),
		parity=serial.PARITY_NONE,
		stopbits=serial.STOPBITS_ONE,
		bytesize=serial.EIGHTBITS,
		timeout=0.01	
	)
	ser.flushInput()
	write_to_log("Changed interface speed to " + str(interface_speed))
	

# Buffer functions
def dump_buffer (time_in_sec, sample_rate, number_of_channels, file_name="audio_file.raw"):
	global stop_streaming_flag
	stop_streaming_flag = False
	write_to_log("Start dumping")
	wanted_fifo_size = 16*(int(time_in_sec))*(int(sample_rate))*(int(number_of_channels))/8 	# size in Bytes
	current_fifo_size= 0		# size in Bytes
	max_bytes_to_read_from_buffer = 2304 		# 0x900 = 2304
	audio_file = open (file_name, "wb") 
	
	wakeup()
	while(current_fifo_size < wanted_fifo_size):
		if (stop_streaming_flag == True): 
			write_to_log("User has requested to interrupt the streaming")
			break

		try:			
			ser.write("0ar")
			time.sleep (0.01)
			fw_buffer_size = ser.read(5)[:4]
			fw_buffer_size_int = int(fw_buffer_size,16)
			fw_buffer_size_bytes = 16*fw_buffer_size_int
		
		except Exception, e:
			write_to_log ("Error while reading data: " + str(e))
			ser.flushInput()
			continue	

		if (fw_buffer_size_int < max_bytes_to_read_from_buffer) :
			ser.write("20w"+fw_buffer_size)
			data = ser.read(fw_buffer_size_bytes) 
			audio_file.write(data)
			current_fifo_size += fw_buffer_size_bytes
			
			data_len = len(data)
			if (data_len != fw_buffer_size_bytes):
				write_to_log ("Error ! missing " + str (fw_buffer_size_bytes - data_len) + " bytes")
			
		else:
			ser.write("20w"+(str(hex(max_bytes_to_read_from_buffer)[2:].zfill(4))))
			data = ser.read(16*max_bytes_to_read_from_buffer)	
			audio_file.write(data)
			current_fifo_size += 16*max_bytes_to_read_from_buffer
			
			data_len = len(data)
			if (data_len != 16*max_bytes_to_read_from_buffer):
				write_to_log ("Error ! missing " + str (16*max_bytes_to_read_from_buffer - data_len) + " bytes")
			

	audio_file.close()
	write_to_log("Dumping Finished")
	
def stop_streaming():
	global stop_streaming_flag
	stop_streaming_flag = True
	write_to_log("Stop streaming")

def stream (time_in_sec, sample_rate, channels):
	write_register_short("1", "3")
	dump_buffer(time_in_sec, sample_rate, channels)

# Audio functions
def convert_to_wav(source_file_name, sample_rate, number_of_channels, output_file_name="audio_file.wav"):
	if not (os.path.isfile(source_file_name)):
		write_to_log("File " + source_file_name + " not exist")
		return
	pcmfile = open (source_file_name ,'rb')
	pcmdata = pcmfile.read()
	wavfile = wave.open(output_file_name ,'wb')
	sample_rate = int(sample_rate)
	number_of_channels = int(number_of_channels)
	wavfile.setparams((number_of_channels,2,sample_rate,0,'NONE','NONE'))
	wavfile.writeframes(pcmdata)
	wavfile.close()
	write_to_log("Done convert to wav")

def play_audio (cardID, wave_filename, volume):
	if (os.path.isfile(wave_filename)):
		write_to_log ("Playing " + wave_filename)	
		if (cardID == "0"):
			shell_command ("amixer -q sset PCM,0 " + str(volume) + "%") # set the volume
			shell_command ("aplay -q -D hw:0,0 " + str(wave_filename)) # play the audio file
		else:
			shell_command ("amixer -q sset -c 1 'Master' " + str(volume))
			shell_command ("aplay -D " + str(cardID) + " " + str(wave_filename)) # play the audio file
	else:
		write_to_log ("File " + wave_filename + " not found")
	
def stop_audio ():
	write_to_log ("Stopping playback")
	shell_command ("sudo pkill -f aplay")
	

# Hibernate functions	
def enter_hibernate():
	save_mic_settings()
	write_register_short("25","0")
	write_register_short("24","0")
		
	wakeup()
	ser.write("01w0006")
	write_to_log("entering hibernate mode.... bye....")
	
def exit_hibernate():
	wakeup()	# there is already wakeup function in write_register_short function
	config_mic()
	write_to_log("exiting hibernate mode.... bye....")
	
def save_mic_settings():
	global mic24
	global mic25
	value_24 = read_register_short("24")
	
	if(value_24 == "0000"):
		write_to_log("The value of reg 0x24 is '0x0000'")
	else:
		mic24 = value_24
		write_to_log("reg 0x24  value is = 0x" + mic24)
				
		mic25 = read_register_short("25")
		write_to_log("reg 0x25  value is = 0x" + mic25)		
		write_to_log("MIC settings saved")

def config_mic():
	global mic24
	global mic25
	write_register_short("24",mic24)
	write_register_short("25",mic25)
	write_to_log("MIC settings configured")	


# Callback function	
def interrupt_callback(self):
	global stop_streaming_flag
	stop_streaming_flag = True
	time.sleep(0.05)
	if ( (DEMO == True) and (STREAMING == True) ):
		thread.start_new_thread(blink_LED,(2, 0))
		dump_buffer(BUF_SIZE, AUDIO_SAMPLE_RATE, number_of_channels)
		thread.start_new_thread(blink_LED,(2, 1))
		if (AUTO_PLAYBACK == True):
			convert_to_wav("audio_file.raw", AUDIO_SAMPLE_RATE, number_of_channels)
			play_audio ("0", "audio_file.wav", 100)
		write_register_short ("01", "0001")
	else:
		thread.start_new_thread(blink_LED,(2, 1))
		wordID = int(read_register_short("5b"))
		if (wordID < 101): #Got a trigger
			if (DEMO == True):
				play_audio("0", "beep.wav",100)
			
			if (statistic == True):				
				sv_score=read_register_short("5d")
				write_to_log("Got a trigger! sv_score= 0x" + sv_score)					
				write_to_log("word id: 0x" + str(wordID))
			else:
				write_to_log("Got a trigger!")
			
		else: #Got a command
			write_to_log("Got a command!")
			write_to_log("word id: 0x" + str(wordID))
			

# Init function	
def reset():
	wakeup()
	GPIO.output(RESET_GPIO,False)
	time.sleep(0.1)
	GPIO.output(RESET_GPIO,True)
	time.sleep(0.1)
	
	# turn leds off
	GPIO.output(LED_GPIO,False)
	if (EVB_TYPE=="EVB_S"):
		GPIO.output(FIRMWARE_LOADED_LED_GPIO, False)
		
	write_to_log ("Reset the chip successfully")
	
#def init_demo(): # D6
	#global number_of_channels
	#disable_statistic()
	#change_interface_speed(1000000)			# Set interface speed to 2 MHz
	#write_register_short("29","0001") 		# Set host interface to UART
	#read_register("0")     	          		# read current FW version number
	#write_register("22","10C0")	      	
	#write_register("23","6020")
	#write_register("10","E000")
	#write_register("15","8e8e")       		# GPIO number to indicate pass phrase detection
	
	## Set microphones 
	#if (MIC == "DMIC_LEFT"):
		#write_register("24","2052")
		#number_of_channels = 1
	#elif (MIC == "DMIC_RIGHT"):
		#write_register("24","F043")
		#number_of_channels = 1
	#elif (MIC == "AMIC"):
		#write_register("24","0008")
		#number_of_channels = 1
	#elif (MIC == "STEREO"):
		#write_register("24","2042")			# MIC1
		#write_register("25","F053")			# MIC2
		#number_of_channels = 2
	
	## Set microphone's GAIN
	#if (MIC == "AMIC"):
		#write_register("4","0000")
		#write_register("16",ANALOG_GAIN_LEVEL)
	#else:
		#write_register("4",DIGITAL_GAIN_LEVEL)
		#write_register("16","0000")
	
	#if (STREAMING == False):
		#write_register("17","0008")			# reserved register for debug option (value '0008' means cancel the buffering mode and remain in detection mode)

	#write_to_log("Init ended")
	
def init_demo(): # For AMAZON project
	global number_of_channels
	disable_statistic()
	change_interface_speed(1000000)			# Set interface speed to 2 MHz
	write_register_short("29","0001") 		# Set host interface to UART
	read_register("0")     	          		# read current FW version number
	write_register("22","1060")
	
	reg_value = ((AUDIO_SAMPLE_RATE-16000)/160)+20
	write_register("23",reg_value)

	write_register("10","7000")				# Set DSP Clock
	write_register("15","8e8e")       		# GPIO number to indicate pass phrase detection
	
	# Set microphones 
	if (MIC == "DMIC_LEFT"):
		write_register("24","2042")
		number_of_channels = 1
	elif (MIC == "DMIC_RIGHT"):
		write_register("24","F041")
		number_of_channels = 1
	elif (MIC == "AMIC"):
		write_register("24","0008")
		number_of_channels = 1
	elif (MIC == "STEREO"):
		write_register("24","2042")			# MIC1
		write_register("25","F053")			# MIC2
		number_of_channels = 2
	
	# Set microphone's GAIN
	if (MIC == "AMIC"):
		write_register("4","0000")
		write_register("16",ANALOG_GAIN_LEVEL)
	else:
		write_register("4",DIGITAL_GAIN_LEVEL)
		write_register("16","0000")
	
	if (STREAMING == False):
		write_register("17","0008")			# reserved register for debug option (value '0008' means cancel the buffering mode and remain in detection mode)

	write_to_log("Init ended")

#def init_demo():
	#global number_of_channels
	#disable_statistic()
	#change_interface_speed(460800)			# Set interface speed to 460800
	#write_register_short("29","0001") 		# Set host interface to UART
	#read_register("0")     	          		# read current FW version number
	#write_register("22","1060")	      	
	
	#if (VOICE_COMMANDS == True):
		#reg_value = ((AUDIO_SAMPLE_RATE-16000)/160)+21
	#else: # Voice Trigger Mode
		##reg_value = ((AUDIO_SAMPLE_RATE-16000)/160)+23
		#reg_value = ((AUDIO_SAMPLE_RATE-16000)/160)+20
	#write_register("23",reg_value)

	## Set DSP Clock
	#if (VOICE_COMMANDS == True):
		#write_register("10","0017")
	#else: # Voice Trigger Mode
		##write_register("10","0013")
		#write_register("10","e000")
	
	#write_register("15","8e8e")       		# GPIO number to indicate pass phrase detection
	
	## Set microphones 
	#if (MIC == "DMIC_LEFT"):
		#write_register("24","2042")
		#number_of_channels = 1
	#elif (MIC == "DMIC_RIGHT"):
		#write_register("24","F041")
		#number_of_channels = 1
	#elif (MIC == "AMIC"):
		#write_register("24","0008")
		#number_of_channels = 1
	#elif (MIC == "STEREO"):
		#write_register("24","2042")			# MIC1
		#write_register("25","F053")			# MIC2
		#number_of_channels = 2
	
	## Set microphone's GAIN
	#if (MIC == "AMIC"):
		#write_register("4","0000")
		#write_register("16",ANALOG_GAIN_LEVEL)
	#else:
		#write_register("4",DIGITAL_GAIN_LEVEL)
		#write_register("16","0000")
	
	#if (STREAMING == False):
		#write_register("17","0008")			# reserved register for debug option (value '0008' means cancel the buffering mode and remain in detection mode)

	#write_to_log("Init ended")


def init():
	#disable_statistic()
	write_register_short("29","0001") 	  #enable UART interfaces
	#write_to_I2C_bus(cpld_i2c_addr, 0 ,PROJECT_CPLD)
	#read_register("0")                # read current FW version number
	#write_register("22","1060")       # Sensory uses separate 1k words buffer
	#write_register("23","0000")       # no VAD
	#write_register("10","f002")       # 8x24MHz = 192MHz DSP clock used, for 32KHz value 'f002' used
	#write_register("1d","0200")
	##write_register("1e","c180")      #
	#write_register("15","8b8b")       # GPIO number to indicate pass phrase detection, for 32KHz value '008b' used
	#write_register("24","a041")       # MIC1
	#write_register("25","a053")       # MIC2
	##write_register("1f","0204")      # TDM configuration - relevant only for AC
	#write_register("0c","7530")       # UART baud rate configuration (3M for UART recording)
	#write_register("02","0526")       # overall size of the trigger a-model - calculated per model
	#load_trigger_model ("1_HBG_330_p_run.bin")        # load trigger a-model 
	#read_register("41")                               # verify trigger a-model successfully loaded
	#load_asrp_param ("AsrpParams_V238_MMVT_007.bin")  # load ASRP param
	#write_register("34","0001")                       # enable ASRP algorithm
	#write_register("100","0021")                      # enable SINR and MIXERS only
	#write_register("30", "108c")                      # define  recording points
	#write_register("17","0008")                       # reserved register for debug option (value '0008' means cancel the buffering mode)
	#write_register("01","0001")                       # enter detection mode
	write_to_log("Init ended")


# Registers handling functions	

def wakeup():
	if ( (CHIP_TYPE=="D4") or (CHIP_TYPE=="D6") ):
		ser.write(chr(0x00))
		time.sleep(0.05)
		ser.write(chr(0x00))
		ser.flushInput()
		time.sleep(0.03)
	else:
		GPIO.output(WAKEUP_GPIO,True)
		time.sleep(0.1)	
	
def write_register(reg_num, value):
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
			read_register(reg_num)

			write_in_progress = False
			break
		else:
			write_to_log("writing in use... please wait...")
			time.sleep(0.01)
		
def write_register_short(reg_num, value):
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
			break
		else:
			write_to_log("writing in use... please wait...")
			time.sleep(0.01)

def read_register(register_num):
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
			write_to_log("reading in use... please wait...")
			time.sleep(0.01)
		
def read_register_short(register_num):
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
			return serRead
		else:
			write_to_log("reading in use... please wait...")			
			time.sleep(0.01)			

def read_register_loop(register_num):
	i=0
	write_to_log("reading register 0x" + str(register_num))
	while (i<100):
		read_register(register_num)
		time.sleep(0.1)
		i=i+1
	write_to_log("done loop reading") 

def read_IO_port (reg_address):
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
			break
		else:
			write_to_log("reading in use... please wait...")			
			time.sleep(0.01)

def write_IO_port (reg_address, reg_value):
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
			
			read_IO_port (reg_address)
			write_in_progress = False
			break
		else:
			write_to_log("writing in use... please wait...")			
			time.sleep(0.01)

def write_to_I2C_bus(i2c_address, reg_num, reg_value):
	reg_num = int(reg_num)
	reg_value = str(reg_value)
	reg_value = int(reg_value.zfill(4),16)
	i2c_address = int (i2c_address, 16)
	i2c.write_byte_data (i2c_address , reg_num, reg_value)
	write_to_log("I2C address: " + str(i2c_address) + ";  register number: 0x" + str(reg_num) + " ;  value: 0x" + str(reg_value))
	time.sleep(0.01)
	
def read_checksum_from_fw():
	ser.flushInput()
	ser.write(chr(0x5A) + chr(0x0E))
	readSerial = ser.read(6)
	readSerialList = list(readSerial)		
	for i in range (0, len(readSerialList)):
		readSerialList[i] = str(hex(ord(readSerialList[i])))
	time.sleep(0.01)
	return readSerialList[2:]

def dump_scu_reg():
	write_to_log("Dump SCU registers")
	dumpSCU = ['0060','0064','0068']
	write_register_short("6", "0300")
	for i in range(len(dumpSCU)):		
		write_register_short("5", dumpSCU[i])
		result_low = (str(read_register_short("7")))[:4]
		result_high = (str(read_register_short("8")))[:4]
		write_to_log("address: 0x0300" + dumpSCU[i] + " ;  value: 0x" + str(result_high) + " " + str(result_low))
	write_to_log("SCU registers Dump finished")

def dump_fw_reg():
	reg_addr = 0
	while (reg_addr < 111):
		reg_addr = reg_addr + 1
		text =  "In addr: " + (hex(reg_addr)) + " The value: " + read_register_short("r "+str(hex(reg_addr))[2:])
		write_to_log(text)

##################################
##################################
###### 		Main Code	 	######
##################################
##################################
gc.enable()
create_log_filename()

if (DEMO == True):
	reset() # Reset the chip
	load_fw (FIRMWARE) # upload FW
	init_demo() # Init the system for demo

	# Load acoustic model(s)
	pre_load_trigger_model(A_MODEL)
	if (VOICE_COMMANDS == True):
		pre_load_command_model(A_MODEL_VC)
		load_command_model(A_MODEL_VC)
	load_trigger_model(A_MODEL)

	write_register ("01", "0001") # Change to detection mode
	
	play_audio("0", "oksay.wav" ,100)
	blink_LED(4, 1)

GPIO.add_event_detect(INTERRUPT_TRIGGER_GPIO, GPIO.RISING, callback=interrupt_callback) 


print "\n********************* UART interface *****************"	
print ("\nTo dump audio buffer type: 'dump' followed by: 'Enter'\n\
To read register type: 'r <register_num>' followed by: 'Enter'\n\
To write to a register type: 'w <register_num> <value>' followed by: 'Enter'\n\
To load trigger acoustic model type: 'lt' followed by: 'Enter'\n\
To load command acoustic model type: 'lc' followed by: 'Enter'\n\
To load Google acoustic model type: 'lg' followed by: 'Enter'\n\
To reset the chip type: 'reset' followed by: 'Enter'\n\
To exit type: 'q' followed by: 'Enter'\n")


user_selection = ''
while (user_selection != 'q'):
	user_selection = raw_input("")
	userList=user_selection.split()
	if (user_selection == ''):
			print "Insert valid command"
	elif (userList[0] == "shell"):	
		userList=user_selection.split()
		userList.remove(userList[0])
		command= ' '.join(userList)	
		shell_command (command)
	elif ((len(userList)) == 1 ) :	
		if (user_selection == 'reset'):
			reset()
		elif (user_selection == 'scu'):
			dump_scu_reg()
		elif (user_selection == 'dump_reg'):
			dump_fw_reg()
		elif (user_selection == 'read_checksum'):
			read_checksum_from_fw()
		elif (user_selection == 'disable_statistic'):
			disable_statistic()
		elif (user_selection == 'enable_statistic'):
			enable_statistic()
		elif (user_selection == 'init'):
			init()
		elif (user_selection == 'stop_streaming'):
			stop_streaming()
		elif (user_selection == 'enter_hibernate'):
			enter_hibernate()
		elif (user_selection == 'exit_hibernate'):
			exit_hibernate()
		elif (user_selection == 'save_mic_settings'):
			save_mic_settings()
		elif (user_selection == 'config_mic'):
			config_mic()
		elif (user_selection == 'stop_audio'):
			stop_audio()
		elif (user_selection == 'create_acoustic_model'):
			create_acoustic_model()	
		elif (user_selection == 'show_values'):
			show_values()		
		elif (user_selection == 'q'):
			write_to_log("quit the system")			
		else:
			print "Insert valid command"
	elif ((len(userList)) == 2 ) :		
		if (userList[0] == "set_date_time"):
			set_date_time(userList[1])
		elif (userList[0] == 'reg_loop'):
			read_register_loop(userList[1])
		elif (userList[0] == 'lf'):
			load_fw(userList[1])
		elif (userList[0] == 'lt'):
			load_trigger_model(userList[1])
		elif (userList[0] == 'lc'):
			load_command_model(userList[1])
		elif (userList[0] == 'lg'):
			load_google_model(userList[1])
		elif (userList[0] == 'la'):
			load_asrp_param(userList[1])
		elif (user_selection[0] == 'r'):
			read_register(userList[1])
		elif (userList[0] == 'change_interface_speed'):
			change_interface_speed(userList[1])
		elif (userList[0] == 'import_values'):
			import_values_from_file(userList[1])
		elif (userList[0] == 'plt'):
			pre_load_trigger_model(userList[1])
		elif (userList[0] == 'plc'):
			pre_load_command_model(userList[1])
		elif (userList[0] == 'io_r'):
			read_IO_port(userList[1])
		else:
			print "Insert valid command"
	elif ((len(userList)) == 3 ) :	
		if (userList[0] == 'w'):
			write_register(userList[1], userList[2])
		elif (userList[0] == 's'):
			write_register_short(userList[1], userList[2])
		elif (userList[0] == 'play_audio'):
			thread.start_new_thread(play_audio,("0", userList[1], userList[2]))
		elif (userList[0] == 'io_w'):
			write_IO_port (userList[1], userList[2])
		else:
			print "Insert valid command"
	elif ((len(userList)) == 4 ) :
		if (userList[0] == "dump"):
			thread.start_new_thread(dump_buffer,(userList[1], userList[2], userList[3]))
		elif (userList[0] == "stream"):
			stream(userList[1], userList[2], userList[3])
		elif (userList[0] == "convert"):		
			convert_to_wav(userList[1], userList[2],userList[3])
		elif (userList[0] == 'play_audio'):
			thread.start_new_thread(play_audio,(userList[1], userList[2], userList[3]))
		elif (userList[0] == 'write_i2c'):
			write_to_I2C_bus(userList[1], userList[2], userList[3])
		else:
			print "Insert valid command"
	elif ((len(userList)) == 5 ) :
		if (userList[0] == "dump"):
			thread.start_new_thread(dump_buffer,(userList[1], userList[2], userList[3], userList[4]))
		elif (userList[0] == "convert"):		
			convert_to_wav(userList[1], userList[2], userList[3], userList[4])
		else:
			print "Insert valid command"
	else:
		print "Insert valid command"	

sys.exit(0)
