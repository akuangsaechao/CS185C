import csv
import sys

myFile = open(sys.argv[1])
csv_f = csv.reader(myFile)

for row in csv_f:
    print row[2]
