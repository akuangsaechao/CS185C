import sys
import pandas as pd
from tqdm import tqdm
from datetime import datetime
from sklearn import tree
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from PIL import Image

# Modify CLI Output of Data frame
pd.set_option('display.height', 1000)
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 10)
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
    labels = 'LOW', 'MEDIUM LOW', 'MEDIUM HIGH', 'HIGH'
    highCount = listValue.count('HIGH')
    mediumHighCount = listValue.count('MEDIUM HIGH')
    mediumLowCount = listValue.count('MEDIUM LOW')
    lowCount = listValue.count('LOW')

    fracs = [lowCount, mediumLowCount, mediumHighCount, highCount]

    the_grid = GridSpec(1, 1)

    plt.subplot(the_grid[0, 0], aspect=1)

    plt.pie(fracs, labels=labels, autopct='%1.1f%%', shadow=True)

    plt.show()


def collect(arg):
    df = pd.read_csv(arg)

    customer_price = {}
    customer_quantity = {}
    with tqdm(total=len(df.index), desc="Populating Coordinate List") as pbar:
        for index, row in df.iterrows():
            pbar.update(1)
            if row['UnitPrice'] > 0 and row['Quantity'] > 0 and row['CustomerID'] > 0:
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
            if index == 150000:
                break

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

    #print(X)
    return X


def calculateY(X):
    Y = []
    for index, x in enumerate(X):
        if x[0] < 125:
            if x[1] >= 1500:
                Y.append('HIGH')
            elif x[1] >= 1000 and x[1] < 1500:
                Y.append('MEDIUM HIGH')
            elif x[1] >= 500 and x[1] < 1000:
                Y.append('MEDIUM LOW')
            else:
                Y.append('LOW')
        elif x[0] >= 125 and x[0] < 250:
            if x[1] >= 1250:
                Y.append('HIGH')
            elif x[1] >= 750 and x[1] < 1250:
                Y.append('MEDIUM HIGH')
            elif x[1] >= 250 and x[1] < 750:
                Y.append('MEDIUM LOW')
            else:
                Y.append('LOW')
        elif x[0] >= 375 and x[0] < 500:
            if x[1] >= 1000:
                Y.append('HIGH')
            elif x[1] >= 500 and x[1] < 1000:
                Y.append('MEDIUM HIGH')
            elif x[1] >= 100 and x[1] < 500:
                Y.append('MEDIUM LOW')
            else:
                Y.append('LOW')
        else:
            if x[1] >= 750:
                Y.append('HIGH')
            elif x[1] >= 500 and x[1] < 750:
                Y.append('MEDIUM HIGH')
            elif x[1] >= 250 and x[1] < 500:
                Y.append('MEDIUM LOW')
            else:
                Y.append('LOW')

    return Y


def check_valueColor(inList):
    colors = []
    for vals in inList:
        if vals == 'HIGH':
            colors.append('#ff0000')
        if vals == 'MEDIUM HIGH':
            colors.append('#ff8c00')
        if vals == 'MEDIUM LOW':
            colors.append('#0072ff')
        if vals == 'LOW':
            colors.append('#2d008e')
    return colors


# Graphs scatter plot given a 2d list with coordinates
def plot_graph(coordinateList, valueList):
    xs = [x[0] for x in coordinateList]
    ys = [x[1] for x in coordinateList]
    colors = []

    for vals in valueList:
        if vals == 'HIGH':
            colors.append('#ff0000')
        if vals == 'MEDIUM HIGH':
            colors.append('#ff8c00')
        if vals == 'MEDIUM LOW':
            colors.append('#0072ff')
        if vals == 'LOW':
            colors.append('#2d008e')
        # if vals == "['HIGH']":
        #     colors.append('#ff0000')
        # if vals == 'MEDIUM HIGH':
        #     colors.append('#ff8c00')
        # if vals == 'MEDIUM LOW':
        #     colors.append('#0072ff')
        # if vals == 'LOW':
        #     colors.append('#2d008e')

    plt.scatter(xs, ys, c=colors)
    #plt.ylim(0, max(ys))
    #plt.xlim(0, max(xs))
    plt.ylim(0, 2500)
    plt.xlim(0, 1000)
    plt.savefig('graph.png', dpi=300)
    return True


X = collect(sys.argv[1])
Y = calculateY(X)

clf = tree.DecisionTreeClassifier()
clf = clf.fit(X, Y)
plot_graph(X, Y)

try:
    img = Image.open('graph.png')
    img.show()
    while True:
        amount = raw_input('Total Amount Spent: ')
        if amount == 'exit':
            break
        while amount.isdigit() != True:
            amount = raw_input('Total Amount Spent (INT ONLY): ')
            if amount == 'exit':
                break

        quantity = raw_input('Quantity Purchased: ')
        if quantity == 'exit':
            break
        while quantity.isdigit() != True:
            quantity = raw_input('Quantity Purchased (INT ONLY): ')
            if quantity == 'exit':
                break

        predList = [amount, quantity]
        pred = clf.predict([[amount, quantity]])
        colors = check_valueColor(pred)
        plt.scatter(amount, quantity, s=100, c=colors)
        plt.ylim(0, 2500)
        plt.xlim(0, 1000)
        plt.savefig('pred.png', dpi=300)
        img = Image.open('pred.png')
        img.show()
        #plt.show()
        print(pred)

except KeyboardInterrupt:
    pass
