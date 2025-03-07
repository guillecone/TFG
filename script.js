document.addEventListener('DOMContentLoaded', () => {
    fetch('http://127.0.0.1:5000/nuevos_pacientes')
        .then(response => response.json())
        .then(data => {
            console.log("Datos de nuevos pacientes:", data); // 🔹 Verificar datos en consola
            
            const fechas = data.map(item => item.fecha); // Extraer fechas
            const pacientes = data.map(item => item.total_pacientes); // Extraer cantidad de pacientes

            const ctx = document.getElementById('chart-nuevos-pacientes').getContext('2d');

            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: fechas,
                    datasets: [{
                        label: 'Nuevos Pacientes',
                        data: pacientes,
                        borderColor: 'rgba(54, 162, 235, 1)',
                        backgroundColor: 'rgba(54, 162, 235, 0.2)',
                        borderWidth: 2,
                        tension: 0.3,
                        fill: true,
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: { display: true },
                        title: {
                            display: true,
                            text: 'Número de Nuevos Pacientes por Día'
                        }
                    },
                    scales: {
                        x: { title: { display: true, text: 'Fecha' } },
                        y: { title: { display: true, text: 'Cantidad de Pacientes' }, beginAtZero: true }
                    }
                }
            });
        })
        .catch(error => console.error('Error al cargar nuevos pacientes:', error));
});
