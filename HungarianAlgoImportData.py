import pandas as pd


def import_data(file):
    raw_data = pd.read_csv(file)
    return raw_data


if __name__ == "__main__":
    df = import_data('BDD Test.csv')
