from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask.cli import load_dotenv

from client.github_client import GitHubClient
import os
from pathlib import Path

# Загрузка переменных из .env
load_dotenv()

# Инициализация Flask приложения
app = Flask(__name__)
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


@app.route("/repo-info", methods=["POST"])
def repo_info():
    """
    Получение информации о репозитории.
    """
    repo_name = request.form.get("repo_name")  # Получаем репозиторий из параметра URL
    if not repo_name:
        return jsonify({"error":"Необходимо указать названия репозитория"})  # Если не указан репозиторий, показываем ошибку

    client = GitHubClient(repo_name)
    data = client.get_repository_info()

    if data.get("error"):
        return jsonify({"error":data["error"]}), 400
    return render_template("repo_info.html", repo_name=repo_name, data=data)


@app.route("/search-commits", methods=["POST"])
def search_commits():
    """
    Поиск коммитов по фразе.
    """
    repo_name = request.form.get("repo_name", DEFAULT_REPO)
    query = request.form.get("query", "")
    client = GitHubClient(repo_name)
    commits = client.search_repository_commits(query)
    return render_template(
        "search_commits.html",
        repo_name=repo_name,
        query=query,
        commits=commits)


@app.route("/commit-stats", methods=["POST"])
def commit_stats():
    """
    Построение статистики коммитов за интервал времени.
    """
    repo_name = request.form.get("repo_name", DEFAULT_REPO)
    start_date = request.form.get("start_date", "2024-01-01")
    end_date = request.form.get("end_date", "2024-12-31")
    client = GitHubClient(repo_name)
    stats = client.get_commit_statistics(start_date, end_date)

    if "error" in stats:
        return jsonify({"error": stats["error"]}), 400

    # Передаем данные для визуализации на графике
    return render_template(
        "commit_stats.html",
        repo_name=repo_name,
        start_date=start_date,
        end_date=end_date,
        stats=stats
    )


if __name__ == "__main__":
    # Запуск приложения
    app.run(debug=True, host="0.0.0.0", port=5000)
