from github import Github


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

    def get_repos(self):
        user = self.g.get_user()
        repos = user.get_repos()
        for repo in repos:
            if not repo.archived:
                print(repo.name, repo.html_url, repo.get_issues().totalCount)


