import serial
import time
import serial.tools.list_ports

def pause(text):
    try: 
        input(text)
    except: 
        pass

porte = serial.tools.list_ports.comports()



for port, desc, hwid in porte:
   global ser
   if "Arduino Mega 2560" in desc:
       ser = serial.Serial(str(port))
       break


# ser = serial.Serial("COM13")

time.sleep(1)


var = ser.read() 
# while var == b'%':
#     var = ser.read()

while True:
    var = ser.read() 
    if var == (41).to_bytes(1):
        ser.write("c".encode("utf-8"))
    else:
        ser.write("w".encode("utf-8"))

    time.sleep(5)
    # var = "c"
    # var2 = "12"
    # i = 0

    # print(ser.name)
    # ser.write("w".encode("utf-8"))
    # ser.write("w".encode("utf-8"))

    # pause("Invio per continuare...")
    # char = ser.read(1)
    # print(char)
ser.close()
