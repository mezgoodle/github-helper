from unittest import TestCase

from github.PaginatedList import PaginatedList
from github.Repository import Repository

from api import Api
from config import GITHUB_TOKEN


class TestApi(TestCase):
    def setUp(self) -> None:
        self.api = Api(GITHUB_TOKEN)

    def test_get_user_info(self):
        output = self.api.get_user_info()
        self.assertIsNotNone(output)
        self.assertIsInstance(output, tuple)

    def test_get_repos(self):
        output = self.api.get_repos()
        self.assertIsNotNone(output)
        self.assertIsInstance(output, PaginatedList)

    def test_get_repo(self):
        repo_name = 'portfolio'
        non_exist_repo_name = 'portfolio1'
        output = self.api.get_repo(repo_name)
        self.assertIsNotNone(output)
        self.assertIsInstance(output, Repository)
        output = self.api.get_repo(non_exist_repo_name)
        self.assertIsNone(output)

    def test_get_issues_or_prs(self):
        output = self.api.get_issues_or_prs(True)
        self.assertIsNotNone(output)
        self.assertIsInstance(output, list)
        self.assertTrue(all(not item.pull_request for item in output))
        output = self.api.get_issues_or_prs(False)
        self.assertIsNotNone(output)
        self.assertIsInstance(output, list)
        self.assertTrue(all(item.pull_request for item in output))
