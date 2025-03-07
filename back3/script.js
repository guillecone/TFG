document.addEventListener('DOMContentLoaded', () => {

    // Cargar datos de la API
    function fetchData(endpoint, elementId) {
        fetch(`http://127.0.0.1:5000/${endpoint}`)
            .then(response => response.json())
            .then(data => {
                console.log(endpoint, data);
                document.getElementById(elementId).textContent = data.length;
            })
            .catch(error => console.error(`Error al cargar ${endpoint}:`, error));
    }

    // Llamadas a la API
    fetchData('clinicas', 'total-clinicas');
    fetchData('pacientes', 'total-pacientes');
    fetchData('doctores', 'total-doctores');
    fetchData('citas', 'total-citas');
    fetchData('empleados', 'total-empleados');
    fetchData('material_dental', 'total-material');
    fetchData('medicamentos', 'total-medicamentos');
    fetchData('proveedores_dentales', 'total-proveedores');

});

document.addEventListener('DOMContentLoaded', () => {
    fetch('http://127.0.0.1:5000/citas_por_doctores')
        .then(response => response.json())
        .then(data => {
            console.log("Citas por Doctores:", data);
            const ctx = document.getElementById('chart-citas').getContext('2d');
            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: data.map(item => item.doctor),
                    datasets: [{
                        label: 'Citas',
                        data: data.map(item => item.total_citas),
                        backgroundColor: 'rgba(54, 162, 235, 0.6)'
                    }]
                }
            });
        })
        .catch(error => console.error('Error al cargar citas por doctores:', error));
});

document.addEventListener('DOMContentLoaded', () => {
    fetch('http://127.0.0.1:5000/pacientes_por_tratamientos')
        .then(response => response.json())
        .then(data => {
            console.log("Pacientes por Tratamientos:", data);
            const ctx = document.getElementById('chart-tratamientos').getContext('2d');
            new Chart(ctx, {
                type: 'pie',
                data: {
                    labels: data.map(item => item.tratamiento),
                    datasets: [{
                        label: 'Pacientes',
                        data: data.map(item => item.total_pacientes),
                        backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56']
                    }]
                }
            });
        })
        .catch(error => console.error('Error al cargar pacientes por tratamientos:', error));
});

document.addEventListener('DOMContentLoaded', () => {
    fetch('http://127.0.0.1:5000/citas')
        .then(response => response.json())
        .then(data => {
            console.log("Citas:", data); // 🔹 Ver datos en consola
            const listaCitas = document.getElementById('lista-citas');
            listaCitas.innerHTML = '';

            data.forEach(cita => {
                const li = document.createElement('li');
                li.textContent = `📅 ${cita.fecha_hora} - Paciente: ${cita.id_paciente} - Motivo: ${cita.motivo}`;
                listaCitas.appendChild(li);
            });
        })
        .catch(error => console.error('Error al cargar las citas:', error));
});

document.addEventListener('DOMContentLoaded', () => {
    fetch('http://127.0.0.1:5000/pacientes')
        .then(response => response.json())
        .then(data => {
            console.log("Pacientes:", data); // 🔹 Ver datos en consola
            const listaPacientes = document.getElementById('lista-pacientes');
            listaPacientes.innerHTML = '';

            data.forEach(paciente => {
                const li = document.createElement('li');
                li.textContent = `🧑 ${paciente.nombre} - DNI: ${paciente.dni} - Tel: ${paciente.telefono}`;
                listaPacientes.appendChild(li);
            });
        })
        .catch(error => console.error('Error al cargar los pacientes:', error));
});

document.addEventListener('DOMContentLoaded', async () => {
    // 🔹 Función para obtener datos desde la API
    async function fetchData(endpoint) {
        try {
            const response = await fetch(`http://127.0.0.1:5000/${endpoint}`);
            const data = await response.json();
            return data;
        } catch (error) {
            console.error(`Error al cargar ${endpoint}:`, error);
            return [];
        }
    }

    // 🔹 Obtener datos
    const pacientesMedicamentos = await fetchData('pacientes_medicamentos');
    const tratamientosMedicamentos = await fetchData('tratamientos_medicamentos');

    // 📊 Gráfico: Medicamentos por Paciente
    const pacientesMedicamentosChart = new Chart(document.getElementById('chart-pacientes-medicamentos').getContext('2d'), {
        type: 'bar',
        data: {
            labels: pacientesMedicamentos.map(item => `Paciente ${item.id_paciente}`),
            datasets: [{
                label: 'Cantidad de Medicamentos',
                data: pacientesMedicamentos.map(item => item.id_medicamento),
                backgroundColor: 'rgba(54, 162, 235, 0.6)'
            }]
        }
    });

    // 📊 Gráfico: Medicamentos por Tratamiento
    const tratamientosMedicamentosChart = new Chart(document.getElementById('chart-tratamientos-medicamentos').getContext('2d'), {
        type: 'pie',
        data: {
            labels: tratamientosMedicamentos.map(item => `Tratamiento ${item.id_tratamiento}`),
            datasets: [{
                data: tratamientosMedicamentos.map(item => item.id_medicamento),
                backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4CAF50', '#FF9F40']
            }]
        }
    });

    // 📋 Tabla: Medicamentos por Pacientes
    const tablaPacientesMedicamentos = document.getElementById('tabla-pacientes-medicamentos');
    pacientesMedicamentos.forEach(item => {
        const row = document.createElement('tr');
        row.innerHTML = `<td>Paciente ${item.id_paciente}</td><td>Medicamento ${item.id_medicamento}</td>`;
        tablaPacientesMedicamentos.appendChild(row);
    });

    // 📋 Tabla: Medicamentos por Tratamientos
    const tablaTratamientosMedicamentos = document.getElementById('tabla-tratamientos-medicamentos');
    tratamientosMedicamentos.forEach(item => {
        const row = document.createElement('tr');
        row.innerHTML = `<td>Tratamiento ${item.id_tratamiento}</td><td>Medicamento ${item.id_medicamento}</td>`;
        tablaTratamientosMedicamentos.appendChild(row);
    });
});

document.addEventListener('DOMContentLoaded', () => {
    fetch('http://127.0.0.1:5000/pacientes_nuevos_recurrentes')
        .then(response => response.json())
        .then(data => {
            const ctx = document.getElementById('chart-pacientes').getContext('2d');
            new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels: ['Nuevos', 'Recurrentes'],
                    datasets: [{
                        data: [data[0].nuevos, data[0].recurrentes],
                        backgroundColor: ['#FF6384', '#36A2EB']
                    }]
                }
            });
        })
        .catch(error => console.error('Error al cargar pacientes nuevos vs recurrentes:', error));
});

document.addEventListener('DOMContentLoaded', () => {
    fetch('http://127.0.0.1:5000/facturacion_por_clinica')
        .then(response => response.json())
        .then(data => {
            const ctx = document.getElementById('chart-facturacion').getContext('2d');
            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: data.map(item => item.clinica),
                    datasets: [{
                        label: 'Facturación (€)',
                        data: data.map(item => item.total_facturado),
                        backgroundColor: '#36A2EB'
                    }]
                }
            });
        })
        .catch(error => console.error('Error al cargar la facturación por clínica:', error));
});
