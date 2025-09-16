"""
Steps 1, 2, and 4
- Step 1: Row reduction
- Step 2: Column reduction
- Step 4: Adjustment (when Step 3 isn't optimal yet)
"""
import numpy as np

def step1_row_reduction(M):
    """
    Step 1: Row reduction
    Subtract each row's minimum from that row so every row gets at least one 0.
    """
    M = M.astype(float).copy() # work on a float copy so we don't mutate the original
    row_mins = M.min(axis=1, keepdims=True) # shape (n_rows, 1)
    return M - row_mins 

def step2_col_reduction(M):
   """
    Step 2: Column reduction
    Subtract each column's minimum from that column so every column has a 0.
    """
   M = M.astype(float).copy() # work on a float copy so we don't mutate the original
   col_mins = M.min(axis=0, keepdims=True) # shape (1, n_cols)
   return M - col_mins 

 
def step4_adjust_matrix(M, row_covered, col_covered, eps=1e-12):
    """
    Step 4: Adjustment
    When Step 3 isn't optimal yet:
    - Find the smallest uncovered value.
    - Subtract it from all uncovered cells.
    - Add it back to cells at (covered row ∩ covered col).
    """
    M = np.asarray(M, dtype=float).copy()

    row_cov_set = set(int(r) for r in row_covered)
    col_cov_set = set(int(c) for c in col_covered)

    n_rows, n_cols = M.shape
    # Collect all values that are in the uncovered region
    non_zero_element = []
    for r in range(n_rows):
        if r not in row_cov_set:            # only rows that are NOT covered
            for c in range(n_cols):
                if c not in col_cov_set:    # only cols that are NOT covered
                    non_zero_element.append(M[r, c])

    if not non_zero_element:    # no uncovered cells means nothing to adjust
        return M

    min_num = min(non_zero_element)    # smallest uncovered value
    
    # Subtract min from every uncovered cell
    for r in range(n_rows):
        if r not in row_cov_set:
            for c in range(n_cols):
                if c not in col_cov_set:
                    M[r, c] = M[r, c] - min_num
                    
    # Add min to cells at (covered row ∩ covered col)
    for r in row_cov_set:
        for c in col_cov_set:
            M[r, c] = M[r, c] + min_num

    return M
