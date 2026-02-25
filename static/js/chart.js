function createChart(temp, vib, press) {

    const ctx = document
        .getElementById('machineChart')
        .getContext('2d');

    new Chart(ctx, {

        type: 'bar',

        data: {

            labels: [
                'Temperature',
                'Vibration',
                'Pressure'
            ],

            datasets: [{

                label: 'Machine Parameters',

                data: [
                    temp,
                    vib,
                    press
                ],

                backgroundColor: [

                    '#00f5ff',
                    '#00ff95',
                    '#ff4b5c'

                ]

            }]
        },

        options: {

            responsive: true,

            plugins: {

                legend: {

                    labels: {

                        color: 'white'

                    }
                }
            },

            scales: {

                y: {

                    ticks: {

                        color: 'white'

                    }
                },

                x: {

                    ticks: {

                        color: 'white'

                    }
                }
            }
        }
    });
}