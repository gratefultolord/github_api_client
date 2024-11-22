document.addEventListener("DOMContentLoaded", () => {
    const labels = JSON.parse(document.getElementById("commitChart").dataset.labels);
    const data = JSON.parse(document.getElementById("commitChart").dataset.data);

    const ctx = document.getElementById('commitChart').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Частота коммитов',
                data: data,
                borderColor: 'rgb(75, 192, 192)',
                tension: 0.1
            }]
        },
        options: {
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Дата'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Кол-во коммитов'
                    }
                }
            }
        }
    });
});


