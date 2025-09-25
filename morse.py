import time
import board
import digitalio
"""recordar que al querer usar este codigo en una raspberry pi pico se debe nombrar el archivo como code.py
"""
# Diccionario Morse
MORSE_CODE = {
    "A": ".-",   "B": "-...", "C": "-.-.", "D": "-..",
    "E": ".",    "F": "..-.", "G": "--.",  "H": "....",
    "I": "..",   "J": ".---", "K": "-.-",  "L": ".-..",
    "M": "--",   "N": "-.",   "O": "---",  "P": ".--.",
    "Q": "--.-", "R": ".-.",  "S": "...",  "T": "-",
    "U": "..-",  "V": "...-", "W": ".--",  "X": "-..-",
    "Y": "-.--", "Z": "--..",
    " ": " "  # espacio para separar palabras
}

# Configuración LED en GP2
led = digitalio.DigitalInOut(board.GP2)
led.direction = digitalio.Direction.OUTPUT

# Definición de tiempos
DOT = 0.2       # punto = 1 unidad
DASH = DOT * 3  # raya = 3 unidades
LETTER_SPACE = DOT * 3
WORD_SPACE = DOT * 7

def blink(symbol):
    """Hace parpadear un símbolo morse (punto o raya)."""
    if symbol == ".":
        led.value = True
        time.sleep(DOT)
        led.value = False
    elif symbol == "-":
        led.value = True
        time.sleep(DASH)
        led.value = False
    time.sleep(DOT)  # espacio entre símbolos de una misma letra

def send_message(msg):
    for char in msg.upper():
        if char == " ":
            time.sleep(WORD_SPACE - LETTER_SPACE)  # espacio entre palabras
        else:
            morse = MORSE_CODE.get(char, "")
            for symbol in morse:
                blink(symbol)
            time.sleep(LETTER_SPACE - DOT)  # espacio entre letras

# Mensaje a enviar
mensaje = "JOA GAY"

while True:
    send_message(mensaje)
    time.sleep(3)  # pausa antes de repetir
