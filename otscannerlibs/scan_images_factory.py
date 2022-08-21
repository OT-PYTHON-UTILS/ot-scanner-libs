import os
import logging
from botocore.exceptions import ClientError

class scanImages:
    def __init__(self, client):
        self.client = client

    def _scan_images_with_given_versions(self,ecr_url,repository_name,repository_versions):
        self.ecr_url = ecr_url
        self.repository_name = repository_name
        self.repository_versions = repository_versions
        try:
            self.client.describe_images(repositoryName=repository_name)
            for repository_version in repository_versions:
                try:
                    logging.info(f"Scanning {repository_name}:{repository_version} ...")
                    command = f"trivy image --format template --template '@reportFormats/html.tpl' -o reports/{self.repository_name}-{repository_version}.html {self.ecr_url}/{self.repository_name}:{repository_version}"
                    os.system(command)
                except BaseException as e:
                    logging.error(f'Failed to scan {repository_name}:{repository_version} image. Error message: {e}')
                
        except ClientError as e:
            if "RepositoryNotFoundException" in str(e):
                logging.error(f'Repository {repository_name} not found in ECR. Error message: {e}')
            else:
                logging.error(f'Failed to scan {repository_name} images. Error message: {e}')

    def _scan_images_with_all_versions(self,ecr_url, repository_name):
        self.ecr_url = ecr_url
        self.repository_name = repository_name
        try:
            repository_details = self.client.describe_images(repositoryName=repository_name)
            repository_versions = []
            for repository_detail in range(len(repository_details['imageDetails'])):
                for image in repository_details['imageDetails'][repository_detail]['imageTags']:
                    repository_versions.append(image)
            scanImages._scan_images_with_given_versions(self,ecr_url,repository_name,repository_versions)
        except ClientError as e:
            if "RepositoryNotFoundException" in str(e):
                logging.error(f'Repository {repository_name} not found in ECR. Error message: {e}')
            else:
                raise e
        
