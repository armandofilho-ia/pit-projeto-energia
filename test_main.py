# Instalação: pip install pytest httpx
# Rodar: python -m pytest -v
import json

import pytest
from fastapi.testclient import TestClient

# shortcut: importar o main roda init_db() no banco real (cria um medicoes.db vazio, ignorado pelo Git); mover init_db para o startup se isso incomodar
import main

LEITURA_VALIDA = {
    "device_id": "esp32_teste",
    "voltage_v": 5.02,
    "current_a": 0.3,
    "power_w": 1.506,
    "energy_wh": 0.01,
}


@pytest.fixture
def cliente(tmp_path, monkeypatch):
    # Banco temporário: os testes nunca tocam no medicoes.db de verdade
    monkeypatch.setattr(main, "CAMINHO_BANCO", tmp_path / "teste.db")
    main.init_db()
    return TestClient(main.app)


def test_grava_leitura_valida(cliente):
    resposta = cliente.post("/api/readings", json=LEITURA_VALIDA)
    assert resposta.status_code == 200

    ultima = cliente.get("/api/readings/latest").json()
    for campo, valor in LEITURA_VALIDA.items():
        assert ultima[campo] == valor


def test_latest_banco_vazio(cliente):
    assert cliente.get("/api/readings/latest").json() == {"status": "vazio"}


def test_latest_devolve_a_ultima(cliente):
    cliente.post("/api/readings", json=LEITURA_VALIDA)
    cliente.post("/api/readings", json={**LEITURA_VALIDA, "current_a": 0.45})

    assert cliente.get("/api/readings/latest").json()["current_a"] == 0.45


@pytest.mark.parametrize("campo, valor", [("current_a", -99), ("voltage_v", 1e9)])
def test_recusa_valor_fora_do_limite(cliente, campo, valor):
    resposta = cliente.post("/api/readings", json={**LEITURA_VALIDA, campo: valor})
    assert resposta.status_code == 422


def test_recusa_nan(cliente):
    # O json= do httpx recusa NaN antes de enviar; o ESP32 pode mandar, então o corpo vai como texto
    corpo = json.dumps({**LEITURA_VALIDA, "voltage_v": float("nan")})
    resposta = cliente.post(
        "/api/readings", content=corpo, headers={"content-type": "application/json"}
    )
    assert resposta.status_code == 422


def test_recusa_campo_faltando(cliente):
    leitura = {**LEITURA_VALIDA}
    del leitura["current_a"]
    assert cliente.post("/api/readings", json=leitura).status_code == 422
