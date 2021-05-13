"""
Responds to commands from Mac: PiGpioClient
LEDS: 18 (active high), 5, 6, 13, 19 (active low)
Buttons: 4, 17
CMDs:
LED  On  Off
18    1    2
 5    3    4
 6    5    6
13    7    8
19    9   10
All  11   12

0  -> server time
20 -> button status
99 -> server shutdown

Last touched: 10/18/2019
"""

from socket import *
import time
from gpiozero import LED, Button

print ("========================================")
# Configure PI GPIO pins - hardcode for now?
out18 = LED(18)
out18.off()
out05 = LED(5, active_high=False)
out05.off()
out06 = LED(6, active_high=False)
out06.off()
out13 = LED(13, active_high=False)
out13.off()
out19 = LED(19, active_high=False)
out19.off()

button04 = Button(4)
button17 = Button(17)

s = socket(AF_INET, SOCK_STREAM)    # create TCP socket
s.bind(('',8888))                   # bind to port 8888
s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
s.listen(2)                         # listen, but allow <=2 pending connections
print("Listening for connection...")
client,addr = s.accept()            # get a connection
print("...got a connection from %s" % str(addr))

cmdStr = "Cmd: "
buttonState = 0    # nothing pressed since last status msg
notDone = True
while notDone:
    # First we check button state
    if button04.is_pressed:
        buttonState = buttonState | 1
    
    if button17.is_pressed:
        buttonState = buttonState | 2
#    print("buttonState = %d" % buttonState)
    
    # Then we receive look for a command
    inCmd = client.recv(16)
    
    # Convert to string
    inCmdDecode = inCmd.decode('ascii', 'ignore')
    inCmdDecode = inCmdDecode[0:7]
#    print(" inCmdDecode = %s" % inCmdDecode)
    
    cmdStr = str(inCmdDecode.split()[0])
#    print("   cmdStr = %s" % cmdStr)
    
    cmdNum = 10*int(inCmdDecode[5]) + int(inCmdDecode[6])
#    print("  cmdNum= %d" % cmdNum)
    
    if cmdStr != "Cmd:":
        print("*** Malformed command from Mac")
        cmdNum = -1
    
    # Then we decode command and respond
    if cmdNum == 0:                 # return time string
        timestr = time.ctime(time.time()) + "\r\n"
        client.send(timestr.encode('ascii'))
    
    elif cmdNum == 1:               # turn LED18 on
        out18.on()
        respStr = "OK"
        client.send(respStr.encode("ascii"))
    
    elif cmdNum == 2:               # turn LED18 off
        out18.off()
        respStr = "OK"
        client.send(respStr.encode("ascii"))
    
    elif cmdNum == 3:               # turn LED05 on
        out05.on()
        respStr = "OK"
        client.send(respStr.encode("ascii"))
    
    elif cmdNum == 4:               # turn LED05 off
        out05.off()
        respStr = "OK"
        client.send(respStr.encode("ascii"))
    
    elif cmdNum == 5:               # turn LED06 on
        out06.on()
        respStr = "OK"
        client.send(respStr.encode("ascii"))
    
    elif cmdNum == 6:               # turn LED06 off
        out06.off()
        respStr = "OK"
        client.send(respStr.encode("ascii"))
    
    elif cmdNum == 7:               # turn LED13 on
        out13.on()
        respStr = "OK"
        client.send(respStr.encode("ascii"))
    
    elif cmdNum == 8:               # turn LED13 off
        out13.off()
        respStr = "OK"
        client.send(respStr.encode("ascii"))
    
    elif cmdNum == 9:               # turn LED19 on
        out19.on()
        respStr = "OK"
        client.send(respStr.encode("ascii"))
    
    elif cmdNum == 10:               # turn LED19 off
        out19.off()
        respStr = "OK"
        client.send(respStr.encode("ascii"))
    
    elif cmdNum == 11:               # turn all LEDs on
        out18.on()
        out05.on()
        out06.on()
        out13.on()
        out19.on()
        respStr = "OK"
        client.send(respStr.encode("ascii"))

    elif cmdNum == 12:               # turn all LEDs off
        out18.off()
        out05.off()
        out06.off()
        out13.off()
        out19.off()
        respStr = "OK"
        client.send(respStr.encode("ascii"))
    
    elif cmdNum == 20:              # get button status
        respStr = str(buttonState)
        client.send(respStr.encode("ascii"))
        buttonState = 0
    
    elif cmdNum == 99:               # terminate this program
        respStr = "Server shutting down"
        client.send(respStr.encode("ascii"))
        notDone = False
    
    else:
        print("*** Unexpected command number: %d", cmdNum)
        respStr = "*** Unexpected command number"
        client.send(respStr.encode("ascii"))
    
client.close()
print("client.close - bye")
