import serial as srl

serial = srl.Serial('/dev/rfcomm0', 9600)

serial.open()
serial.reset_input_buffer()

for x in range(50):
    serial.write(bytes(str(x), 'uft_8'))
    inVar = serial.read_until().decode()
    print(f"OUT: {str(x)} IN: {str(inVar)}")

serial.close()