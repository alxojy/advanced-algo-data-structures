# Advanced Algorithms & Data Structures
### Weekly prac codes for FIT3155- Advanced algorithms & data structures

| Week(i)/Prac(i+1) | Algorithm | Notes |
|-----------|-----------|-------|
| Week 1 | Z-algorithm | O(M+N) linear string searching. Concatenate pat$text |
| Week 2 | Boyer Moore | Used z-algorithm to generate good suffix & matched prefix array. Included Galil's optimization. <br>  Code not included for week 2 prac. Reversed Boyer Moore is implemented for Assignment 1. Refer to Assignment 1, question 1. |
| Week 2 | KMP | Used z-algorithm to generate SPi values | 
| Week 3 | Ukkonen | 3 rules, 4 tricks. Understanding the algorithm: http://web.stanford.edu/~mjkay/gusfield.pdf. <br> Code implementation: https://www.cs.helsinki.fi/u/ukkonen/SuffixT1withFigs.pdf. <br> Resources which made understanding the algo easier: https://www.geeksforgeeks.org/ukkonens-suffix-tree-construction-part-6/?ref=rp & https://stackoverflow.com/questions/9452701/ukkonens-suffix-tree-algorithm-in-plain-english. | 
| Week 4 | Disjoint sets | Union by size, union by height/ rank. |

### Assignments
#### Assignment 1 
| Question | Task |
|-------|--------|
| 1 | Reversed Boyer Moore. Left to right scanning, right to left alignment. Used z-algorithm to generate good *prefix* & matched *suffix* array. Bad character table is reversed. Galil's optimization included for good prefix and matched suffix cases. |
| 2 | Wildcard matching. Used z-algorithm on unique substrings in the pattern without the wildcard, '?'. |
| 3 | Modified KMP. Transform SPi array to SPix matrix where x is the mismatched character. Included galil's optimization. |

