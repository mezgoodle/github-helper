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
        result = ''
        for repo in repos:
            if not repo.archived:
                result += f'- {repo.name}. [Link]({repo.html_url}). Total issues and prs: {repo.get_issues().totalCount}\n '
        return result
