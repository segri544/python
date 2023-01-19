import serial.tools.list_ports


ports=serial.tools.list_ports.comports()
# create blank instance of serial object

serialInst= serial.Serial()
portList=[]

# add all ports in list and show them
for oneport in ports:
    portList.append(str(oneport))
    print(str(oneport))

val=input("select port: COM")
for x in range(0,len(portList)):
    if portList[x].startswith("COM"+str(val)):
        portVar = "COM" + str(val)
        print(portVar)# or print(portlist[x])

serialInst.baudrate = 9600  # gönderilen datanın sampling rate ile okunan sample rate ayı olmalı
serialInst.port = portVar
serialInst.open()

while True:
    if serialInst.in_waiting:
        packet = serialInst.readline()
        print(packet.decode('utf'))
        