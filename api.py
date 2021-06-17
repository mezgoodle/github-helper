from github import Github

g = Github('TOKEN')

for repo in g.get_user().get_repos():
    print(repo.name)
    # to see all the available attributes and methods
    # print(dir(repo))
