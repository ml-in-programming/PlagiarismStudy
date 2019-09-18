Gathering statistics is the final and the main stage of Plagiarism Detection. 

Firstly, GatherData.py collects all the necessary information about the blocks into the created /data/ subdirectory. In the process, it creates a temporary file resultsExtended.pairs, which consists of only the pairs of interest. It then uses a set of the blocks of interest from these pairs to collect the information:
* The licenses are collected using the latest version of [ninka](http://ninka.turingmachine.org/) (the repository on [GitHub](https://github.com/dmgerman/ninka)), which parses the top of each file and lists the possible licenses. If ninka detects a license, we choose the most probable one, if it doesn't — we choose the project's license from PGA data, and if the project also doesn't have a license, we list it as "All Rights Reserved". The results are stored in StatisticsLicensesFiles.txt.
* *git blame* is used to gather the information about the last time of modifications of the blocks. The information is collected for all the necessary files (stored in StatisticsBlameFiles.txt), then for each block the largest mode among its lines is calculated and the resulting date is considered to be this block's last time of modification. This data is stored in StatisticsBlameBlocks.txt.

Additionally, if any of the file names has a character that doesn't allow it to be processed by either ninka or git blame, it is listed in StatisticsBadFiles.txt, and in the end, the final list of pairs resultsRelated.pairs is compiled for the next step.

Next, GetNeighbors.py compiles a list of all blocks of interest and a list of all their clones for each of them. In the process, it creates a subdirectory /data/neighbors/ for temporary files and deletes it afterwards.
