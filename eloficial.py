import board
import digitalio
import time

# Configurar pines de los segmentos
segments = []
pins = [board.GP0, board.GP1, board.GP2, board.GP3, board.GP18, board.GP19, board.GP20]

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




import analogio
import pwmio


# Entradas analógicas
pot = analogio.AnalogIn(board.A0)
ldr = analogio.AnalogIn(board.A1)

# Salida PWM al láser
laser = pwmio.PWMOut(board.GP14, frequency=5000, duty_cycle=0)
buzzer = pwmio.PWMOut(board.GP10, duty_cycle=0, frequency=440, variable_frequency=True)
def read_analog(pin):
    # Retorna valor 0-65535
    return pin.value

def beep(frequency, duration):
    buzzer.frequency = frequency
    buzzer.duty_cycle = 32768  # 50% duty cycle
    time.sleep(duration)
    buzzer.duty_cycle = 0      # apagar
    time.sleep(0.05)
while True:
    ## Estado 0: Espera potenciómetro > 1100, todo apagado
    while True:
        pot_value = read_analog(pot)
        ldr_value = read_analog(ldr)
        if (pot_value)>1100:
            break
        display_number(0)
        duty = int(pot_value * (1 - ldr_value / 65535))
        laser.duty_cycle = duty
    while True:
        pot_value = read_analog(pot)
        ldr_value = read_analog(ldr)
        if (pot_value)<1100:
            break
        

        if (ldr_value)>150:
            display_number(2)
            for n in range (5):
                beep(440, 0.5)  # La
        else:
            display_number(1)
            
        # Normalizamos LDR a factor entre 0 y 1
        ldr_factor = ldr_value / 65535
        
        # Ajustamos el duty_cycle según potenciómetro y LDR
        # LDR alto (mucha luz) reduce intensidad del láser
        duty = int(pot_value * (1 - ldr_factor))
        laser.duty_cycle = duty
        
        print(f"Pot: {pot_value}, LDR: {ldr_value}, Duty: {duty}")
        time.sleep(0.1)