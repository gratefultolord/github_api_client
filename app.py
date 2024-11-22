from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask.cli import load_dotenv
import requests

from client.github_client import GitHubClient
import os
from pathlib import Path

# Загрузка переменных из .env
load_dotenv()

# Инициализация Flask приложения
app = Flask(__name__, static_folder='static', static_url_path='/static')
os.chdir(Path(__file__).parent)
DEFAULT_REPO = os.getenv("DEFAULT_REPO", "octocat/Hello-World")


@app.route("/", methods=["GET", "POST"])
def index():
    """
    Главная страница с формой для ввода репозитория.
    """
    if request.method == "POST":
        repo_name = request.form.get("repo_name")  # Получаем репозиторий из формы
        if not repo_name:
            return "Пожалуйста, укажите репозиторий.", 400  # Если не указан репозиторий, показываем ошибку

        # Перенаправляем на страницу с информацией о репозитории
        return redirect(url_for('repo_info', repo_name=repo_name))

    return render_template("index.html")  # Страница с формой для ввода репозитория


@app.route("/repo-info", methods=["GET", "POST"])
def repo_info():
    """
    Получение информации о репозитории.
    """
    repo_name = request.form.get("repo_name")  # Получаем repo_name из URL (параметры запроса)
    print(f"repo_name: {repo_name}")
    if not repo_name:
        return jsonify({"error":"Необходимо указать название репозитория"}), 400

    client = GitHubClient(repo_name)
    data = client.get_repository_info()

    if data.get("error"):
        return jsonify({"error": data["error"]}), 400
    
    return render_template("repo_info.html", repo_name=repo_name, data=data)


@app.route("/search-commits", methods=["POST"])
def search_commits():
    """
    Поиск коммитов по фразе.
    """
    full_repo_name = request.form.get("repo_name")
    
    query = request.form.get("commit_message", "")
    
    # Проверка на корректность
    if "/" not in full_repo_name:
        return render_template("repo_info.html", data={"error": "Неверный формат репозитория"})
    
    user_name, repo_name = full_repo_name.split("/", 1)
    
    client = GitHubClient(full_repo_name)  # Передаем полный репозиторий
    commits = client.search_repository_commits(query)
    
    return render_template(
        "search_commits.html",
        repo_name=repo_name,
        query=query,
        commits=commits)


@app.route('/commit-stats', methods=['GET', 'POST'])
def commit_stats():
    repo_owner = request.form.get('repo_owner')
    repo_name = request.form.get('repo_name')

    response = requests.get(f"https://api.github.com/repos/{repo_owner}/{repo_name}/commits")
    
    if response.status_code == 200:
        commits = response.json()
        print(f"Полученные коммиты: {commits}")  # Логируем данные
    else:
        commits = []
        print(f"Ошибка получения коммитов: {response.status_code} - {response.json()}")  # Логируем ошибку

    return render_template('commit_stats.html', commits=commits, repo_name=repo_name)


if __name__ == "__main__":
    # Запуск приложения
    app.run(debug=True, host="0.0.0.0", port=5000)
