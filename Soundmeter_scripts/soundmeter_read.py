import usb.util
import time
import colorama
from colorama import Fore, Back, Style
import mysql.connector 

config = {  
	"user": "damian",
	"password": "j3Remy.J0hn",
	"host": "141.19.143.13",   
	"database": "calmvie"
}


db = mysql.connector.connect(**config)
#need to change to specific id of soundmeter
#which is attached to raspberry
idsoundmeter =1

VID = 0x0483
PID = 0x5750

active=True # Variable stop the while loop.

#Find device
#If you want to use multiple soundmeter, you need to the same for a different usb-port
dev = usb.core.find(idVendor=VID, idProduct=PID)

cfg = dev.get_active_configuration()
intf = cfg[(0,0)]
ep_out = intf [1]
ep_in = intf[0]
intf_i = intf.bInterfaceNumber

if dev is None:
    print("Gerät wurde nicht gefunden.")
else:
    print("Gerät wurde gefunden.")
    
#if remainin process still active: stop process
if dev.is_kernel_driver_active(intf_i):
    dev.detach_kernel_driver(intf_i)
    
dev.set_configuration()

#message for the soundmeter
msg = [0xB3]+[0x00]*(0x40-1)

mycursor = db.cursor()
try:
    while active:                
        #communicate with soundmeter
        dev.write(ep_out, msg)
        ret = dev.read(ep_in, 0x40)
                    
        #first 2 ints of soundmeter -> soundmeter response
        if isinstance(ret[0], int) and isinstance(ret[1], int):
            lautstaerke = ret[0]*256 + ret[1]   #Hier muss noch eine Liste an Lautstärken hin
                    
        ausgabe_lautstaerke = lautstaerke//10     
        string_lautstaerke = str(ausgabe_lautstaerke)
        
        sql = "INSERT INTO measurement (time, soundmeter_id, value) VALUES (NOW(), %s, %s)"
        val = [
                (idsoundmeter,ausgabe_lautstaerke),
                #If u want to have multiple soundmeter attached to the raspberry, you can add more values here.
                #(2,ausgabe_lautstaerke+2)
              ]
        mycursor.executemany(sql, val)
        
        db.commit()
        time.sleep(1)
finally:                
    dev.reset()
    db.close()
    mycursor.close()