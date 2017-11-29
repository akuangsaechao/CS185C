import sys
import pandas as pd
from tqdm import tqdm
from datetime import datetime
from sklearn import tree
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

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
            if row['UnitPrice'] == 5.0:
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


def pie_distribution(listValue):
    labels = 'Rich', 'Poor More 50', 'Rich Less 50', 'Poor'
    richCount = listValue.count('Rich')
    poor50Count = listValue.count('Poor More 50')
    rich50Count = listValue.count('Rich Less 50')
    poor = listValue.count('Poor')

    fracs = [richCount, poor50Count, rich50Count, poor]

    the_grid = GridSpec(1, 1)

    plt.subplot(the_grid[0, 0], aspect=1)

    plt.pie(fracs, labels=labels, autopct='%1.1f%%', shadow=True)

    plt.show()

def collect(arg):
    df = pd.read_csv(arg)

    customer_price = {}
    customer_quantity = {}
    with tqdm(total=len(df.index)) as pbar:
        for index, row in df.iterrows():
            pbar.update(1)
            # print(row['UnitPrice'], row['CustomerID'])
            if customer_price.has_key(row['CustomerID']):
                price = customer_price.get(row['CustomerID'])
                price.append(row['UnitPrice'])
                customer_price[row['CustomerID']] = price
                quantity = customer_quantity.get(row['CustomerID'])
                quantity.append(row['Quantity'])
                customer_quantity[row['CustomerID']] = quantity
            else:
                price = []
                price.append(row['UnitPrice'])
                customer_price[row['CustomerID']] = price
                quantity = []
                quantity.append(row['Quantity'])
                customer_quantity[row['CustomerID']] = quantity
            #if index==10000:
                #break

    X = []
    customerTotalPrice = {}
    for key, value in customer_price.iteritems():
        totalPrice = 0
        for price in value:
            totalPrice += price
        customerTotalPrice[key] = totalPrice

    customerTotalQuantity = {}
    for key, value in customer_quantity.iteritems():
        totalQuantity = 0
        for quantity in value:
            totalQuantity += quantity
        customerTotalQuantity[key] = totalQuantity

    for key, value in customerTotalQuantity.iteritems():
        point = []
        point.append(customerTotalPrice.get(key))
        point.append(value)
        X.append(point)
    return X

# Graphs scatter plot given a 2d list with coordinates
def plot_graph(coordinateList):
    xs = [x[0] for x in coordinateList]
    ys = [x[1] for x in coordinateList]
    plt.scatter(xs, ys)
    plt.ylim(0, 2000)
    plt.xlim(1, 5000)
    plt.savefig('graph.png')
    plt.show()

X = collect(sys.argv[1])
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

# Decision Tree Prediction
#clf = tree.DecisionTreeClassifier()
#clf = clf.fit(X, Y)
#clf.predict([[80, 10]])

plot_graph(X)

