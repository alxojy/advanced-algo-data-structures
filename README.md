# Advanced Algorithms & Data Structures
### Weekly prac codes for FIT3155- Advanced algorithms & data structures

| Week(i)/Prac(i+1) | Algorithm | Notes |
|-----------|-----------|-------|
| Week 1 | Z-algorithm | O(M+N) linear string searching. Concatenate pat$text |
| Week 2 | Boyer Moore | Used z-algorithm to generate good suffix & matched prefix array. Included Galil's optimization. Code not included for week 2 prac. Reversed Boyer Moore is implemented for Assignment 1. Refer to Assignment 1, question 1. |
| Week 2 | KMP | Used z-algorithm to generate SPi values | 
| Week 3 | Ukkonen | 3 rules, 4 tricks. http://web.stanford.edu/~mjkay/gusfield.pdf. Sidenote: It was difficult implementing this and I spent a lot of time thoroughly going through the paper to completely understand the algorithm. | 

### Assignments
#### Assignment 1 
| Question | Task |
|-------|--------|
| 1 | Reversed Boyer Moore. Left to right scanning, right to left alignment. Used z-algorithm to generate good *prefix* & matched *suffix* array. Bad character table is reversed. Galil's optimization included for good prefix and matched suffix cases. |
| 2 | Wildcard matching. Used z-algorithm on unique substrings in the pattern without the wildcard, '?'. |
| 3 | Modified KMP. Transform SPi array to SPix matrix where x is the mismatched character. Included galil's optimization. |

