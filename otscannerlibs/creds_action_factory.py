import os, requests,re
from giturlparse import parse
import logging

class CredScanningActions:
    def __init__(self):
        pass

    def _fetch_github_repo_urls(self,user):
        self.user = user
        urls = []
        input_user_data = re.split('[:]',self.user)
        if input_user_data[0] == "public":
            if len(re.split('[:]',self.user)) == 3:
                github_username = input_user_data[1]
                github_repo = input_user_data[2]
                URL =  "https://github.com/"+github_username+"/"+github_repo+".git"
                urls.append(URL)

            if len(re.split('[:]',self.user)) == 2:
                input_user_data = re.split('[:]',self.user)
                github_username = input_user_data[1]
                URL = "https://api.github.com/users/"+github_username+"/repos"
                response = requests.get(url = URL)
                for url in range(len(response.json())):
                    urls.append(response.json()[url]["clone_url"])

        if input_user_data[0] == "private":
            logging.warning("Enter the public repository only")

        return urls


    def _fetch_gitlab_repo_urls(self,user):
        self.user = user
        urls = []
        input_user_data = re.split('[:]',self.user)
        if input_user_data[0] == "public":
            if len(re.split('[:]',self.user)) == 3:
                gitlab_username = input_user_data[1]
                gitlab_repo = input_user_data[2]
                URL = "https://gitlab.com/"+gitlab_username+"/"+gitlab_repo+".git"
                urls.append(URL)

            if len(re.split('[:]',self.user)) == 2:
                input_user_data = re.split('[:]',self.user)
                gitlab_username = input_user_data[1]
                URL = "https://gitlab.com/api/v4/users/"+gitlab_username+"/projects/"
                response = requests.get(url = URL)
                for url in range(len(response.json())):
                    urls.append(response.json()[url]['http_url_to_repo'])

        if input_user_data[0] == "private":
            logging.warning("Enter the public repository only")
        
        return urls

    def _fetch_github_org_urls(self,org):
        self.org = org
        urls = []
        input_user_data = re.split('[:]',self.org)
        if input_user_data[0] == "public":
            if len(re.split('[:]',self.org)) == 4:
                github_orgname = input_user_data[2]
                github_orgrepo = input_user_data[3]
                URL =  "https://github.com/"+github_orgname+"/"+github_orgrepo+".git"
                urls.append(URL)

            if len(re.split('[:]',self.org)) == 3:
                input_user_data = re.split('[:]',self.org)
                github_orgname = input_user_data[2]
                URL = "https://api.github.com/orgs/"+github_orgname+"/repos"
                response = requests.get(url = URL)
                for url in range(len(response.json())):
                    urls.append(response.json()[url]["clone_url"])

        if input_user_data[0] == "private":
            logging.warning("Enter the public organisations only")

        return urls

    def _fetch_gitlab_org_urls(self,org):
        self.org = org
        urls = []
        if len(re.split('[:]',self.org)) == 2:
            input_user_data = re.split('[:]',self.org)
            gitlab_orgs = input_user_data[0]
            URL = "https://api.gitlab.com/orgs/"+gitlab_orgs+"/repos"
            response = requests.get(url = URL)
            for url in range(len(response.json())):
                if input_user_data[1]:
                    urls.append(response.json()[url]["clone_url"])
                else:
                    urls.append(response.json()[url]["clone_url"])

        return urls

    def _scan_users_repo(self,users,plateform):
        self.users = users
        self.plateform = plateform
        try:
            for user in self.users:
                if self.plateform == "github":
                    urls = self._fetch_github_repo_urls(user)
                if self.plateform == "gitlab":
                    urls = self._fetch_gitlab_repo_urls(user)
                for url in urls:
                    url_info = parse(url)
                    command = f"trivy repo --format template --template '@trivyreportformats/html.tpl' -o reports/{url_info.host}-{url_info.repo}.html {url}"
                    os.system(command)
        except TypeError as e:
            if "NoneType" in str(e):
                logging.warning("Please enter the data in the users section")

    def _scan_org_repo(self,orgs,plateform):
        self.orgs = orgs
        self.plateform = plateform
        try:
            for org in self.orgs:
                if self.plateform == "github":
                    urls = self._fetch_github_org_urls(org)
                if self.plateform == "gitlab":
                    urls = self._fetch_gitlab_org_urls(org)
                for url in urls:
                    url_info = parse(url)
                    command = f"trivy repo --format template --template '@trivyreportformats/html.tpl' -o reports/{url_info.host}-{url_info.repo}.html {url}"
                    os.system(command)
        except TypeError as e:
            if "NoneType" in str(e):
                logging.warning("Please enter the data in the orgs section")
