import tkinter as tk
import tkinter.messagebox as msgbox
import boot_loader_module as boot
import serial.tools.list_ports
from tkinter import filedialog as fd
import time
 

rec =False
number_of_rec_chars=0
recieved_bytes=""
# Dropdown menu options
Baud_rates = [
    "1200",
	"2400",
	"4800",
	"9600",
	"56000",
	"115200",
]

 
class Window(tk.Tk):
	def __init__(self):
		super().__init__()
		self.title("Bruchless Motor Boot Loader Tool")
		
		
		ports = serial.tools.list_ports.comports()
		available_ports = ["None"]
		for x in ports:
			available_ports.append(x.device)

		print(available_ports)
		
		
		self.clicked_ports = tk.StringVar()
		self.clicked_ports.set( "COM4" )

		self.clicked_baudrate = tk.StringVar()
		self.clicked_baudrate.set( "2400" )

		
		self.name_text = tk.StringVar()
		self.name_text.set("D:\python\myprojects\myfile.txt")
		
		
		self.label_file_path_text = tk.Label(self, text = "Please Enter The Hex File Path :").place(x = 10,y = 10)  
		self.name_entry = tk.Entry(self, textvar=self.name_text,width=50).place(x=15,y=40)
		
		get_hex_file_button = tk.Button(self, text="...",command=self.open_file_dialog,height=1,width=3).place(x = 325,y = 37)
		
		self.label_port_text = tk.Label(self, text = "Select The USB PORT").place(x = 10,y = 90) 
		self.drop_ports = tk.OptionMenu( self , self.clicked_ports , *available_ports ).place(x=15,y=120)
		
		self.label_text="Port is Closed"
		self.label_port_status = tk.Label(self, text = self.label_text)
		self.label_port_status.place(x = 130,y = 125) 
		
		#self.label_baudrate_text = tk.Label(self, text = "Select The BaudRate").place(x = 10,y = 120) 
		#self.drop_baudrate = tk.OptionMenu( self , self.clicked_baudrate , *Baud_rates ).place(x=15,y=140)
		
		
		self.label_uart_response_text = tk.Label(self, text = "",anchor='w',height=1,width=50,bg="white")
		self.label_uart_response_text.place(x = 15,y = 180)

        
		self.label_percentage = tk.Label(self, text = "0%")
		self.label_percentage.place(x = 380,y = 180)        
		
		Open_serial_button = tk.Button(self, text="Open Port",command=self.Open_PORT,height=1,width=10).place(x = 400,y = 10)  
		
		hello_button = tk.Button(self, text="Start program",command=self.Start_programming,height=1,width=10).place(x = 400,y = 50)
		
		close_serial_button = tk.Button(self, text="Close Port",command=self.Close_PORT,height=1,width=10).place(x = 400,y = 90) 
		
		Exit_button = tk.Button(self, text="Exit",command=self.Exit,height=1,width=10).place(x = 400,y = 130) 
		
	
	def open_file_dialog(self) :
		self.name_text.set(fd.askopenfilename())
	
	def Start_programming(self):
            boot.boot_close_port()
            boot.boot_init_port(self.clicked_ports.get(),"9600")
            boot.boot_send_string("start boot")
            time.sleep(1)
            boot.boot_close_port()
            boot.boot_init_port(self.clicked_ports.get(),self.clicked_baudrate.get())
            open_response=boot.boot_open_port()
            self.label_port_status.configure(text="Port is Opened")	
            global rec	
            self.label_percentage['text'] = ""
            rec=True

		
		
		
		
	
	
	def Read_uart_recieving(self):
		print("nothing")
		
	
	def Close_PORT(self):
		global rec
		self.label_port_status.configure(text="Port is Closed")	
		boot.boot_close_port()
		rec=False
		

	def Open_PORT(self):
		
		boot.boot_init_port(self.clicked_ports.get(),self.clicked_baudrate.get())
		open_response=boot.boot_open_port()
		if open_response==True :
			self.label_port_status.configure(text="Port is Opened")			
		else :
			msgbox.showerror("Error")
		
	def Exit(self):
			self.after(0, self.destroy)
		
	def task(self):
    
        
            global rec
            global number_of_rec_chars
            global recieved_bytes
        
        
            if rec==True :
        
                boot.boot_serial(self.name_text.get(),self.clicked_ports.get(),self.clicked_baudrate.get())
                
                self.label_percentage['text'] = str(boot.uploading_percentage)
                self.label_percentage['text'] += '%'
                self.label_uart_response_text['text'] = ""
                print_numbers=int(boot.uploading_percentage)
                print_numbers/=2
                for q in range(0,int(print_numbers)):
                    self.label_uart_response_text['text'] += "#"
            if boot.start_recieving==True :
                y=boot.boot_init_port.ser.read(2).decode('utf-8')	
                z=str(y)
#print(z, end ="")
                recieved_bytes+=z
                if z=="##" :
                    print("Target_Responding")
                    boot.start_recieving=False
                    
                    
			
		
            if  boot.End_programming_flag==True :
                self.label_percentage['text'] = "100%"
                msgbox.showinfo("Done", "Done Uploading The Code")
                boot.End_programming_flag=False
                rec=False
		
            window.after(1, self.task)  # reschedule event in 2 seconds


if __name__ == "__main__":
	window = Window()
	window.geometry("490x210")
	window.after(1, window.task)
	window.mainloop()
    
 
