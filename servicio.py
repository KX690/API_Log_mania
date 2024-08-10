import time
import requests
import json
import random
from datetime import datetime

SERVICE_NAME = "Servicio1"
LOG_LEVELS = ["INFO", "ERROR", "DEBUG", "WARNING"]

SERVER_URL = "http://localhost:5000/logs"  

def generar_log():
    log = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "nombre_servicio": SERVICE_NAME,
        "nivel_log": random.choice(LOG_LEVELS),  
        "mensaje":  f'Este es un registro (log) de {SERVICE_NAME}'
    }
    return log

def send_log(log):
    headers = {
    "Content-Type": "application/json"
    }
    response = requests.post(SERVER_URL, headers=headers, data=json.dumps(log))

    if response.status_code == 200:
        print("Log enviado correctamente.")
    else:
        print(f"Error al enviar el log: {response.status_code}, {response.text}")

if __name__ == "__main__":
    while True:
        log = generar_log()
        send_log(log)
        time.sleep(10)
