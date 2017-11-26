import sys
import pandas as pd
from tqdm import tqdm

# Allows all 8 columns to be displayed in cli
pd.set_option('display.height', 1000)
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


def unique_buyer(arg):
    df = pd.read_csv(arg)

    add = []

    with tqdm(total=len(df.index)) as pbar:
        for index, row in df.iterrows():
            # print(row['UnitPrice'], row['CustomerID'])
            if row['UnitPrice'] == 4.15:
                add.append(row['CustomerID'])
            pbar.update(1)

    print(str(len(set(add))) + " Unique Buyers")


unique_buyer(sys.argv[1])