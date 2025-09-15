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
<<<<<<< HEAD


"""
=======
    
def step4_adjust_matrix(M, row_covered, col_covered, eps=1e-12):
    M = np.asarray(M, dtype=float).copy()

    row_cov_set = set(int(r) for r in row_covered)
    col_cov_set = set(int(c) for c in col_covered)

    n_rows, n_cols = M.shape

    non_zero_element = []
    for r in range(n_rows):
        if r not in row_cov_set:
            for c in range(n_cols):
                if c not in col_cov_set:
                    non_zero_element.append(M[r, c])

    if not non_zero_element:
        return M

    min_num = min(non_zero_element)

    for r in range(n_rows):
        if r not in row_cov_set:
            for c in range(n_cols):
                if c not in col_cov_set:
                    M[r, c] = M[r, c] - min_num

    for r in row_cov_set:
        for c in col_cov_set:
            M[r, c] = M[r, c] + min_num

    return M


'''def step4_adjust_matrix(M, row_covered, col_covered, eps=1e-12):
  """
>>>>>>> cbbe0ec6d295174dfafbf327b5fb6de38ebb1555
    Step 4: Only run this if Step 3 wasn't optimal yet.
    Make new zeros in places that aren't covered by any line.
        1) Find m = smallest *positive* uncovered finite value.
        2) Subtract m from all uncovered cells.
        3) Add m to cells at (covered row ∩ covered col).
    Notes:
        - If no positive uncovered values exist (uncovered region all zeros),
          return and let Step 3 add another covering line.
        - Inputs are coerced to boolean masks; tiny float noise is zeroed.
    """
def step4_adjust_matrix(M, row_covered, col_covered, eps=1e-12):
  
    # 1) normalize
    M = np.asarray(M, dtype=float).copy()
    row_covered = np.asarray(row_covered, dtype=bool).reshape(-1)
    col_covered = np.asarray(col_covered, dtype=bool).reshape(-1)

    '''if M.shape != (row_covered.size, col_covered.size):
        raise ValueError(
            f"Shape mismatch: M{M.shape} vs row_covered{row_covered.shape} / col_covered{col_covered.shape}"
        )'''

    # 2) uncovered region mask
    uncovered = (~row_covered)[:, None] & (~col_covered)[None, :]


    if not np.any(uncovered):
        print("none found")
        return M

    # 3) pick smallest *positive* uncovered finite value
    finite = np.isfinite(M)
    candidates = uncovered & finite & (M > eps)
    if not np.any(candidates):
        # all uncovered entries are already zero (or non-finite)
        return M

    m = M[candidates].min()
    print

    # 4) update
    M[uncovered] -= m
    intersections = (row_covered[:, None] & col_covered[None, :])
    if np.any(intersections):
        M[intersections] += m

    # 5) clean float fuzz
    M[np.abs(M) < eps] = 0.0
    return M'''
