import serial
import time

rec_array ="allah akber"
first_enter=False
content=""
bytes_index=0
End_programming_flag=False
start_recieving=False
file_size=0
uploading_percentage=0


def boot_serial(file_path,usb_port,baud_rate):
        global first_enter
        global content
        global bytes_index
        global End_programming_flag
        global file_size
        global start_recieving
        global uploading_percentage
	
        if first_enter==False :
            first_enter=True
           
            file = open(file_path, 'r')
            content = file.read()
            file_size=len(content)
            print ("len file ")
            print (file_size)
            file.close()
            start_recieving=True
            

	
	
        for x in range(0,1) :
                
            boot_init_port.ser.write(content[bytes_index].encode())
            print(content[bytes_index], end ="", sep="")
            bytes_index+=1
           
            uploading_percentage=int((bytes_index/file_size)*100)
            #print(str(uploading_percentage)+"%")
            
            
                    
            if bytes_index>=file_size :
                print ("matched")
                print (bytes_index)
                print (file_size)
                End_programming_flag=True
                file_size=0
                bytes_index=0
                first_enter=False
                start_recieving=False
                
	
	
	
	

		
def boot_read_ch_serial():
	
	rec_char = boot_init_port.ser.read()
	rec_array+=str(rec_char)
	return rec_char
def boot_send_string(_string):
     boot_init_port.ser.write(_string.encode())
def boot_close_port():
	boot_init_port.ser.close()
	
def boot_open_port():
	if boot_port_status() :
		print("opened")	
		return True
	else :
		print("closed")
		boot_init_port.ser.open()
		return False

def boot_init_port(usb_port,baud_rate):	
	boot_init_port.ser = serial.Serial(usb_port, baud_rate,timeout=0.016)
	
def boot_port_status():
		if boot_init_port.ser.isOpen():
			return True
		else :
			return False

'''			
boot_init_port("COM3","2400")
boot_open_port()

boot_serial("D:\python\myprojects\myfile.txt","COM3","2400")

boot_close_port()

'''	
