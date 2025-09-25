import board
import digitalio
import time

# LED en GP14
led = digitalio.DigitalInOut(board.GP14)
led.direction = digitalio.Direction.OUTPUT

# Sensor (tilt switch) en GP15
sensor = digitalio.DigitalInOut(board.GP15)
sensor.direction = digitalio.Direction.INPUT
sensor.pull = digitalio.Pull.UP   # el módulo suele dar LOW cuando está cerrado

while True:
    if not sensor.value:  # sensor activado
        led.value = True
    else:
        led.value = False
    time.sleep(0.1)
