import numpy as np

'''
   * Helper function to systematically mark the first zero occurence
   * In each row.  Starting from smallest num of zeros.
   * @param "zero_mat" Copy of boolean matrix (N x N)
   * @return "mark_zero" empty 1D np array to contain set of marked zeros
   '''
def min_zero_row(zero_mat, mark_zero):
    
    min_row = [99999, -1] # [num_zeros, row_ind]

    for row_num in range(zero_mat.shape[0]): 
        if np.sum(zero_mat[row_num] == True) > 0 and min_row[0] > np.sum(zero_mat[row_num] == True):
            min_row = [np.sum(zero_mat[row_num] == True), row_num]

    # Marked the specific row and column as False
    zero_index = np.where(zero_mat[min_row[1]] == True)[0][0]
    mark_zero.append((min_row[1], zero_index)) # Mark the first zero in this row
    
    # Make all values in corresponding row and column False to proceed
    zero_mat[min_row[1], :] = False 
    zero_mat[:, zero_index] = False

'''
   * Function iteratively determines the minimal number of "lines" 
   * to be made in the reduced cost matrix in order to mark all zeros.
   * Let R, C, and Z be integers such that 0 </= int </= N
   * @param "mat" 2D np array for the reduced, square cost matrix (N x N)
   * @return "marked_rows" 1D np array of rows through which a "line" is made (len = R)
   * @return "marked_cols" 1D np array of columns through which a "line" is made (len = C)
   * @return "marked_zero" 2D np array of indices of all zeros in reduced matrix (Z x 2)
   '''
def Step_3_Line_Check(mat):

    # Matrix --> Boolean Matrix (0 True, else False)
    current_mat = mat
    zero_bool_mat = (current_mat == 0)
    zero_bool_mat_copy = zero_bool_mat.copy()

    # Find the indices of zeros in the matrix (only the first in each row)
    marked_zero = []
    while (True in zero_bool_mat_copy):
        min_zero_row(zero_bool_mat_copy, marked_zero)

    # Separate row and col indices for later use
    marked_zero_row = []
    marked_zero_col = []
    for i in range(len(marked_zero)):
        marked_zero_row.append(marked_zero[i][0])
        marked_zero_col.append(marked_zero[i][1])

    # Collect number of rows with 0s
    non_marked_row = list(set(range(current_mat.shape[0])) - set(marked_zero_row))
    
    marked_cols = []
    change_made = True
    while change_made: # If we hit a run that changes nothing --> STOP
        change_made = False
        for curr_row in range(len(non_marked_row)):
            row_array = zero_bool_mat[non_marked_row[curr_row], :]
            for curr_col in range(row_array.shape[0]):
                # In each row, we check each bool_val for unmrked zeros (Trues)
                if row_array[curr_col] == True and curr_col not in marked_cols:
                    # If we missed smth, we add to our marked cols and keep going
                    marked_cols.append(curr_col)
                    change_made = True

        for row_num, col_num in marked_zero:
            # Update the set of non-marked rows for reduction to minimal set
            if row_num not in non_marked_row and col_num in marked_cols:
                non_marked_row.append(row_num)
                change_made = True
    # Reduce set of rows down based on non-marked rows
    marked_rows = list(set(range(mat.shape[0])) - set(non_marked_row))
    
    return np.array(marked_rows), np.array(marked_cols), np.array(marked_zero)


matrix = np.random.choice(np.arange(15, dtype=np.int32), 
                          size=(4, 4), replace=True)
num_cols = matrix.shape[1]
num_rows = matrix.shape[0]


'''
 This section of code is technically someone else's
    part, but I needed to have 0's consistently.
    It DOES NOT WORK!

for row in matrix:  
    row -= min(row)

for col_ind in range (0, num_cols):
    col = matrix[:,col_ind]
    col -= min(col)


[row_lines, col_lines, marked_zeros] = Step_3_Line_Check(matrix)

#print(row_lines, col_lines, marked_zeros)

if len(row_lines) + len(col_lines) == len(matrix):  # Skip to Step 5
    #step_5_blabla()
    print("step5")
else: # Go to Step 4
    #step4_adjust_matrix(matrix, row_lines, col_lines)
    print("step4")


'''