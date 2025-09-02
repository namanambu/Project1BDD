import numpy as np

def Line_Check(reduced_matrix):

    
    lines_used = 5

    return lines_used


Line_Check(7)

matrix = np.random.choice(np.arange(15, dtype=np.int32), 
                          size=(4, 4), replace=True)
#print(matrix)
num_cols = matrix.shape[1]
num_rows = matrix.shape[0]



'''
 This section of code is technically someone else's
    part, but I needed to have 0's consistently.
    It DOES NOT WORK!
'''
for row in matrix:  
    row -= min(row)

for col_ind in range (0, num_cols):
    col = matrix[:,col_ind]
    col -= min(col)


# The implementation had it set to use the boolean, but no?
#matrix = (matrix == 0) # Convert the matrix to boolean

zero_inds_r, zero_inds_c = np.where(matrix == 0)

for row_ind in range(0, num_rows):
    if 




print(zero_inds_r, zero_inds_c)
print(matrix)