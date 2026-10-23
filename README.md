# ENERGIA - Sistema Inteligente de Monitoramento e Análise do Consumo de Energia Elétrica

## Sobre o Projeto
Este projeto, desenvolvido como parte do Projeto Integrador I do Piauí Instituto de Tecnologia (PIT), consiste em um sistema MVP (Minimum Viable Product) focado no controle e na tomada de decisão do consumidor por meio da análise de dados históricos de consumo de energia elétrica, não se limitando à premissa básica de "vender economia de energia".

O sistema simula a coleta de parâmetros elétricos de um dispositivo IoT (ESP32) e os transmite para uma API backend. Os dados são armazenados e consumidos em tempo real por um dashboard web interativo, permitindo a visualização da curva de potência e dos indicadores acumulados.

## Arquitetura do Sistema
- **Simulador de Hardware (Python):** Script que atua no lugar do microcontrolador físico durante o MVP, gerando dados estocásticos de tensão, corrente, potência e energia acumulada.
- **Backend (FastAPI & SQLite):** API de alta performance que recebe as cargas de dados via POST e gerencia a persistência no banco de dados relacional.
- **Frontend (HTML/JS):** Dashboard assíncrono que consome a API (GET) para exibir cartões de status dinâmicos e um gráfico em tempo real.

## Tecnologias Utilizadas
- **Backend:** Python, FastAPI, Uvicorn, Pydantic
- **Banco de Dados:** SQLite
- **Simulação IoT:** Python (Requests)
- **Frontend:** HTML5, CSS3, JavaScript, Chart.js, FontAwesome

## Como Executar o Projeto Localmente

**1. Clone o repositório e configure o ambiente**
```bash
git clone [https://github.com/seu-usuario/pit-projeto-energia.git](https://github.com/seu-usuario/pit-projeto-energia.git)
cd pit-projeto-energia
python -m venv venv
# No Windows:
venv\Scripts\activate
# Instale as dependências:
pip install fastapi uvicorn requests