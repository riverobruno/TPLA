import board
import digitalio
import time
import usb_cdc
import analogio
import pwmio
import wifi
import socketpool
import adafruit_minimqtt.adafruit_minimqtt as MQTT
import json
led = digitalio.DigitalInOut(board.GP6)
led.direction = digitalio.Direction.OUTPUT

# Sensor (tilt switch) en GP11
sensor = digitalio.DigitalInOut(board.GP11)
sensor.direction = digitalio.Direction.INPUT
sensor.pull = digitalio.Pull.UP

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

# Entradas analógicas
pot = analogio.AnalogIn(board.A0)
ldr = analogio.AnalogIn(board.A1)

# Salida PWM al láser
laser = pwmio.PWMOut(board.GP14, frequency=5000, duty_cycle=0)
buzzer = pwmio.PWMOut(board.GP10, duty_cycle=0, frequency=440, variable_frequency=True)
paratemp={"bandera":False,"temporizador":0,"contador":0}


# Configuración de RED
SSID = "Tu wifi"
PASSWORD = "Contraseña de tu wifi"
BROKER = "La IPv4 de la pc donde corre mosquitto. Win: ipconfig o Linux: ip addr"  
NOMBRE_EQUIPO = "Actuadores"
DESCOVERY_TOPIC = "descubrir"
TOPIC = f"sensores/{NOMBRE_EQUIPO}"

print(f"Intentando conectar a {SSID}...")
try:
    wifi.radio.connect(SSID, PASSWORD)
    print(f"Conectado a {SSID}")
    print(f"Dirección IP: {wifi.radio.ipv4_address}")
except Exception as e:
    print(f"Error al conectar a WiFi: {e}")
    while True:
        pass 

# Configuración MQTT 
pool = socketpool.SocketPool(wifi.radio)

def connect(client, userdata, flags, rc):
    print("Conectado al broker MQTT")
    client.publish(DESCOVERY_TOPIC, json.dumps({"equipo":NOMBRE_EQUIPO,"magnitudes": ["posición", "inclinación"]}))

mqtt_client = MQTT.MQTT(
    broker=BROKER,
    port=1883,
    socket_pool=pool
)

mqtt_client.on_connect = connect
mqtt_client.connect()

# Usamos estas varaibles globales para controlar cada cuanto publicamos
LAST_PUB = 0
PUB_INTERVAL = 5  
def publish():
    global last_pub,pot_value,inclinado
    now = time.monotonic()
   
    if now - last_pub >= PUB_INTERVAL:
        try:
            pos_topic = f"{TOPIC}/posición" 
            mqtt_client.publish(pos_topic, str(pot_value))
            inclina_topic = f"{TOPIC}/inclinación" 
            mqtt_client.publish(inclina_topic, str(inclinado))
            
            last_pub = now
          
        except Exception as e:
            print(f"Error publicando MQTT: {e}")
def read_analog(pin):
    # Retorna valor 0-65535
    return pin.value

def beep(frequency, duration):
    buzzer.frequency = frequency
    buzzer.duty_cycle = 32768  # 50% duty cycle
    time.sleep(duration)
    buzzer.duty_cycle = 0      # apagar
    time.sleep(0.05)

def vertemporizador():#Todo esto del diccionario lo hice para hacer una especie de procedimiento sin definir dentro las variables globales
    if usb_cdc.console.in_waiting > 0:  # hay datos disponibles
        # Leer una línea completa (terminada en '\n')
        msg = usb_cdc.console.readline().decode("utf-8").strip()
        if msg.isdigit():
            paratemp["bandera"] = True
            display_number(3)
            paratemp["temporizador"] =2*(int(msg))
            paratemp["contador"] = 0
        else:
            print("entrada no válida")
    if paratemp["bandera"]:
        paratemp["contador"] += 1
        print(paratemp["contador"]) # 2 porque cada ciclo es 0.5s y la entrada es en segundos
        if paratemp["contador"] >= paratemp["temporizador"]:
            paratemp["bandera"] = False


while True:
    ## Estado 0: Espera potenciómetro > 1100, todo apagado
    while True:
        pot_value = read_analog(pot)
        ldr_value = read_analog(ldr)
        if not sensor.value:  # sensor activado
            led.value = True
        else:
            led.value = False
        inclinado=led.value
        if (pot_value)>1100:
            break
        display_number(0)
        print(f"Pot: {pot_value}, LDR: {ldr_value}, Inclinación: {led.value}")
        publish()
        if usb_cdc.console.in_waiting > 0:
            print("El sistema está apagado, gire el potenciómetro para programar la temporización")
        time.sleep(0.5)
        
    while True:
        pot_value = read_analog(pot)
        if not sensor.value:  # sensor activado
            led.value = True
        else:
            led.value = False
        inclinado=led.value
        if (pot_value)<1100:
            break
        vertemporizador()
        
        if not paratemp["bandera"]:
            
            # Ajustamos el duty_cycle según potenciómetro y LDR
            # LDR alto (mucha luz) reduce intensidad del láser
            duty = int(pot_value)
            laser.duty_cycle = duty
            time.sleep(0.1)  # Pequeña pausa para estabilizar lectura
            ldr_value = read_analog(ldr)
            if (ldr_value)>150:
                display_number(2)
                for n in range (5):
                    beep(440, 0.5)
                    print("je")
                    
            else:
                display_number(1)
                
            
        else:
            laser.duty_cycle = 0
        print(f"Pot: {pot_value}, LDR: {ldr_value}, Inclinación: {led.value}")
        publish()
        time.sleep(0.5)