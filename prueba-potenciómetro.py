import board
import analogio
import time

# Potenciómetro en GP26
pot = analogio.AnalogIn(board.A0)

while True:
    value = pot.value  # 0 a 65535
    voltage = (value / 65535) * 3.3
    print(f"Valor ADC: {value}, Voltaje: {voltage:.2f} V")
    time.sleep(0.2)
