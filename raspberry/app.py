import RPi.GPIO as GPIO
from lib_nrf24 import NRF24
import time
import spidev
from random import randint

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

pipes = [[0xE8, 0xE8, 0xF0, 0xF0, 0xE1], [0xF0, 0xF0, 0xF0, 0xF0, 0xE1]]

radio = NRF24(GPIO, spidev.SpiDev())
radio.begin (0, 17)  # CE0 value 0 is GPIO 8  CE Value - GPIO 17

radio.setPayloadSize(32)
radio.setChannel(0x76)
radio.setDataRate(NRF24.BR_1MBPS)
radio.setPALevel(NRF24.PA_MAX)

radio.setAutoAck(True)
radio.enableDynamicPayloads()
radio.enableAckPayload()

radio.openWritingPipe(pipes[0])
radio.openReadingPipe(1,pipes[1])
radio.printDetails()
#radio.startListening()
time.sleep(1)

while True:
    message = "1P"       
    while len(message) <32:
        message.append(0)
    
    radio.write(message)
    print("sent the message: {}".format(message))
    radio.startListening()

    while not radio.available(0):
        time.sleep(1/100)

    receivedMessage = []
    radio.read(receivedMessage, radio.getDynamicPayloadSize())
    print ("Received: {}".format(receivedMessage))

    print("Translating our received message into unicode characters...")
    string = ""

    for n in receivedMessage:
        if (n >=32 and n <= 126):
            string += chr(n)
    print("Our received message decodes to: {}".format(string))

    radio.stopListening()   

    print("Waiting ...")
    time.sleep(3)
