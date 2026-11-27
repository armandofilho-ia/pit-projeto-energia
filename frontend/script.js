const ctx = document.getElementById('powerChart').getContext('2d');
const powerChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: [],
        datasets: [{
            label: 'Consumo de Potência (W)',
            data: [],
            borderColor: '#2563eb',
            backgroundColor: 'rgba(37, 99, 235, 0.1)',
            borderWidth: 3,
            tension: 0.4,
            fill: true,
            pointBackgroundColor: '#10b981',
            pointRadius: 4
        }]
    },
    options: {
        responsive: true,
        scales: {
            y: { beginAtZero: true, suggestedMax: 3 }
        },
        animation: { duration: 400 }
    }
});

const maxDataPoints = 15;

// 10 s = 3 envios perdidos seguidos (o simulador envia a cada 3 s); menos que isso faria o selo piscar à toa
const LIMITE_SEM_DADOS_MS = 10000;
let ultimoTimestamp = null;
// Relógio do navegador, não o do servidor: os dois podem estar com horas diferentes
let momentoUltimaMudanca = null;

function estaSemComunicacao(agora, momentoUltimaMudanca) {
    return momentoUltimaMudanca === null || agora - momentoUltimaMudanca > LIMITE_SEM_DADOS_MS;
}

function atualizarSelo() {
    const semComunicacao = estaSemComunicacao(Date.now(), momentoUltimaMudanca);
    document.getElementById('status-badge').classList.toggle('sem-comunicacao', semComunicacao);
    document.getElementById('status-texto').innerText = semComunicacao ? 'Sem comunicação' : 'Recebendo Dados';
}

async function buscarDados() {
    try {
        const response = await fetch('http://localhost:8000/api/readings/latest');
        const data = await response.json();

        if (data.status !== "vazio") {
            document.getElementById('voltage').innerHTML = `${data.voltage_v.toFixed(2)} <span>V</span>`;
            document.getElementById('current').innerHTML = `${data.current_a.toFixed(2)} <span>A</span>`;
            document.getElementById('power').innerHTML = `${data.power_w.toFixed(4)} <span>W</span>`;
            document.getElementById('energy').innerHTML = `${data.energy_wh.toFixed(4)} <span>Wh</span>`;

            let horaLeitura = data.timestamp.split(" ")[1];
            document.getElementById('time').innerText = data.timestamp;

            // A primeira leitura não conta: ao abrir o painel ela pode ser antiga (de ontem, por exemplo)
            // Fica depois dos toFixed: uma leitura que quebra o painel não pode deixar o selo verde
            if (ultimoTimestamp !== null && data.timestamp !== ultimoTimestamp) {
                momentoUltimaMudanca = Date.now();
            }
            ultimoTimestamp = data.timestamp;

            if(powerChart.data.labels.length > 0 && powerChart.data.labels[powerChart.data.labels.length-1] === horaLeitura) {
                return; 
            }

            powerChart.data.labels.push(horaLeitura);
            powerChart.data.datasets[0].data.push(data.power_w);

            if (powerChart.data.labels.length > maxDataPoints) {
                powerChart.data.labels.shift();
                powerChart.data.datasets[0].data.shift();
            }
            powerChart.update();
        }
    } catch (error) {
        console.error("Erro na comunicação:", error);
    } finally {
        // finally: roda também no return antecipado e no erro, quando o selo mais precisa mudar
        atualizarSelo();
    }
}

setInterval(buscarDados, 3000); 
buscarDados();
