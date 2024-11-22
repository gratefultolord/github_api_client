// Функция для получения данных о коммитах с GitHub
async function getCommitsData(owner, repo) {
    const url = `https://api.github.com/repos/${owner}/${repo}/commits`;
    const response = await fetch(url);
    const commits = await response.json();
    console.log(commits);
    return commits;
}

// Функция для подсчета коммитов по датам
function aggregateCommitsByDate(commits) {
    const commitCounts = {};

    commits.forEach(commit => {
        const commitDate = new Date(commit.committer.date);
        const day = commitDate.toISOString().split('T')[0]; // "YYYY-MM-DD"

        if (commitCounts[day]) {
            commitCounts[day]++;
        } else {
            commitCounts[day] = 1;
        }
    });

    return commitCounts;
}

// Функция для подготовки данных для графика
function prepareChartData(commitCounts) {
    const labels = [];
    const data = [];

    for (const [date, count] of Object.entries(commitCounts)) {
        labels.push(date);
        data.push(count);
    }

    return { labels, data };
}

// Функция для построения графика с использованием Chart.js
async function renderCommitChart(owner, repo) {
    const commits = await getCommitsData(owner, repo);
    const commitCounts = aggregateCommitsByDate(commits);
    const { labels, data } = prepareChartData(commitCounts);

    const ctx = document.getElementById('commitChart').getContext('2d');

    const commitChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Коммиты',
                data: data,
                borderColor: 'rgba(75, 192, 192, 1)',
                fill: false
            }]
        },
        options: {
            scales: {
                x: {
                    type: 'time',
                    time: {
                        unit: 'day'
                    }
                }
            }
        }
    });
}

// Вызов функции для построения графика на странице
renderCommitChart('username', 'repository'); // Замените 'username' и 'repository' на реальные данные
