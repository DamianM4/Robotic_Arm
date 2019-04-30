import serial

ser = serial.Serial('COM3', 115200, timeout=2)
print(ser.name)

def send_data(value):
    ser.write(str.encode(value))

def receive_data():
    print(ser.readline())
'''
while 1:
    print "Podaj wartosc"
    val=raw_input()
    send_data(val)
    receive_data()
'''