import board
import digitalio
import time

# Configurar pines de los segmentos
segments = []
pins = [board.GP0, board.GP1, board.GP2, board.GP3, board.GP26, board.GP27, board.GP28]

for pin in pins:
    seg = digitalio.DigitalInOut(pin)
    seg.direction = digitalio.Direction.OUTPUT
    segments.append(seg)

# Tabla de números 0-9 (cátodo común)
numbers = [

    [0,1,1,1,1,1,1],  # 0
    [0,0,0,1,1,0,0],  # 1
    [1,0,1,1,0,1,1],  # 2
    [1,0,1,1,1,1,0],  # 3
    [1,1,0,1,1,0,0],  # 4
    [1,1,1,0,1,1,0],  # 5
    [1,1,1,0,1,1,1],  # 6
    [0,0,1,1,1,0,0],  # 7
    [1,1,1,1,1,1,1],  # 8
    [1,1,1,1,1,1,0]   # 9
]

def display_number(num):
    for i in range(7):
        segments[i].value = numbers[num][i]

while True:
    for n in range(10):
        display_number(n)
        time.sleep(1)
