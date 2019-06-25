[Public Git Archive](https://pga.sourced.tech/) is an archive of all github projects with more than 50 stars.
It is downloaded and stored as index2.csv

Firstly, get_java_projects.py is executed to create a file java_projects_data.txt. It finds all projects in the archive that have at least
1 line of code in Java and saves the following information for them:
* author of the repository;
* name of the repository;
* licensing information.

After that, download_projects.py downloads the projects and saves them in /home/ubuntu/projects/. In the end, each project will be located
in the directory with the name of the author of the repository, and will consist of three items:
* git-cloned directory with the entire history of changes;
* zip-file of the last commit to be processed by SourcererCC;
* txt-file with the licensing information.

The download happens in several steps. The reason for that is that certain projects are deleted or made private after the compilation of the archive, so some of the repositories will not be cloned. The script deletes extra files and also checks that the zip-file contains the main branch of the repository. During its operation, the script creates temporary files list_checks.txt (that checks the existence of the project files) and list_branches.txt (that stores the main brach of each repository).

The last stage of data collection is running create_a_list_of_projects.py that generates project-list.txt, a file that must be copied to
SourcererCC/tokenizers/block-level/.

Now you are ready to continue on to the next stage: searching for clones.
