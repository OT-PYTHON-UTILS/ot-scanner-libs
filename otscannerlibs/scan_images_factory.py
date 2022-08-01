import os

class scanImages:
    def __init__(self, client):
        self.client = client

    def _scan_images_with_given_versions(self,ecr_url,repository_name,repository_versions):
        self.ecr_url = ecr_url
        self.repository_name = repository_name
        self.repository_versions = repository_versions
        for repository_version in repository_versions:
            command = f"trivy image --format template --template '@reportFormats/html.tpl' -o reports/{self.repository_name}-{repository_version}.html {self.ecr_url}/{self.repository_name}:{repository_version}"
        os.system(command)

    def _scan_images_with_all_versions(self,ecr_url, repository_name):
        self.ecr_url = ecr_url
        self.repository_name = repository_name
        repository_details = self.client.describe_images(repositoryName=repository_name)
        repository_versions = []
        for repository_detail in range(len(repository_details['imageDetails'])):
            for image in repository_details['imageDetails'][repository_detail]['imageTags']:
                repository_versions.append(image)
        scanImages._scan_images_with_given_versions(self,ecr_url,repository_name,repository_versions)