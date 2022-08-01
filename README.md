# ot-scanner-libs
I am placeholder of all the python libraries related to Images and Credentials Scanning


## Description

In this library contains two modules:

* Images Scanner(scan_images_factory):

    This module is use to scan the container images present on the private AWS ECR repository. With the help of this module we can scan all the version of repository or only scan the specific version.

* Credentials Scanner(creds_action_factory):

    This module is use to scan the credentails in git tools like Github and GitLab. With the help of this module we can scan all the public repositories of the user and the organisations.
## Getting Started

### Dependencies

* [Trivy Tool](https://github.com/aquasecurity/trivy)

### Installing

* Create a reports directory parallely from where you executing your script.

### Library Calling
from otscannerlibs import   creds_action_factory, scan_images_factory


## Authors

Abhishek Kumar Tiwari

[Contact Info](https://github.com/AbktOps)

## Version History

* 0.1
    * Initial Release

