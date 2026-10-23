from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
import sqlite3
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Permite que o painel web (HTML) acesse a API sem bloqueios do navegador
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializa o banco de dados SQLite
def init_db():
    conn = sqlite3.connect("medicoes.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS leituras (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            device_id TEXT,
            timestamp TEXT,
            voltage_v REAL,
            current_a REAL,
            power_w REAL,
            energy_wh REAL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Define o formato dos dados que o ESP32 vai enviar
class Leitura(BaseModel):
    device_id: str
    voltage_v: float
    current_a: float
    power_w: float
    energy_wh: float

@app.post("/api/readings")
def receber_leitura(leitura: Leitura):
    conn = sqlite3.connect("medicoes.db")
    cursor = conn.cursor()
    agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    cursor.execute('''
        INSERT INTO leituras (device_id, timestamp, voltage_v, current_a, power_w, energy_wh)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (leitura.device_id, agora, leitura.voltage_v, leitura.current_a, leitura.power_w, leitura.energy_wh))
    
    conn.commit()
    conn.close()
    return {"status": "sucesso"}

@app.get("/api/readings/latest")
def obter_ultima_leitura():
    conn = sqlite3.connect("medicoes.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM leituras ORDER BY id DESC LIMIT 1')
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return dict(row)
    return {"status": "vazio"}