from github import Github
from github.GithubException import UnknownObjectException


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

    def get_repos(self) -> str:
        repos = self.user.get_repos()
        result = ''
        index = 1
        for repo in repos:
            if not repo.archived:
                result += f'{index}. {repo.name}. [Link]({repo.html_url}). ' \
                          f'Total issues and prs: {repo.get_issues().totalCount}\n'
                index += 1
        return result

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

    def get_issues(self) -> str:
        issues = self.user.get_issues()
        result = ''
        for issue in issues:
            if not issue.pull_request:
                result += f'- _{issue.title}_ [#{issue.number}]({issue.html_url}). ' \
                          f'[Link to repository]({issue.repository.html_url}). Created: _{issue.created_at}_. ' \
                          f'Author: _{issue.user.name}_\n'
        return result
