import csv
import sys
import pandas as pd
import numpy as np

df = pd.read_csv(sys.argv[1])
print(df)

print("exit successful")
