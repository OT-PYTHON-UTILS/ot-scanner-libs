import os, requests,re
from giturlparse import parse

class CredScanningActions:
    def __init__(self):
        pass

    def _fetch_github_repo_urls(self, user):
        self.user = user
        urls = []
        data = re.split('[:]',self.user)
        if data[0] == "public":
            if len(re.split('[:]',self.user)) == 3:
                github_username = data[1]
                github_repo = data[2]
                URL =  "https://github.com/"+github_username+"/"+github_repo+".git"
                urls.append(URL)

            if len(re.split('[:]',self.user)) == 2:
                data = re.split('[:]',self.user)
                github_username = data[1]
                URL = "https://api.github.com/users/"+github_username+"/repos"
                response = requests.get(url = URL)
                for x in range(len(response.json())):
                    urls.append(response.json()[x]["clone_url"])

        return urls


    def _fetch_gitlab_repo_urls(self, user):
        self.user = user
        urls = []
        data = re.split('[:]',self.user)
        if data[0] == "public":
            if len(re.split('[:]',self.user)) == 3:
                gitlab_username = data[1]
                gitlab_repo = data[2]
                URL = "https://gitlab.com/"+gitlab_username+"/"+gitlab_repo+".git"
                urls.append(URL)

            if len(re.split('[:]',user)) == 2:
                data = re.split('[:]',self.user)
                gitlab_username = data[1]
                URL = "https://gitlab.com/api/v4/users/"+gitlab_username+"/projects/"
                response = requests.get(url = URL)
                for x in range(len(response.json())):
                    urls.append(response.json()[x]['http_url_to_repo'])

        if data[0] == "private":
            pass
        return urls


    def _fetch_github_org_urls(self, orgs):
        self.orgs = orgs
        urls = []
        data = re.split('[:]',self.orgs)

        if data[0] == "public":
            print(len(re.split('[:]',self.orgs)))
            if len(re.split('[:]',self.orgs)) == 4:
                github_orgname = data[2]
                github_orgrepo = data[3]
                URL =  "https://github.com/"+github_orgname+"/"+github_orgrepo+".git"
                urls.append(URL)

            if len(re.split('[:]',self.orgs)) == 3:
                data = re.split('[:]',self.orgs)
                github_orgname = data[2]
                URL = "https://api.github.com/orgs/"+github_orgname+"/repos"
                print("Without repo => ",URL)
                response = requests.get(url = URL)
                for x in range(len(response.json())):
                    urls.append(response.json()[x]["clone_url"])

        if data[0] == "private":
            pass
        return urls

    def _fetch_gitlab_org_urls(self, orgs):
        self.orgs = orgs
        urls = []

        if len(re.split('[:]',orgs)) == 2:
            data = re.split('[:]',orgs)
            gitlab_orgs = data[0]
            URL = "https://api.gitlab.com/orgs/"+gitlab_orgs+"/repos"
            print(URL)
            response = requests.get(url = URL)
            for x in range(len(response.json())):
                if data[1]:
                    urls.append(response.json()[x]["clone_url"])
                else:
                    urls.append(response.json()[x]["clone_url"])

        return urls


    def _scan_users_repo(self, users, plateform):
        self.users = users
        self.plateform = plateform
        for user in self.users:
            print(user)
            if self.plateform == "github":
                urls = CredScanningActions._fetch_github_repo_urls(self,user)
            if self.plateform == "gitlab":
                urls = CredScanningActions._fetch_gitlab_repo_urls(self,user)
            for url in urls:
                url_info = parse(url)
                command = f"trivy repo --format template --template '@trivyreportformats/html.tpl' -o reports/{url_info.host}-{url_info.repo}.html {url}"
                report = os.system(command)
        return report

    def _scan_org_repo(self, orgs,plateform):
        self.orgs = orgs
        self.plateform = plateform
        for org in self.orgs:
            if self.plateform == "github":
                urls = CredScanningActions._fetch_github_org_urls(self,org)
            if self.plateform == "gitlab":
                urls = CredScanningActions._fetch_gitlab_org_urls(self,org)
            for url in urls:
                url_info = parse(url)
                command = f"trivy repo --format template --template '@trivyreportformats/html.tpl' -o reports/{url_info.host}-{url_info.repo}.html {url}"
                report = os.system(command)
        return report
