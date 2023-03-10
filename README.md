# Frequent Pattern Growth Approach for Mining Frequent Itemsets
## Description
Course: Data Mining and Knowledge Discovery (Fall 2021) <br />
Task: Write own program


>“Can we design a method that mines the complete set of frequent itemsets without such a costly candidate generation process?” An interesting method in this attempt is called frequent pattern growth, or simply FP-growth, which adopts a divide-and-conquer strategy as follows. First, it compresses the database representing frequent items into a frequent pattern tree, or FP-tree, which retains the itemset association information. It then divides the compressed database into a set of conditional databases (a special kind of projected database), each associated with one frequent item or “pattern fragment,” and mines each database separately. For each “pattern fragment,” only its associated data sets need to be examined. Therefore, this approach may substantially reduce the size of the data sets to be searched, along with the “growth” of patterns being examined. 
>
>*J. Han, Jian Pei, and Micheline Kamber, Data mining: concepts and techniques. S.l: Elsevier Science, 2011.*


### Task:
![Screenshot 2023-03-10 155907](https://user-images.githubusercontent.com/101310529/224261206-5c0c44d4-c165-4058-ad86-c0628691d29f.png)


### Answer:
#### Frequency Table for the Items in descending order of frequency
![Screenshot 2023-03-10 160614](https://user-images.githubusercontent.com/101310529/224261268-2845c8c7-0e5f-408d-adac-ea150678d5a6.png)


#### Result of the frequent itemsets sorted in descending order of support count. * *(format: (term1, term2 ...): support_count )* *
```
Frequent Itemsets Final Output (Sorted Descending)
               Frequent Item  Support
0                     [Milk]     5526
1                     [Ghee]     5510
2            [Coffee Powder]     5509
3                  [Yougurt]     5503
4                    [Bread]     5484
5                    [Sweet]     5483
6                    [Sugar]     5482
7                   [Butter]     5481
8                   [Cheese]     5476
9                   [Panner]     5444
10                   [Lassi]     5432
11              [Tea Powder]     5383
12     [Ghee, Coffee Powder]     2578
13            [Sweet, Lassi]     2576
14           [Sugar, Butter]     2571
15             [Milk, Sugar]     2563
16  [Coffee Powder, Yougurt]     2555
17           [Bread, Panner]     2550
18           [Sweet, Butter]     2543
19            [Bread, Sweet]     2539
20             [Milk, Lassi]     2539
21         [Yougurt, Cheese]     2532
22            [Ghee, Butter]     2530
23           [Bread, Cheese]     2530
24          [Yougurt, Sugar]     2529
25         [Yougurt, Butter]     2529
26    [Coffee Powder, Bread]     2528
27            [Ghee, Panner]     2523
28     [Milk, Coffee Powder]     2518
29   [Coffee Powder, Cheese]     2517
30             [Milk, Bread]     2517
31             [Ghee, Sugar]     2516
32           [Milk, Yougurt]     2513
33    [Coffee Powder, Lassi]     2512
34             [Milk, Sweet]     2512
35             [Ghee, Lassi]     2511
36              [Milk, Ghee]     2511
37          [Yougurt, Bread]     2507
38            [Bread, Lassi]     2506
39           [Sugar, Panner]     2505
40           [Sweet, Panner]     2505
41             [Ghee, Sweet]     2504
42             [Ghee, Bread]     2503
43    [Coffee Powder, Sugar]     2503
44       [Sweet, Tea Powder]     2503
45            [Sugar, Lassi]     2503
46   [Coffee Powder, Butter]     2502
47           [Butter, Lassi]     2501
```
