import requests
import os
from flask.cli import load_dotenv
from urllib.parse import urlparse

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_API_URL = "https://api.github.com"

HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}

def extract_repo_info(repo_url):
    """
    Извлечение username и repository из URL репозитория GitHub.
    :param repo_url: string, URL репозитория GitHub
    :return: tuple (username, repo_name)
    """
    parsed_url = urlparse(repo_url)
    
    # Проверяем, что URL корректен и содержит ожидаемую структуру
    if parsed_url.netloc == "github.com":
        path_parts = parsed_url.path.strip("/").split("/")
        if len(path_parts) == 2:
            username = path_parts[0]
            repo_name = path_parts[1]
            return username, repo_name
    return None, None  # Если URL не соответствует ожидаемой структуре


def get_repo_info(repo_name):
    """
    Получение информации о репозитории на GitHub.
    :param repo_name: string, формат username/repository
    :return: dict с названием, URL, описанием репозитория
    """
    url = f"https://api.github.com/repos/{repo_name}"
    response = requests.get(url)
    
    if response.status_code != 200:
        raise ValueError(f"Не удалось получить информацию о репозитории {repo_name}")
    
    repo_info = response.json()
    
    return {
        "name": repo_info.get("name"),
        "html_url": repo_info.get("html_url"),
        "description": repo_info.get("description")
    }


def search_commits(repo_url, query):
    """
    Поиск коммитов по фразе.
    :param repo_url: string, URL репозитория GitHub
    :param query: string, фраза для поиска
    :return: list с данными о коммитах
    """
    # Разбираем URL репозитория на username и repo_name
    username, repo_name = extract_repo_info(repo_url)
    print("print username, repo_name: ", username, repo_name)
    if not username or not repo_name:
        raise ValueError(f"Неверный URL репозитория: {repo_url}")

    # Создаем запрос для поиска
    url = f"https://api.github.com/search/commits?q={query}+repo:{username}/{repo_name}"
    
    # Выполняем запрос к GitHub API
    response = requests.get(url, headers=HEADERS)
    print(url)

    if response.status_code != 200:
        raise ValueError(f"Ошибка поиска коммитов: {response.json()}")

    commits = []
    for item in response.json().get("items", []):
        commit_data = item["commit"]
        commits.append({
            "html_url": item["html_url"],
            "sha": item["sha"],
            "author_email": commit_data["author"]["email"],
            "date": commit_data["author"]["date"],
            "message": commit_data["message"]
        })
        print("item: ", item)

    return commits


def get_commit_frequency(repo_name, start_date, end_date):
    """
    Получение статистики коммитов за указанный период.
    :param repo_name: string, формат username/repository
    :param start_date: string, начальная дата (YYYY-MM-DD)
    :param end_date: string, конечная дата (YYYY-MM-DD)
    :return: dict с датами и частотой коммитов
    """
    url = f"https://api.github.com/repos/{repo_name}/commits"
    params = {
        "since": f"{start_date}T00:00:00Z",
        "until": f"{end_date}T23:59:59Z"
    }
    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        raise ValueError(f"Не удалось получить коммиты для репозитория {repo_name}")
    
    commits = response.json()
    
    # Группируем коммиты по датам
    commit_dates = {}
    for commit in commits:
        commit_date = commit["commit"]["author"]["date"][:10]  # берем только дату (YYYY-MM-DD)
        if commit_date not in commit_dates:
            commit_dates[commit_date] = 0
        commit_dates[commit_date] += 1
    
    # Подготавливаем данные для возвращения
    dates = sorted(commit_dates.keys())
    frequencies = [commit_dates[date] for date in dates]
    
    return {
        "dates": dates,
        "frequencies": frequencies
    }

