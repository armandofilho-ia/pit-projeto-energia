// Lógica de Navegação e Menu Inferior
function navegar(telaId, indexMenu = -1) {
    // Oculta todas as telas e exibe a solicitada
    document.querySelectorAll('.view').forEach(el => el.classList.remove('active'));
    document.getElementById(telaId).classList.add('active');

    const menu = document.getElementById('bottom-menu');
    const navItems = document.querySelectorAll('.nav-item');

    // Verifica se a tela pertence às áreas logadas para mostrar o menu
    if (['view-dashboard', 'view-historico', 'view-alertas', 'view-ajustes'].includes(telaId)) {
        menu.style.display = 'flex';
        // Atualiza a cor do ícone selecionado
        if(indexMenu >= 0) {
            navItems.forEach(el => el.classList.remove('active'));
            navItems[indexMenu].classList.add('active');
        }
    } else {
        menu.style.display = 'none'; // Esconde menu no Login/Cadastro
    }
}

// Gráfico do Dashboard (Ao Vivo)
const ctxDash = document.getElementById('mobPowerChart').getContext('2d');
const mobPowerChart = new Chart(ctxDash, {
    type: 'line',
    data: {
        labels: ['10:00', '10:01', '10:02', '10:03', '10:04', '10:05'],
        datasets: [{
            label: 'Potência', data: [85, 90, 88, 95, 99, 92],
            borderColor: '#2563eb', backgroundColor: 'rgba(37, 99, 235, 0.1)',
            borderWidth: 2, tension: 0.4, fill: true, pointRadius: 0
        }]
    },
    options: {
        responsive: true, plugins: { legend: { display: false } },
        scales: { x: { grid: { display: false } }, y: { border: { display: false } } }
    }
});

// Gráfico Estático da Tela Histórico
const ctxHist = document.getElementById('historyChart').getContext('2d');
new Chart(ctxHist, {
    type: 'bar',
    data: {
        labels: ['Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb', 'Dom'],
        datasets: [{
            label: 'kWh', data: [4.2, 3.8, 4.5, 4.0, 5.1, 6.2, 5.8],
            backgroundColor: '#10b981', borderRadius: 5
        }]
    },
    options: {
        responsive: true, plugins: { legend: { display: false } },
        scales: { x: { grid: { display: false } } }
    }
});

// Simulação do sensor (Ao Vivo)
setInterval(() => {
    const newVal = 85 + Math.random() * 20;
    mobPowerChart.data.labels.push('');
    mobPowerChart.data.datasets[0].data.push(newVal);
    if(mobPowerChart.data.labels.length > 10) {
        mobPowerChart.data.labels.shift();
        mobPowerChart.data.datasets[0].data.shift();
    }
    mobPowerChart.update();

    if(document.getElementById('view-dashboard').classList.contains('active')){
        document.getElementById('mob-voltage').innerHTML = `${(219 + Math.random() * 2).toFixed(1)}<span>V</span>`;
        document.getElementById('mob-current').innerHTML = `${(0.40 + Math.random() * 0.1).toFixed(2)}<span>A</span>`;
        document.getElementById('mob-power').innerHTML = `${newVal.toFixed(1)}<span>W</span>`;
    }
}, 3000);
