# Advanced Algorithms & Data Structures
### Weekly prac codes for FIT3155- Advanced algorithms & data structures

| Week[i] | Algorithm | Notes |
|-----------|-----------|-------|
| Week 1 | Z-algorithm | O(M+N) linear string searching. Concatenate pat$text |
| Week 2 | Boyer Moore | Used z-algorithm to generate good suffix & matched prefix array. Included Galil's optimization. <br>  Code not included for week 2 prac on normal Boyer Moore. Reversed Boyer Moore is implemented instead. Right to left scanning, left to right letter comparisons, good prefix & matched suffix array. |
| | KMP | Used z-algorithm to generate SPi values | 
| | Modified KMP | Transform SPi array to SPix matrix where x is the mismatched character. Included galil's optimization. |
| Week 3 | Ukkonen | Included code to generate suffix array. (Store 'j' pointer on each leaf when building suffix tree. Traverse tree in lexicographical order to the leaf to generate suffix arr). <br> Notes: <br> 3 rules, 4 tricks. Understanding the algorithm: http://web.stanford.edu/~mjkay/gusfield.pdf. <br> Code implementation based on: https://www.cs.helsinki.fi/u/ukkonen/SuffixT1withFigs.pdf. <br> Resources which made understanding the algo easier: https://www.geeksforgeeks.org/ukkonens-suffix-tree-construction-part-6/?ref=rp & https://stackoverflow.com/questions/9452701/ukkonens-suffix-tree-algorithm-in-plain-english. | 
| Week 4 | Disjoint sets | Union by size, union by height/ rank. |
| Week 5 | Binomial heap | Added a lookup table for O(1) search. <br> Code implementation based on: http://www.cs.toronto.edu/~anikolov/CSC265F19/binomial-heaps.pdf |
| Week 6 | Fibonacci heap | Added a lookup table for O(1) search. <br> Code implementation based on: http://staff.ustc.edu.cn/~csli/graduate/algorithms/book6/chap21.htm |
| Week 7 | B-trees | |
