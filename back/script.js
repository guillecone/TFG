document.addEventListener('DOMContentLoaded', () => {

    // Citas por Doctores
    fetch('http://127.0.0.1:5000/citas_por_doctores')
        .then(response => response.json())
        .then(data => {
            if (data.length === 0) {
                console.warn("No hay datos para citas por doctores.");
                return;
            }

            const ctx = document.getElementById('chart-citas').getContext('2d');
            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: data.map(d => d.doctor),
                    datasets: [{
                        label: 'Citas',
                        data: data.map(d => d.total_citas),
                        backgroundColor: 'rgba(54, 162, 235, 0.6)',
                        borderColor: 'rgba(54, 162, 235, 1)',
                        borderWidth: 1
                    }]
                }
            });
        })
        .catch(error => console.error('Error al cargar las citas por doctores:', error));

    // Pacientes por Tratamientos
    fetch('http://127.0.0.1:5000/pacientes_por_tratamientos')
        .then(response => response.json())
        .then(data => {
            if (data.length === 0) {
                console.warn("No hay datos para pacientes por tratamientos.");
                return;
            }

            const ctx = document.getElementById('chart-tratamientos').getContext('2d');
            new Chart(ctx, {
                type: 'pie',
                data: {
                    labels: data.map(d => d.tratamiento),
                    datasets: [{
                        data: data.map(d => d.total_pacientes),
                        backgroundColor: ['red', 'blue', 'green', 'orange', 'purple']
                    }]
                }
            });
        })
        .catch(error => console.error('Error al cargar los pacientes por tratamientos:', error));
});
