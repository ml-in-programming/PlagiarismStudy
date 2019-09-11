# GitHub Plagiarism Study

This project is dedicated to the analysis of plagiarism and license violations in the Java corpus of Github. The research is currently being conducted and is planned to be publised in 2020.

The study consists of three main parts that together make up this repository:
1. **Data Collection** describes the compilation and the download of our corpus. At the end of this stage, the corpus is downloaded in the necessary formats (zip-files for clone detection and git clones for analysis), along with the licensing information of the projects.
2. **Clone Detection** takes place in the downloaded projects using our modified version of **SourcererCC**, presented here as a submodule. In case of such a large dataset, the search is conducted in parallel on several Amazon Web Services. After this stage, a list of clone pairs is obtained for the corpus.
3. Gathering **Statistics** is the final part of our pipeline, that takes both the downloaded projects and detected clones and uses them to perform the analysis of plagiarism and licensing violations in the data. For that, linenses and the last times of modification of code are gathered, a list of clones for each fragment of code is compiled and the analysis itself is conducted.

Each of these segments has its own detailed ReadMe.

If you have any more questions, feel free to contact us at areyde.elvgren@gmail.com.
