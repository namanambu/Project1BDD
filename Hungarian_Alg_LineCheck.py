import numpy as np
import pandas as pd

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

'''
    * Function for determining the optimal assignment of rows (doctors) to columns (hospitals) 
    * based on the indices of zeros in a cost matrix. The goal is to assign rows to columns while meeting
    * constraints, such as assigning only unmatched rows and columns at each step to avoid repeats.
    * Let R, C, and Z be integers such that 0 </= int </= N (total rows, columns, and zeros in matrix).
    * @param "zero_inds" 2D list of indices (Z x 2) of all zeros in the matrix. Each entry is [row_index, col_index].
    * @return "assignments" 2D list of pairs [row, col] representing the solution to the assignment problem.
    '''
def STEP5_find_solution(zero_inds):
    
    
    rows = []
    cols = []

    # Separate the indices into their column and row components
    for i in range(len(zero_inds)):
        rows.append(zero_inds[i][0])
        cols.append(zero_inds[i][1])

    # Vars to track progress
    assignments = []
    matched_rows = []
    matched_cols = []
    unmatched_rows = []

    round_min = 1 # The amount of 0s a row can have to be match eligible this time
    for i in range(len(zero_inds)):
        row = rows[i]
        if sum(rows == row) == 1: # Then proceed to assign them
            assignments.append([row, cols[i]])
            matched_rows.append(row)
            matched_cols.append(cols[i])
        else: # They have too many options --> wait
            unmatched_rows.append(row)
            if sum(rows == row) < (round_min + 1): 
                round_min = sum(rows == row)
            else:
                round_min += 1

    new_matches = 0
    while len(set(unmatched_rows)) != new_matches: # Set because we'll have repeats
        for row in unmatched_rows:
            if row not in matched_rows:
                indices = [i for i in range(len(rows)) if rows[i] == row]
                for index in indices:
                    if (sum(rows == row) <= round_min) and (cols[index] not in matched_cols): # Prevent more than 1 match per place
                        assignments.append([row, cols[index]])
                        matched_rows.append(row)
                        matched_cols.append(cols[index])
                        new_matches += 1
                        unmatched_rows.remove(row)
                        break
        rows_with_zeros = [row for row in unmatched_rows if rows.count(row) > 0]
        if rows_with_zeros:  # If unmatched rows remain
            round_min = min(rows.count(row) for row in rows_with_zeros)  # Find the next lowest threshold
        else:
            break  # This is actually the only way the loop ends
                    
                

    return assignments

'''
    * Function iteratively processes assignment pairs from Step 5 and maps them to doctors and hospital positions
    * from the prepped, padded square cost matrix. Each assignment identifies the matched doctor and hospital index.
    * Let R and C be integers such that 0 </= int </= M (number of doctors and positions in the prepped matrix)
    * @param "assignments" 2D list or np.ndarray where each pair (row, col) represents a match of doctor to hospital
    * @param "prepped_data" pandas DataFrame for the square, padded cost matrix with rows as doctors (MxN)
    * @param "num_doctors" integer with the number of doctors we are trying to match
    * @return "matches_df" pandas DataFrame with matched doctors and hospital positions 
    *                      Columns: ['Doctor', 'Hospital Position']
    '''
def Match_Residents(assignments, prepped_data, num_doctors):

    doctor_names = list(prepped_data.index[:num_doctors])  # First `num_doctors` rows, rest are extra
    hospital_names = list(prepped_data.columns) 

    # Filter assignments to only include actual doctors (rows < num_doctors)
    filtered_assignments = [pair for pair in assignments if pair[0] < num_doctors]

    # Prepare list of matches
    matches = []
    for row, col in filtered_assignments:
        doctor = doctor_names[row]  # Map row index to actual doctor name
        hospital = hospital_names[col]  # Map column index to hospital position name

        # Append to matches list
        matches.append({"Doctor": doctor, "Hospital Position": hospital})

    # Convert matches list to a DataFrame
    matches_df = pd.DataFrame(matches)

    return matches_df