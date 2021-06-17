from github import Github


class API:
    def __init__(self, token):
        self.g = Github(token)

    def get_user_info(self) -> str:
        """
        Method that returns string with information about user
        :return: string with information
        """
        user = self.g.get_user()
        return f'You have been authenticated with login _{user.login}_ as _{user.name}_'

    def get_repos(self):
        pass

