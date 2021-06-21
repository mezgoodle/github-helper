from github import Github
from github.GithubException import UnknownObjectException


class Api:
    def __init__(self, token):
        self.g = Github(token)

    def get_user_info(self) -> str:
        """
        Method that returns string with information about user
        :return: string with information
        """
        user = self.g.get_user()
        return f'You have been authenticated with login *{user.login}* as *{user.name}*'

    def get_repos(self) -> str:
        user = self.g.get_user()
        repos = user.get_repos()
        result = ''
        for repo in repos:
            if not repo.archived:
                result += f'- {repo.name}. [Link]({repo.html_url}). Total issues and prs: {repo.get_issues().totalCount}\n '
        return result

    def get_repo(self, repo_name: str) -> dict:
        user = self.g.get_user()
        try:
            repo = user.get_repo(repo_name)
            return {
                'name': repo.name,
                'url': repo.html_url,
                'stars': repo.stargazers_count,
                'count_of_issues': repo.get_issues().totalCount,
                'issues': repo.get_issues()
            }
        except UnknownObjectException:
            return {}
