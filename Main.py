import numpy as np
import pandas as pd 
import Hungarian_Alg_Steps as HAS
import Hungarian_Alg_LineCheck as HAL
import HungarianAlgoImportData as HAID

df = HAID.import_data('BDD Test.csv')
hi = HAID.get_hospital_info(df)
prepped_df = HAID.prep_data(df)


prepped_array = prepped_df.to_numpy(copy = True)

reduced_matrix = HAS.step2_col_reduction(HAS.step1_row_reduction(prepped_array))

row_lines, col_lines, marked_zeros = HAL.Step_3_Line_Check(reduced_matrix)

while len(row_lines) + len(col_lines) != len(reduced_matrix):
    new_matrix = HAS.step4_adjust_matrix(row_lines, col_lines)
    row_lines, col_lines, marked_zeros = HAL.Step_3_Line_Check(new_matrix)

#step_5_blabla()
print("Where the func the function!?")





