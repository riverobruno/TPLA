import board
import pwmio
import time

laser = pwmio.PWMOut(board.GP14, frequency=1000, duty_cycle=0, variable_frequency=False)

# Aumentar y disminuir intensidad
while True:
    # Encender gradualmente
    for duty in range(0, 65535, 2000):
        laser.duty_cycle = duty
        time.sleep(0.05)
    # Apagar gradualmente
    for duty in range(65535, 0, -2000):
        laser.duty_cycle = duty
        time.sleep(0.05)
