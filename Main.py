import numpy as np
import pandas as pd 
import Hungarian_Alg_Steps as HAS
import Hungarian_Alg_LineCheck as HAL
import HungarianAlgoImportData as HAID

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






df = HAID.import_data('Test_VarB.csv')
hi = HAID.get_hospital_info(df)
prepped_df = HAID.prep_data(df)
prepped_array = prepped_df.to_numpy(copy = True)

reduced_matrix = HAS.step2_col_reduction(HAS.step1_row_reduction(prepped_array))

row_lines, col_lines, marked_zeros = HAL.Step_3_Line_Check(reduced_matrix)

while len(row_lines) + len(col_lines) != len(reduced_matrix):
    new_matrix = HAS.step4_adjust_matrix(row_lines, col_lines)
    row_lines, col_lines, marked_zeros = HAL.Step_3_Line_Check(new_matrix)

assignments = HAL.STEP5_find_solution(marked_zeros)
num_to_match = len(HAID.get_doctors(df))
matches_df = HAL.match_residents(assignments, df)
matches_df = matches_df.sort_values("Doctor")

matches_numeric = Match_Residents(assignments, prepped_df, num_to_match)
score, max_score = HAID.get_score(prepped_df, matches_numeric)
print(matches_df)
print(f'\nWe have achieved a solution of: {(1 - score / max_score) * 100:.1f}%')





