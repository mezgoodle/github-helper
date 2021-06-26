# TODO: Add docstrings
# TODO: Add tests
from github import Github
from github.GithubException import UnknownObjectException
from github.Issue import Issue
from github.PaginatedList import PaginatedList
from github.PullRequest import PullRequest
from github.Repository import Repository


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

    def get_repo(self, repo_name: str) -> Repository:
        try:
            repo = self.user.get_repo(repo_name)
            return repo
        except UnknownObjectException:
            return None

    def get_issues_or_prs(self, option: bool) -> list:
        # TODO: get user authored issues and prs
        items = self.user.get_issues()
        result = []
        for item in items:
            if (item.pull_request is None) == option:
                result.append(item)
        return result

    def close_issues_or_prs(self, url) -> None:
        items = self.user.get_issues()
        for item in items:
            if item.url == url:
                item.edit(state='closed')

    def merge_prs(self, url) -> None:
        items = self.user.get_issues()
        for item in items:
            if item.url == url:
                repo = self.user.get_repo(item.repository.name)
                pr_number = url.split('/')[-1]
                pr = repo.get_pull(int(pr_number))
                pr.merge()

    def create_issue(self, data: dict) -> Issue:
        repo = self.get_repo(data['RepoName'])
        try:
            issue = repo.create_issue(
                title=data['Title'],
                body=data['Body'],
                assignee=data['Assignee']
            )
            return issue
        except Exception:
            return None

    def create_pr(self, data: dict) -> PullRequest:
        repo = self.get_repo(data['RepoName'])
        try:
            pr = repo.create_pull(
                title=data['Title'],
                body=data['Body'],
                base=data['Base'],
                head=data['Head'],
                draft=data['Draft']
            )
            pr.add_to_assignees(data['Assignee'])
            return pr
        except Exception as e:
            return None
