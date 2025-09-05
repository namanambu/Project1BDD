import pandas as pd


def import_data(file):
    raw_data = pd.read_csv(file)
    return raw_data

def get_hospital_info(df):
    """
    Grabs the number of positions at each hospitals
    Args:
        df (DataFrame): the raw imported data from csv file

    Returns:
        hospital (number of hospitals +1, 0): : the hos
    """
    hospital_info = df[:1]
    return hospital_info

def prep_data(df):
    #clean the number of positions out of the dataframe
    prepped_data = df[1:]
    #drop the names of the doctors
    prepped_data = prepped_data.drop('Hospital', axis = 1)
    prepped_data['hii'] = prepped_data['H1']

    return prepped_data


if __name__ == "__main__":
    df = import_data('BDD Test.csv')
    hi = get_hospital_info(df)
    print(prep_data(df))
