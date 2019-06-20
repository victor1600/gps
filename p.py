#!/usr/bin/python

import serial
import time
from decimal import *
from subprocess import call

def find(str, ch):
    for i, ltr in enumerate(str):
        if ltr == ch:
            yield i

# Enable Serial Communication
port = serial.Serial("/dev/ttyS0", baudrate=115200, timeout=1)
# Transmitting AT Commands to the Modem
# '\r\n' indicates the Enter key

port.write('AT'+'\r\n')
rcv = port.read(100)
print ('rcv')
time.sleep(.1)

port.write('AT+CGNSPWR=1'+'\r\n')    	 	# to power the GPS
rcv = port.read(100)
print ('rcv')
time.sleep(.1)

port.write('AT+CGNSIPR=115200'+'\r\n') # Set the baud rate of GPS
rcv = port.read(100)
print ('rcv')
time.sleep(.1)

port.write('AT+CGNSTST=1'+'\r\n')    # Send data received to UART
rcv = port.read(100)
print ('rcv')
time.sleep(.1)

port.write('AT+CGNSINF'+'\r\n')   	# Print the GPS information
rcv = port.read(200)
print ('rcv')
time.sleep(.1)
ck=1
while ck==1:
    fd = port.read(200)		# Read the GPS data from UART
    #print fd
    time.sleep(.5)
    if '$GNRMC' in fd:		# To Extract Lattitude and
        ps=fd.find('$GNRMC')		# Longitude
        dif=len(fd)-ps
        if dif >= 50:
            data=fd[ps:(ps+50)]
            print ('data')
            ds=data.find('A')		# Check GPS is valid
            if ds >= 0 and ds <= 20:
                p=list(find(data, ","))
                lat=data[(p[2]+1):p[3]]
                lon=data[(p[4]+1):p[5]]

# GPS data calculatio

                s1=lat[2:len(lat)]
                s1=Decimal(s1)
                s1=s1/60
                s11=int(lat[0:2])
                s1 = s11+s1

                s2=lon[3:len(lon)]
                s2=Decimal(s2)
                s2=s2/60
                s22=int(lon[0:3])
                s2 = s22+s2

                print ('Latitud y Longitud:' + str(s1))+("," + str((s2 * (-1))))
