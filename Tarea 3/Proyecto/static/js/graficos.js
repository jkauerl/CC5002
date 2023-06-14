// Configuración del gráfico de donaciones
Highcharts.chart("grafico-donaciones", {
    chart: {
        type: 'bar'
    },
    title: {
        text: 'Total de donaciones por tipo'
    },
    xAxis: {
        categories: ['Frutas', 'Verduras', 'Otros']
    },
    yAxis: {
        title: {
        text: 'Total de donaciones'
        }
    },
    series: [{
        name: 'Donaciones',
        data: []
    }]
});
  
// Configuración del gráfico de pedidos
Highcharts.chart("grafico-pedidos", {
    chart: {
        type: 'bar'
    },
    title: {
        text: 'Total de pedidos por tipo'
    },
    xAxis: {
        categories: ['Frutas', 'Verduras', 'Otros']
    },
    yAxis: {
        title: {
        text: 'Total de pedidos'
        }
    },
    series: [{
        name: 'Pedidos',
        data: []
    }]
});

fetch("/get-total")
    .then((response) => response.json())
    .then((data) => {

        donaciones = data[0];
        pedidos = data[1];
        const chartDonaciones = Highcharts.charts.find(
            (chart) => chart && chart.renderTo.id === "grafico-donaciones"
        )

        const chartPedidos = Highcharts.charts.find(
            (chart) => chart && chart.renderTo.id === "grafico-pedidos"
        )

        chartDonaciones.update({
            series: [
                {
                    data: donaciones
                }
            ]
        })

        chartPedidos.update({
            series: [
                {
                    data: pedidos
                }
            ]
        })
    })
.catch((error) => console.error("Error", error))