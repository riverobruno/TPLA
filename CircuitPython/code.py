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

# Sensor (tilt switch) en GP7
sensor = digitalio.DigitalInOut(board.GP7)
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
SSID = "el nombre del WiFi"
PASSWORD = "La contraseña del WiFi"
BROKER = "IPv4 del broker MQTT"
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
    client.publish(DESCOVERY_TOPIC, json.dumps({"equipo":NOMBRE_EQUIPO,"magnitudes": ["posicion", "inclinacion", "porcentaje de luz"]}))

mqtt_client = MQTT.MQTT(
    broker=BROKER,
    port=1883,
    socket_pool=pool
)

mqtt_client.on_connect = connect
mqtt_client.connect()

# Usamos estas varaibles globales para controlar cada cuanto publicamos
last_pub = 0
PUB_INTERVAL = 5  
def publish():
    global last_pub,elangulo,elporcentaje,inclinado
    now = time.monotonic()
   
    if now - last_pub >= PUB_INTERVAL:
        try:
            pos_topic = f"{TOPIC}/posicion" 
            mqtt_client.publish(pos_topic, str(elangulo))
            inclina_topic = f"{TOPIC}/inclinacion" 
            mqtt_client.publish(inclina_topic, str(inclinado))
            luz_topic = f"{TOPIC}/porcentaje de luz"
            mqtt_client.publish(luz_topic, str(elporcentaje))
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
            paratemp["temporizador"] =2*(int(msg)) # 2 porque cada ciclo es 0.5s y la entrada es en segundos
            paratemp["contador"] = 0
        else:
            print("entrada no válida")
    if paratemp["bandera"]:
        paratemp["contador"] += 1
        print("temporizador en curso") 
        if paratemp["contador"] >= paratemp["temporizador"]:
            paratemp["bandera"] = False

def angulo_potenciometro(valor_adc, valor_min=0, valor_max=65535):
    """
    Convierte el valor ADC del potenciómetro a ángulos (0-180 grados)
    
    Args:
        valor_adc (int): Valor ADC del potenciómetro (0 a 65535)
    
    Returns:
        float: Ángulo en grados (0° a 180°)
    """
    # Normalizar el valor de mínimo-máximo a 0-180 grados
    valor_limitado = max(valor_min, min(valor_adc, valor_max))
    angulo = (valor_limitado-valor_min) / (valor_max-valor_min) * 180
    return round(angulo)

def intensidad_fotorresistor(valor_adc, valor_min=0, valor_max=65535):
    """
    Convierte el valor ADC del fotorresistor KY-018 a porcentaje de luz
    
    NOTA: El fotorresistor disminuye su valor cuando recibe más luz
    
    Args:
        valor_adc (int): Valor ADC del fotorresistor (0 a 65535)
        valor_min (int): Valor mínimo con mucha luz (por defecto 0)
        valor_max (int): Valor máximo en oscuridad (por defecto 65536)

    Returns:
        float: Porcentaje de luz (0% a 100%)
    """
    # Asegurar que el valor esté dentro del rango esperado
    valor_limitado = max(valor_min, min(valor_adc, valor_max))
    
    # Convertir a porcentaje INVERSO (valor alto = poca luz = 0%, valor bajo = mucha luz = 100%)
    porcentaje = ((valor_max - valor_limitado) / (valor_max - valor_min)) * 100
    return round(porcentaje)

while True:
    ## Estado 0: Espera potenciómetro > 1100, todo apagado
    while True:
        pot_value = read_analog(pot)
        ldr_value = read_analog(ldr)
        if not sensor.value:  # sensor activado
            led.value = False
        else:
            led.value = True
        inclinado=led.value
        if (pot_value)>2050 or inclinado:
            break
        display_number(0)
        elangulo= angulo_potenciometro(pot_value,1800,62100)
        elporcentaje=intensidad_fotorresistor(ldr_value,0,2000)
        print(f"ángulo potenciómetro: {elangulo}°, porcentaje de luz: {elporcentaje} %, Inclinado: {inclinado}")
        publish()
        laser.duty_cycle = 0
        while usb_cdc.console.in_waiting > 0:
            usb_cdc.console.read(usb_cdc.console.in_waiting)
            print("El sistema está apagado, gire el potenciómetro para programar la temporización")   
        time.sleep(0.5)
        
    while True:
        pot_value = read_analog(pot)
        if not sensor.value:  # sensor activado
            led.value = False
        else:
            led.value = True
        inclinado=led.value
        if not inclinado:
            if (pot_value)<2050:
                break
            vertemporizador()
            if not paratemp["bandera"]:
                # Ajustamos el duty_cycle según potenciómetro y LDR
                # LDR alto (mucha luz) reduce intensidad del láser
                duty = int(pot_value)
                laser.duty_cycle = duty
                time.sleep(0.1)  # Pequeña pausa para estabilizar lectura
                ldr_value = read_analog(ldr)
                if (ldr_value)>700:
                    display_number(2)
                    for n in range (5):
                        beep(440, 0.5)
                        print("alarma activada por láser")        
                else:
                    display_number(1)
            else:
                laser.duty_cycle = 0
        else:
            display_number(4)
            for n in range (5):
                beep(500, 0.2)
                print("alarma activada por forcejeo") 
            if paratemp["bandera"]:
                paratemp["contador"]+=2 # para que siga el conteo del temporizador mientras está inclinado el sensor 
        elangulo= angulo_potenciometro(pot_value,1800,62100)
        elporcentaje=intensidad_fotorresistor(ldr_value,0,2000)
        print(f"ángulo potenciómetro: {elangulo}°, porcentaje de luz: {elporcentaje} %, Inclinado: {inclinado}")
        publish()
        time.sleep(0.5)