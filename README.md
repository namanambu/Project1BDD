Section 1: Background on Hungarian Algorithm and Objective

The assignment problem is a classical optimization problem where the goal is to select the maximum matching with the lowest possible cost. In mathematical terms, it boils down to finding a minimum-weight matching in a bipartite graph, where each agent–task pairing carries a weight that reflects how suitable that match is. To solve this type of problem efficiently, Harold Kuhn published the Hungarian algorithm in 1955.[1] The method works by transforming the cost matrix through row and column reductions and iteratively uncovering zeros until an optimal set of pairings is reached.[2] In our project, we used this approach by converting doctors’ ranked hospital preferences into a cost matrix and applying the algorithm to generate assignments that minimize overall dissatisfaction while respecting hospital capacity limits.

Section 2: Model Assumptions
- Each doctor provides a complete ranking of all hospitals with no ties or missing values
- Hospitals do not rank doctors, only doctors rank hospitals
- Each hospital has a capacity currently all set to 1
- The total capacity may differ from the number of doctors (N is not always equal to K). Our code handles this by:
  - Duplicating hospital columns to represent multiple slots
  - Adding “no match” dummy columns/rows to make the cost matrix square
- Doctors can be unmatched if no hospital slots remain
- Ties between equally optimal assignments are broken arbitrarily
- Objective considers rankings only and no other factors
- Assumes reasonable penalty for “no match” so it is only chosen if necessary
- The difference between rank 1 and 2 is treated the same as between 2 and 3
- Hungarian algorithm always produces a solution
- If multiple optimal solutions exist, the particular assignment chosen depends on how zeros are marked/traversed in the algorithm
- Hungarian is fine for small or medium test cases but could become slow for very large datasets

Section 3: Design Decisions

- We chose to represent the problem in a CSV file where each row corresponds to a doctor’s ranked preferences and the header row encodes hospital capacities. This made it easy to test with different datasets and use pandas for preprocessing.
- Hospitals with more than one slot are expanded into multiple columns, such as H1A and H1B, so that the problem becomes one-to-one and fits the Hungarian algorithm’s requirements[3]
- Because the Hungarian algorithm requires a square cost matrix, we padded the smaller dimension with dummy rows/columns. A special “no match” column was added to represent doctors who cannot be placed for cases where n is not equal to k
- Doctors’ rankings were directly converted into costs (lower rank = lower cost). This makes the optimization objective “minimize cost” equivalent to “maximize doctor satisfaction.”
- We modularized the algorithm into steps based on a youtube video explanation of the algorithm which made the logic easier to debug and explain[4]:
     - Step 1: Row reduction
     - Step 2: Column reduction
     - Step 3: Identify zeros and cover them with minimal lines
     - Step 4: Adjust the matrix when coverage is insufficient
     - Step 5: Extract optimal assignments from zero positions
- We wrote helper functions to map matrix indices back to actual doctor and hospital names, and return results as a clean pandas data frame
- To evaluate results, we defined a scoring function that sums the rank costs of assigned matches and compares this to a maximum possible dissatisfaction score. This gave us a percentage measure of solution quality
- By separating data import, preprocessing, algorithm steps, and output formatting into different modules, we kept the code design flexible and easy to maintain

Section 4: Labour Division

- Sakshi worked on implementing Step 1 (row reduction), Step 2 (column reduction), and Step 4 (matrix adjustment) functions of the Hungarian algorithm. She also prepared this project write-up and developed testing functions to check that the code was running correctly

- Jonathan focused on Step 3 of the Hungarian algorithm, which involved crossing out zeros and determining the minimum number of lines needed to cover them. He also put together the main demo script that showcased the full workflow of the algorithm on sample data

- Nnemdi handled the initial data import and preprocessing, including setting up hospital capacities and padding the matrix so it could be used by the algorithm. In addition, she implemented Step 5 of the Hungarian algorithm, which extracted the final assignments of doctors to hospitals from the reduced cost matrix

Section 5: Organization of this Repository
Our code is split into a few main pieces to keep things clean and easy to follow:
- Main.py: runs the full demo, tying everything together and printing the final matches and satisfaction score %
- Demo.ipynb: a notebook we used to show step-by-step outputs and explain the algorithm
- HungarianAlgoImportData.py: handles data loading, hospital capacities, prepping the matrix and scoring results
- Hungarian_Alg_Steps.py: contains the core steps of the Hungarian algorithm (row reduction, column reduction, and matrix adjustment)
- Hungarian_Alg_LineCheck.py: handles crossing out zeros (Step 3), the final assignment step (Step 5), and mapping results back to doctor and hospital names
- README.md: Contains this specific project write up and description
- CSV files: different test datasets we used to check the algorithm

References (cited):
[1]The Hungarian Algorithm for the Assignment Problem. The Department of Computer Science. Accessed September 13, 2025. http://www.cs.emory.edu/~cheung/Courses/253/Syllabus/Assignment/algorithm.html.  
[2]Efimov V. The Hungarian algorithm and its applications in computer vision. Towards Data Science. September 9, 2025. Accessed September 13, 2025. https://towardsdatascience.com/hungarian-algorithm-and-its-applications-in-computer-vision/.  
[3]Hungarian algorithm for solving the assignment problem. Hungarian Algorithm - Algorithms for Competitive Programming. December 13, 2023. Accessed September 13, 2025. https://cp-algorithms.com/graph/hungarian-algorithm.html.  
[4]The Munkres Assignment Algorithm (Hungarian Algorithm). YouTube. Accessed September 13, 2025. https://www.youtube.com/watch?v=cQ5MsiGaDY8&t=290s&pp=ygUdaHVuZ2FyaWFuIGFsZ29yaXRobSBleHBsYWluZWQ%3D. 
