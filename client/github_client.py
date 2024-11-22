from .utils import get_repo_info, search_commits, get_commit_frequency


class GitHubClient:
    """
    Клиент для работы с GitHub API.
    """

    def __init__(self, repo_name):
        """
        Инициализация клиента с указанным репозиторием.
        :param repo_name: string, формат username/repository
        """
        self.repo_name = repo_name

    def get_repository_info(self):
        """
        Получение информации о репозитории.
        :return: dict с названием, URL и описанием
        """
        try:
            return get_repo_info(self.repo_name)
        except ValueError as e:
            return {"error": str(e)}

    def search_repository_commits(self, query):
        """
        Поиск коммитов по фразе.
        :param query: string, фраза для поиска
        :return: list с данными о коммитах
        """
        try:
            return search_commits(self.repo_name, query)
        except ValueError as e:
            return {"error": str(e)}

    def get_commit_statistics(self, start_date, end_date):
        """
        Получение статистики частоты коммитов за указанный интервал.
        :param start_date: string, начальная дата (YYYY-MM-DD)
        :param end_date: string, конечная дата (YYYY-MM-DD)
        :return: dict {"dates": [даты], "frequencies": [кол-во коммитов]}
        """
        try:
            return get_commit_frequency(self.repo_name, start_date, end_date)
        except ValueError as e:
            return {"error": str(e)}
