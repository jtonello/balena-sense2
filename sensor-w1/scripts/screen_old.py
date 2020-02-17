import time #import time for creating delay 
import RPi.GPIO as GPIO #Import LCD library 
import os #Import for file handling 
import glob #Import for global
 
lcd_rs        = 7  #RS of LCD is connected to GPIO 7 on PI
lcd_en        = 8  #EN of LCD is connected to GPIO 8 on PI 
lcd_d4        = 25 #D4 of LCD is connected to GPIO 25 on PI
lcd_d5        = 24 #D5 of LCD is connected to GPIO 24 on PI
lcd_d6        = 23 #D6 of LCD is connected to GPIO 23 on PI
lcd_d7        = 18 #D7 of LCD is connected to GPIO 18 on PI
lcd_backlight =  0  #LED is not connected so we assign to 0
 
lcd_columns = 16 #for 16*2 LCD
lcd_rows    = 2 #for 16*2 LCD
 
# Start new stuff
# Device constants
LCD_CHR = True # Character mode
LCD_CMD = False # Command mode
LCD_CHARS = 16 # Characters per line (16 max)
LCD_LINE_1 = 0x80 # LCD memory location for 1st line
LCD_LINE_2 = 0xC0 # LCD memory location 2nd line

# Define main program code
def main():
 
 GPIO.setwarnings(False)
 GPIO.setmode(GPIO.BCM) # Use BCM GPIO numbers
 GPIO.setup(lcd_en, GPIO.OUT) # Set GPIO's to output mode
 GPIO.setup(lcd_rs, GPIO.OUT)
 GPIO.setup(lcd_d4, GPIO.OUT)
 GPIO.setup(lcd_d5, GPIO.OUT)
 GPIO.setup(lcd_d6, GPIO.OUT)
 GPIO.setup(lcd_d7, GPIO.OUT)

# Initialize display
 lcd_init()

# Loop - send text and sleep 3 seconds between texts
# Change text to anything you wish, but must be 16 characters or less

 while True:
 lcd_text("Hello World!",LCD_LINE_1)
 lcd_text("",LCD_LINE_2)

 lcd_text("Rasbperry Pi",LCD_LINE_1)
 lcd_text("16x2 LCD Display",LCD_LINE_2)

 time.sleep(3) # 3 second delay

 lcd_text("ABCDEFGHIJKLMNOP",LCD_LINE_1)
 lcd_text("1234567890123456",LCD_LINE_2)

 time.sleep(3) # 3 second delay

 lcd_text("I love my",LCD_LINE_1)
 lcd_text("Raspberry Pi!",LCD_LINE_2)

 time.sleep(3)

 lcd_text("MBTechWorks.com",LCD_LINE_1)
 lcd_text("For more R Pi",LCD_LINE_2)

 time.sleep(3)



# from original below
#lcd = LCD.GPIO(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, 
                           lcd_columns, lcd_rows, lcd_backlight)   #Send all the pin details to library 
 
#lcd.message('DS18B20 with Pi \n -CircuitDigest') #Give a intro message
 
#time.sleep(2) #wait for 2 secs
 
os.system('modprobe w1-gpio') 
os.system('modprobe w1-therm')
 
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'
  
def get_temp(): #Fundtion to read the value of Temperature
    file = open(device_file, 'r') #opent the file
    lines = file.readlines() #read the lines in the file 
    file.close() #close the file 
 
    trimmed_data = lines[1].find('t=') #find the "t=" in the line
 
    if trimmed_data != -1:
        temp_string = lines[1][trimmed_data+2:] #trim the strig only to the temoerature value
        temp_c = float(temp_string) / 1000.0 #divide the value of 1000 to get actual value
        return temp_c #return the value to prnt on LCD
 
while 1: #Infinite Loop
 
    #lcd.clear() #Clear the LCD screen
    lcd_text('Temp = %.1f C' % get_temp()) # Display the value of temperature
 
    time.sleep(1) #Wait for 1 sec then update the values

# End of main program code


# Initialize and clear display
def lcd_init():
 lcd_write(0x33,LCD_CMD) # Initialize
 lcd_write(0x32,LCD_CMD) # Set to 4-bit mode
 lcd_write(0x06,LCD_CMD) # Cursor move direction
 lcd_write(0x0C,LCD_CMD) # Turn cursor off
 lcd_write(0x28,LCD_CMD) # 2 line display
 lcd_write(0x01,LCD_CMD) # Clear display
 time.sleep(0.0005) # Delay to allow commands to process

def lcd_write(bits, mode):
# High bits
 GPIO.output(lcd_rs, mode) # RS

 GPIO.output(lcd_d4, False)
 GPIO.output(lcd_d5, False)
 GPIO.output(lcd_d6, False)
 GPIO.output(lcd_d7, False)
 if bits&0x10==0x10:
 GPIO.output(lcd_d4, True)
 if bits&0x20==0x20:
 GPIO.output(lcd_d5, True)
 if bits&0x40==0x40:
 GPIO.output(lcd_d6, True)
 if bits&0x80==0x80:
 GPIO.output(lcd_d7, True)

# Toggle 'Enable' pin
 lcd_toggle_enable()

# Low bits
 GPIO.output(lcd_d4, False)
 GPIO.output(lcd_d5, False)
 GPIO.output(lcd_d6, False)
 GPIO.output(lcd_d7, False)
 if bits&0x01==0x01:
 GPIO.output(lcd_d4, True)
 if bits&0x02==0x02:
 GPIO.output(lcd_d5, True)
 if bits&0x04==0x04:
 GPIO.output(lcd_d6, True)
 if bits&0x08==0x08:
 GPIO.output(lcd_d7, True)

# Toggle 'Enable' pin
 lcd_toggle_enable()

def lcd_toggle_enable():
 time.sleep(0.0005)
 GPIO.output(lcd_en, True)
 time.sleep(0.0005)
 GPIO.output(lcd_en, False)
 time.sleep(0.0005)

def lcd_text(message,line):
 # Send text to display
 message = message.ljust(LCD_CHARS," ")

 lcd_write(line, LCD_CMD)

 for i in range(LCD_CHARS):
 lcd_write(ord(message[i]),LCD_CHR)


#Begin program
try:
 main()
 
except KeyboardInterrupt:
 pass
 
finally:
 lcd_write(0x01, LCD_CMD)
 lcd_text("So long!",LCD_LINE_1)
 lcd_text("MBTechWorks.com",LCD_LINE_2)
 GPIO.cleanup()    