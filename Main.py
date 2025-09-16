import Hungarian_Alg_Steps as HAS
import Hungarian_Alg_LineCheck as HAL
import HungarianAlgoImportData as HAID
from datetime import datetime as dt

start = dt.now() # Start timer


df = HAID.import_data('Tests/Large_Test.csv') # A csv file in format from README.md
prepped_df = HAID.prep_data(df)
prepped_array = prepped_df.to_numpy(copy = True)

reduced_matrix = HAS.step2_col_reduction(HAS.step1_row_reduction(prepped_array))

row_lines, col_lines, marked_zeros = HAL.Step_3_Line_Check(reduced_matrix)

while len(row_lines) + len(col_lines) != len(reduced_matrix):
    print("step4")
    new_matrix = HAS.step4_adjust_matrix(reduced_matrix, row_lines, col_lines)
    row_lines, col_lines, marked_zeros = HAL.Step_3_Line_Check(new_matrix)

assignments = HAL.STEP5_find_solution(marked_zeros)
num_to_match = len(HAID.get_doctors(df))
matches_df = HAL.match_residents(assignments, df)

# How much time has elapsed to end of actual algorithm run
end = dt.now()

# Dropping sorting by hospital and dropping the row indices for style
matches_df = matches_df.sort_values("Hospital Position")
matches_df = matches_df.reset_index(drop=True)



matches_numeric = HAL.match_residents_numeric(assignments, prepped_df, num_to_match)
score, max_score = HAID.get_score(prepped_df, matches_numeric)
print(matches_df)
print(f'\nWe have achieved a solution of: {(1 - score / max_score) * 100:.1f}%\n which took {end-start}')

#matches_df.to_csv("Test_Result.csv") # Uncomment this if you'd like the output in csv format





