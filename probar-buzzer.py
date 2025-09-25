import board
import pwmio
import time

# Buzzer en GP14 (puedes cambiar por otro pin)
buzzer = pwmio.PWMOut(board.GP14, duty_cycle=0, frequency=440, variable_frequency=True)

def beep(frequency, duration):
    buzzer.frequency = frequency
    buzzer.duty_cycle = 32768  # 50% duty cycle
    time.sleep(duration)
    buzzer.duty_cycle = 0      # apagar
    time.sleep(0.05)

# Probar varios tonos
while True:
    beep(440, 0.5)  # La
    beep(880, 0.5)  # La más agudo
    beep(660, 0.5)  # Mi
