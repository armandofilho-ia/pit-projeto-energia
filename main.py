from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from datetime import datetime
import sqlite3
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Caminho fixo ao lado do main.py: assim o banco é o mesmo, seja qual for a pasta onde o uvicorn é iniciado
CAMINHO_BANCO = Path(__file__).parent / "medicoes.db"

# Permite que o painel web (HTML) acesse a API sem bloqueios do navegador
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializa o banco de dados SQLite
def init_db():
    conn = sqlite3.connect(CAMINHO_BANCO)
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
    voltage_v: float = Field(ge=0, le=26, allow_inf_nan=False)
    current_a: float = Field(ge=0, le=3.2, allow_inf_nan=False)
    power_w: float = Field(allow_inf_nan=False)
    energy_wh: float = Field(allow_inf_nan=False)

@app.exception_handler(RequestValidationError)
async def erro_de_validacao(request: Request, exc: RequestValidationError):
    # não devolve o valor recebido: NaN não pode ser convertido para JSON
    erros = [{"loc": e["loc"], "msg": e["msg"]} for e in exc.errors()]
    return JSONResponse(status_code=422, content={"detail": erros})

@app.post("/api/readings")
def receber_leitura(leitura: Leitura):
    conn = sqlite3.connect(CAMINHO_BANCO)
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
    conn = sqlite3.connect(CAMINHO_BANCO)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM leituras ORDER BY id DESC LIMIT 1')
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return dict(row)
    return {"status": "vazio"}