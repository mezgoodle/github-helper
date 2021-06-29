from github import Github
from github.GithubException import UnknownObjectException
from github.Issue import Issue
from github.PaginatedList import PaginatedList
from github.PullRequest import PullRequest
from github.Repository import Repository


class Api:
    """
    Class for manipulating with GitHub API
    """
    def __init__(self, token: str):
        """
        Create the authenticated user as object
        :param token: token for GitHub API
        """
        self.g = Github(token)
        self.user = self.g.get_user()
        self.url = 'https://api.github.com/repos/'

    def get_user_info(self) -> str:
        """
        Method that returns string with information about user
        :return: string with information
        """
        print(self.user.repos_url)
        return f'You have been authenticated with login *{self.user.login}* as *{self.user.name}*'

    def get_repos(self) -> PaginatedList:
        """
        Method for getting all user repositories
        :return: list of repositories
        """
        repos = self.user.get_repos()
        return repos

    def get_repo(self, repo_name: str) -> Repository:
        """
        Method for getting one repository
        :param repo_name: short name of the repository
        :return:
        """
        try:
            repo = self.user.get_repo(repo_name)
            return repo
        except UnknownObjectException:
            return None

    def get_issues_or_prs(self, option: bool) -> list:
        """
        Method for getting oll issues or pull requests
        :param option: issues - True, pull requests - False
        :return: list of items
        """
        items = self.user.get_issues(filter='all')
        result = []
        for item in items:
            if (item.pull_request is None) == option:
                result.append(item)
        return result

    def close_issues_or_prs(self, part_of_url: str) -> None:
        """
        Method for closing issues or pull requests
        :param part_of_url: part of api url for closing
        :return: nothing to return
        """
        url = self.url + part_of_url
        items = self.user.get_issues(filter='all')
        for item in items:
            if item.url == url:
                item.edit(state='closed')

    def merge_prs(self, part_of_url: str) -> None:
        """
        Method for merging pull requests
        :param part_of_url: part of api url for merging
        :return: nothing to return
        """
        url = self.url + part_of_url
        items = self.user.get_issues(filter='all')
        for item in items:
            if item.url == url:
                repo = self.user.get_repo(item.repository.name)
                pr_number = url.split('/')[-1]
                pr = repo.get_pull(int(pr_number))
                pr.merge()

    def create_issue(self, data: dict) -> Issue:
        """
        Method for creating issue
        :param data: meta-data for issue
        :return: Issue object
        """
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
        """
        Method for creating pull request
        :param data: meta-data for pull request
        :return: PullRequest object
        """
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
