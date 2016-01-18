#!/usr/bin/env python3
# encoding=utf-8

from github import Github
from time import strftime


class GithubHandler(object):

    timeformat = "%F"

    def __init__(self, user, repo):
        self.user = user
        self.reponame = repo
        self.fullrepo = "%s/%s" % (user, repo)
        self.gayhub = Github()
        self.repo = self.gayhub.get_repo(self.fullrepo)

    def get_desciption(self):
        return self.repo.description

    def get_forkscount(self):
        return self.repo.forks_count

    def get_name(self):
        return self.repo.name

    def get_openissuecount(self):
        return self.repo.open_issues_count

    def get_owner(self):
        return self.repo.owner

    def get_starcount(self):
        return self.repo.stargazers_count

    def get_watchcount(self):
        return self.repo.watchers_count

    def get_ctime(self):
        return self.repo.created_at.strftime(self.timeformat)

    def get_utime(self):
        return self.repo.updated_at.strftime(self.timeformat)


if __name__ == '__main__':
    gh = GithubHandler("BruceZhang1993", "PyIrcBot")
    print(gh.get_ctime())
