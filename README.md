<h1 id="project-title" align="center">
  github-helper <img alt="logo" width="40" height="40" src="https://raw.githubusercontent.com/mezgoodle/images/master/MezidiaLogoTransparent.png" /><br>
  <img alt="language" src="https://img.shields.io/badge/language-python-brightgreen?style=flat-square" />
  <img alt="GitHub issues" src="https://img.shields.io/github/issues/mezgoodle/github-helper?style=flat-square" />
  <img alt="GitHub closed issues" src="https://img.shields.io/github/issues-closed/mezgoodle/github-helper?style=flat-square" />
  <img alt="GitHub pull requests" src="https://img.shields.io/github/issues-pr/mezgoodle/github-helper?style=flat-square" />
  <img alt="GitHub closed pull requests" src="https://img.shields.io/github/issues-pr-closed/mezgoodle/github-helper?style=flat-square" />
  <img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/mezgoodle/github-helper?style=flat-square">
</h1>

<p align="center">
 🌟Hello everyone! This is the repository of Telegram bot to manage GitHub profile.🌟
</p>

## Motivation :exclamation:

Telegram is a comfortable messanger. Also it has very good API, and bots can make our life easier. So I want to manage my **GitHub** from **Telegram** by bot.

## Build status :hammer:

Here you can see build status of [continuous integration](https://en.wikipedia.org/wiki/Continuous_integration):

[![Python package](https://github.com/mezgoodle/github-helper/actions/workflows/python-package.yml/badge.svg)](https://github.com/mezgoodle/github-helper/actions/workflows/python-package.yml)
[![{Python} CI](https://gitlab.com/mezgoodle/github-helper/badges/main/pipeline.svg)](https://gitlab.com/mezgoodle/github-helper/-/pipelines)

## Badges :mega:

[![Theme](https://img.shields.io/badge/Theme-Bot-brightgreen?style=flat-square)](https://uk.wikipedia.org/wiki/%D0%A0%D0%BE%D0%B1%D0%BE%D1%82_(%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%B0))
[![Platform](https://img.shields.io/badge/Platform-Telegram-brightgreen?style=flat-square)](https://telegram.org/)
 
## Screenshots :camera:

- Start command

![Screenshot 1](https://raw.githubusercontent.com/mezgoodle/images/master/github-helper1.png)

- Help command

![Screenshot 2](https://raw.githubusercontent.com/mezgoodle/images/master/github-helper2.png)

- Set token

![Screenshot 3](https://raw.githubusercontent.com/mezgoodle/images/master/github-helper3.png)

- Me command

![Screenshot 4](https://raw.githubusercontent.com/mezgoodle/images/master/github-helper4.png)

- Get repositories

![Screenshot 5](https://raw.githubusercontent.com/mezgoodle/images/master/github-helper5.png)

![Screenshot 6](https://raw.githubusercontent.com/mezgoodle/images/master/github-helper6.png)

- Get repository

![Screenshot 7](https://raw.githubusercontent.com/mezgoodle/images/master/github-helper7.png)

- Get issues

![Screenshot 8](https://raw.githubusercontent.com/mezgoodle/images/master/github-helper8.png)

![Screenshot 9](https://raw.githubusercontent.com/mezgoodle/images/master/github-helper9.png)

- Get pull requests

![Screenshot 10](https://raw.githubusercontent.com/mezgoodle/images/master/github-helper10.png)

- Create issue by command

![Screenshot 11](https://raw.githubusercontent.com/mezgoodle/images/master/github-helper11.png)

- Create pull request by button

![Screenshot 12](https://raw.githubusercontent.com/mezgoodle/images/master/github-helper12.png)

## Tech/framework used :wrench:

**Built with**

- [aiogram](https://github.com/aiogram/aiogram)
- [cryptography](https://pypi.org/project/cryptography/)
- [PyGithub](https://pygithub.readthedocs.io/en/latest/)
- [pymongo](https://pymongo.readthedocs.io/en/stable/)

## Features :muscle:

With my bot you can **get** information about your _repositories_, _issues_, _pull requests_, **close** issues and pull requests, **create** new ones and **merging** pull requests.

## Code Example :pushpin:

- Class to work with **MongoDB**:

```python
from pymongo import MongoClient, results


class Client:
    """
    Class for manipulating MongoDB cluster
    """
    def __init__(self, password, db_name: str, collection_name: str):
        """
        Initializing client object with access to database
        :param password: password to account
        :param db_name: name of database in current cluster
        :param collection_name: name of collection in current database
        """
        cluster = MongoClient(f'mongodb+srv://mezgoodle:{password}@githubhelper.2tnee.mongodb.net/githubhelper'
                              '?retryWrites=true&w=majority')
        db = cluster[db_name]
        self.collection = db[collection_name]

    def insert(self, data: dict) -> results.InsertOneResult:
        """
        Method for inserting data in collection
        :param data: dictionary with field name and value
        :return: result of inserting
        """
        try:
            return self.collection.insert_one(data)
        except Exception as e:
            print('Error:', e)

    def get(self, query: dict) -> dict:
        """
        Method for getting data from collection
        :param query: dictionary with field name and value
        :return: the document that matches the query
        """
        try:
            return self.collection.find_one(query)
        except Exception as e:
            print('Error:', e)

    def update(self, query: dict, data: dict) -> results.UpdateResult:
        """
        Method for updating data in collection
        :param query: dictionary with field name and value
        :param data: dictionary with the old field name in document and the new value
        :return: result of updating
        """
        try:
            return self.collection.update_one(query, {'$set': data})
        except Exception as e:
            print('Error:', e)

    def delete(self, query: dict) -> results.DeleteResult:
        """
        Method for deleting data in collection
        :param query: dictionary with field name and value
        :return: result of deleting
        """
        try:
            return self.collection.delete_one(query)
        except Exception as e:
            print('Error:', e)
```

- Class to work with **GitHub API**:

```python
from typing import Tuple

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

    def get_user_info(self) -> Tuple[str, str]:
        """
        Method that returns string with information about user
        :return: avatar url and string with information
        """
        return self.user.avatar_url, f'You have been authenticated with login *{self.user.login}* ' \
                                     f'as *{self.user.name}*.\n' \
                                     f'[Link]({self.user.html_url}) to the profile.'

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

    def close_issues_or_prs(self, part_of_url: str) -> bool:
        """
        Method for closing issues or pull requests
        :param part_of_url: part of api url for closing
        :return: status of closing
        """
        try:
            full_url = self.url + part_of_url
            items = self.user.get_issues(filter='all')
            for item in items:
                if item.url == full_url:
                    item.edit(state='closed')
                    return True
        except Exception:
            return False

    def merge_prs(self, part_of_url: str) -> bool:
        """
        Method for merging pull requests
        :param part_of_url: part of api url for merging
        :return: status of merging
        """
        try:
            full_url = self.url + part_of_url
            items = self.user.get_issues(filter='all')
            for item in items:
                if item.url == full_url:
                    repo = self.user.get_repo(item.repository.name)
                    pr_number = full_url.split('/')[-1]
                    pr = repo.get_pull(int(pr_number))
                    pr.merge()
                    return True
        except Exception:
            return False

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
        except Exception:
            return None
```

## Installation :computer:

1. Clone this repository by the command:

```shell
git clone https://github.com/mezgoodle/github-helper.git
```

or do it with [GitHub CLI](https://cli.github.com/).

2. Move to the project and install all packages with [pip](https://pypi.org/project/pip/):

```shell
cd github-helper
pip install -r requirements.txt
```

## Fast usage :dash:

1. Set your environment variables:

In _Windows_ just change by context menu

In _Linux/Mac OS_:

```shell
export API_TOKEN=token
export MONGO_PASSWORD=password
export GITHUB_TOKEN=token
export HASH_KEY=key
```

or change values in [config.py](https://github.com/mezgoodle/github-helper/blob/main/config.py) file.

> for GitHub token you can only set repos scope

2. Execute the script:

```shell
python bot.py
```

## Tests :microscope:

There are three files for testing: [test_api.py](https://github.com/mezgoodle/github-helper/blob/main/test_api.py), [test_database.py](https://github.com/mezgoodle/github-helper/blob/main/test_database.py), [test_hashing.py](https://github.com/mezgoodle/github-helper/blob/main/test_hashing.py)

To execute tests, type the command:

```shell
python -m unittest -v
```

## Contribute :running:

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change. Also look at the [CONTRIBUTING.md](https://github.com/mezgoodle/github-helper/blob/main/CONTRIBUTING.md).

## License :bookmark:

MIT © [mezgoodle](https://github.com/mezgoodle)
