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

def step4_adjust_matrix(M, row_covered, col_covered):
  """
    Step 4: Only run this if Step 3 wasn't optimal yet.
    Make new zeros in places that aren't covered by any line.
      - find the smallest uncovered value m
      - subtract m from all uncovered cells
      - add m to cells at COVERED row ∩ COVERED col
    Then go back to Step 3 and try again.
    """
    M = M.astype(float).copy()
    # cells with NO row line and NO column line = "uncovered"
    uncovered = (~row_covered)[:, None] & (~col_covered)[None, :]
    if not np.any(uncovered):
        return M  # nothing to adjust
    
    m = M[uncovered].min() # m = smallest number sitting in the uncovered region

    # subtract from uncovered entries, at least one of them becomes 0
    M[uncovered] -= m

    # add to intersections of covered rows & covered columns
    intersections = (row_covered[:, None] & col_covered[None, :])
    M[intersections] += m

    return M
