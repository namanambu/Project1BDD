import pandas as pd
import numpy as np


def import_data(file):
    raw_data = pd.read_csv(file)
    return raw_data

def get_hospital_info(df):
    """
    Grabs the number of positions at each hospitals
    Args:
        df (DataFrame): the raw imported data from csv file

    Returns:
        hospital (number of hospitals, 0): : the hos
    """
    hospital_info = df[:1]
    hospital_info = hospital_info.drop('Hospital', axis= 1)
    return hospital_info



def get_doctors(df):
    doctor_info = df['Hospital']
    doctor_info = doctor_info.drop(0)

    return doctor_info
    

def prep_data_step1(df):
    #clean the number of positions out of the dataframe
    prepped_data = df[1:]
    #drop the names of the doctors
    prepped_data = prepped_data.drop('Hospital', axis = 1)
    
    return prepped_data

def prep_data(raw_data):
    #for the distinguishign the position
    position_lettering  = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
    #number of positions available
    hos_info = get_hospital_info(raw_data)
    #the starting data
    base_data = prep_data_step1(raw_data)
    #go through each hospital
    for column in hos_info.columns:
        #grab the number of positions for each hospital
        num_positions = int(hos_info.loc[0, column])
        #only change if more than one position
        if num_positions > 1:
            
            for i in range(num_positions - 1):
                base_data[column + position_lettering[i+1]] = base_data[column]
            base_data = base_data.rename(columns={column: column + position_lettering[0]})
    #pad to make square
    num_rows, num_cols = base_data.shape
    target_dim = max(num_rows, num_cols)

    if num_rows < target_dim:
    # Create a new DataFrame of zeros with the required number of rows
        zero_rows_to_add = target_dim - num_rows
        zero_padded_rows = pd.DataFrame(0, index=range(zero_rows_to_add), columns=base_data.columns)
        base_data = pd.concat([base_data, zero_padded_rows], ignore_index=True)
    
    if num_cols < target_dim:
    # Create new columns filled with zeros
        for i in range(num_cols, target_dim):
            #theres more doctors than positions
            base_data['No Match ' + position_lettering[i]] = 0
    return base_data




def get_score (prepped_df, solution_matrix):
    #get the score from what the ranking was of the hospital the doctor got
    score = 0
    for index, row in solution_matrix.iterrows():
        doctor = row['Doctor']
        hos = row['Hospital Position']
        score += prepped_df.at[doctor, hos]
    #get the max score that could be achieved
    max = prepped_df.max(axis=1)
    max_total = max.sum()
    return score, max_total
    


    


if __name__ == "__main__":
    df = import_data('Test_VarB.csv')
    hi = get_doctors(df)
    lo = get_hospital_info(df)
    print(prep_data_step1(df))
    print(prep_data(df))
