from github import Github
from github.GithubException import UnknownObjectException
from github.PaginatedList import PaginatedList


class Api:
    def __init__(self, token):
        self.g = Github(token)
        self.user = self.g.get_user()

    def get_user_info(self) -> str:
        """
        Method that returns string with information about user
        :return: string with information
        """
        return f'You have been authenticated with login *{self.user.login}* as *{self.user.name}*'

    def get_repos(self) -> PaginatedList:
        repos = self.user.get_repos()
        return repos

    def get_repo(self, repo_name: str) -> dict:
        try:
            repo = self.user.get_repo(repo_name)
            return {
                'name': repo.name,
                'url': repo.html_url,
                'stars': repo.stargazers_count,
                'count_of_issues': repo.get_issues().totalCount,
                'issues': repo.get_issues()
            }
        except UnknownObjectException:
            return {}

    def get_issues_or_prs(self, option: bool) -> list:
        items = self.user.get_issues()
        result = []
        for item in items:
            if (item.pull_request is None) == option:
                result.append(item)
        return result
