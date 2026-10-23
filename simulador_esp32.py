import requests
import time
import random

url = "http://localhost:8000/api/readings"
energy_wh = 0.0

print("Iniciando simulação da carga elétrica...")

while True:
    voltage = 5.02
    current = random.uniform(0.10, 0.50)
    power = voltage * current
    energy_wh += power * (3 / 3600.0)

    payload = {
        "device_id": "esp32_python",
        "voltage_v": round(voltage, 2),
        "current_a": round(current, 2),
        "power_w": round(power, 4),
        "energy_wh": round(energy_wh, 6)
    }

    try:
        resposta = requests.post(url, json=payload)
        print(f"Enviado: {payload} | Status: {resposta.status_code}")
    except Exception as e:
        print(f"Erro de conexão: {e}")

    time.sleep(3)
    