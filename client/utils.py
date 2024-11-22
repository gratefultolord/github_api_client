import requests
import os
from flask.cli import load_dotenv
from collections import defaultdict

# Загрузка переменных из .env
load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_API_URL = "https://api.github.com"

HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}


def get_repo_info(repo_name):
    """
    Получение информации о репозитории.
    :param repo_name: string, формат username/repository
    :return: dict с названием, URL и описанием
    """
    url = f"{GITHUB_API_URL}/repos/{repo_name}"
    response = requests.get(url, headers=HEADERS)

    if response.status_code != 200:
        raise ValueError(
            f"Не удалось получить информацию о репозитории: {response.json()}")

    repo_data = response.json()
    return {
        "name": repo_data.get("name"),
        "html_url": repo_data.get("html_url"),
        "description": repo_data.get("description", "Нет описания")
    }


def search_commits(repo_name, query):
    """
    Поиск коммитов по фразе.
    :param repo_name: string, формат username/repository
    :param query: string, фраза для поиска
    :return: list с данными о коммитах
    """
    url = f"{GITHUB_API_URL}/search/commits"
    params = {
        "q": f"{query}+repo:{repo_name}"
    }
    headers = HEADERS.copy()
    headers["Accept"] = "application/vnd.github.cloak-preview"

    response = requests.get(url, headers=headers, params=params)

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

    return commits


def get_commit_frequency(repo_name, start_date, end_date):
    """
    Подсчет частоты коммитов за заданный период.
    :param repo_name: string, формат username/repository
    :param start_date: string, начальная дата (YYYY-MM-DD)
    :param end_date: string, конечная дата (YYYY-MM-DD)
    :return: dict {"dates": [даты], "frequencies": [кол-во коммитов]}
    """
    url = f"{GITHUB_API_URL}/repos/{repo_name}/commits"
    params = {
        "since": f"{start_date}T00:00:00Z",
        "until": f"{end_date}T23:59:59Z"
    }

    response = requests.get(url, headers=HEADERS, params=params)

    if response.status_code != 200:
        raise ValueError(f"Ошибка получения коммитов: {response.json()}")

    commit_data = response.json()
    frequency = defaultdict(int)

    for commit in commit_data:
        date = commit["commit"]["author"]["date"][:10]
        frequency[date] += 1

    sorted_dates = sorted(frequency.keys())
    return {
        "dates": sorted_dates,
        "frequencies": [frequency[date] for date in sorted_dates]
    }
