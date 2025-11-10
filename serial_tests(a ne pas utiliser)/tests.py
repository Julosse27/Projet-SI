import serial as srl

serial = srl.Serial('/dev/rfcomm0', 9600)

serial.open()
serial.reset_input_buffer()

def envoyer_commande(index: int):
    return


def close():
    serial.close()