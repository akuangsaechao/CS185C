import sys
import pandas as pd
from tqdm import tqdm
from datetime import datetime

import numpy as np
from sklearn import tree
import matplotlib.pyplot as plt

# Modify CLI Output of Data frame
pd.set_option('display.height', 1000)
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 7)
pd.set_option('display.width', 1000)


# Sum of unique buyer ID
def unique_buyer(arg):
    df = pd.read_csv(arg)

    add = []

    with tqdm(total=len(df.index)) as pbar:
        for index, row in df.iterrows():
            # print(row['UnitPrice'], row['CustomerID'])
            if row['UnitPrice'] == 9999999:
                add.append(row['CustomerID'])
            pbar.update(1)

    return str(len(set(add))) + " Unique Buyers"


# Print current data frame
def print_table(arg):
    print(pd.read_csv(arg))


# return pandas dataframe of csv
def csv_dataframe(arg):
    return pd.read_csv(arg)


# Converts excel float time to datetime object
def time_converter(serial):
    seconds = (serial - 25569) * 86400.0
    return datetime.utcfromtimestamp(seconds)


# Table where customerID are row and each column is a different product code
# Values for the table are the quantity purchased of specified product
def pivot_product(arg):
    df = pd.read_csv(arg)
    table = df.pivot_table(index=["CustomerID"], columns=["UnitPrice"], values="Quantity")
    table = table.fillna(0)
    return table


X = [[100, 10],[5, 50], [10, 100]]
Y = []

for index, x in enumerate(X):
    if x[0] >= 50:
        if x[1] >= 5:
            Y.append('rich')
        else:
            Y.append('poor more 50')
    else:
        if x[1] >= 5:
            Y.append('rich less 50')
        else:
            Y.append('poor')

clf = tree.DecisionTreeClassifier()
clf = clf.fit(X, Y)
#print(clf.predict([[80, 10]]))

#print(csv_dataframe(sys.argv[1]))

print(unique_buyer(sys.argv[1]))

#print(pivot_product(sys.argv[1]))
#print_table(sys.argv[1])