import board
import analogio
import time

# Entrada analógica en GP26 (A0)
ldr = analogio.AnalogIn(board.A0)

def read_ldr():
    return ldr.value  # 0 a 65535

while True:
    light = read_ldr()
    print("Valor LDR:", light)
    time.sleep(0.2)
