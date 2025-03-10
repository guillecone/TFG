const apiBaseUrl = "http://localhost:5000/api";

// Función para obtener datos y crear gráficos
async function fetchData(endpoint, chartId, chartType, labelText, color) {
    try {
        const response = await fetch(`${apiBaseUrl}/${endpoint}`);
        if (!response.ok) throw new Error(`Error en API: ${response.status}`);

        const data = await response.json();
        console.log(`📊 Datos recibidos de ${endpoint}:`, data); // 👈 Verifica los datos en la consola

        if (data.length === 0) {
            console.warn(`⚠ No hay datos disponibles para ${endpoint}.`);
            return;
        }

        const labels = data.map(item => item.dia || item.nombre_tratamiento || item.tipo_costo || item.nombre + " " + item.apellido || item.estado || item.hora + ":00");
        const values = data.map(item => item.nuevos_pacientes || item.cantidad_realizada || item.total_gasto || item.consultas_realizadas || item.cantidad || item.cantidad_citas);

        new Chart(document.getElementById(chartId), {
            type: chartType,
            data: {
                labels: labels,
                datasets: [{
                    label: labelText,
                    data: values,
                    backgroundColor: color,
                    borderColor: color,
                    borderWidth: 2,
                    fill: chartType === "line" ? false : true
                }]
            }
        });

    } catch (error) {
        console.error(`❌ Error al cargar ${endpoint}:`, error);
    }
}


// Cargar gráficos al iniciar
function cargarDashboard() {
    fetchData("nuevos_pacientes", "nuevosPacientesChart", "line", "Nuevos Pacientes", "blue");
    fetchData("tratamientos_realizados", "tratamientosChart", "bar", "Tratamientos Realizados", "green");
    fetchData("costos_operativos", "costosChart", "line", "Costos Operativos", "orange");
    fetchData("consultas_por_dentista", "consultasChart", "bar", "Consultas por Dentista", "purple");
    fetchData("nivel_stock", "stockChart", "bar", "Nivel de Stock", "red");
    fetchData("ingresos_por_tratamiento", "ingresosChart", "bar", "Ingresos por Tratamiento", "blue");
}

window.onload = cargarDashboard;
