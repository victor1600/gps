#!/usr/bin/python
import RPi.GPIO as GPIO
import serial
import time
from decimal import *
#EJECUCION DE BOTON
GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.OUT)

while True:
	GPIO.output(7, GPIO.LOW)
	time.sleep(4)
	GPIO.output(7, GPIO.HIGH)
	break
GPIO.cleanup()
#ejecucion de GPS
def find(str, ch):
    for i, ltr in enumerate(str):
        if ltr == ch:
            yield i

port = serial.Serial("/dev/ttyUSB0", baudrate=115200, timeout=1)

port.write('AT'+'\r\n')
rcv = port.read(100)
print ('rcv')
time.sleep(.1)

port.write('AT+CGNSPWR=1'+'\r\n')
rcv = port.read(100)
print ('rcv')
time.sleep(.1)

port.write('AT+CGNSIPR=115200'+'\r\n')
rcv = port.read(100)
print ('rcv')
time.sleep(.1)

port.write('AT+CGNSTST=1'+'\r\n')
rcv = port.read(100)
print ('rcv')
time.sleep(.1)

port.write('AT+CGNSINF'+'\r\n')
rcv = port.read(200)
print ('rcv')
time.sleep(.1)
ck=1
while ck==1:
    fd = port.read(200)
    time.sleep(.5)
    if '$GNRMC' in fd:
        ps=fd.find('$GNRMC')
        dif=len(fd)-ps
        if dif >= 50:
            data=fd[ps:(ps+50)]
            ds=data.find('A')
            if ds >= 0 and ds <= 20:
                p=list(find(data, ","))
                lat=data[(p[2]+1):p[3]]
                lon=data[(p[4]+1):p[5]]

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
            print ('Latitud y Longitud: ' + str(s1))+(',' + str((s2 * (-1))))


            if s1 is not None and s2 is not None:
                archivo = open('coords.json', 'a')
                archivo.write('[{},{}],'.format(str((s2 * (-1))), str(s1)))
                archivo.close()