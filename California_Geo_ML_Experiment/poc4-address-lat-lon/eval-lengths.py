#!/usr/bin/python3

import sys
import pandas as pd

df = pd.read_csv(sys.argv[1])

n = int(df['address'].str.len().max())

print('max length: ' + str(n))

while n > 0:
    
    df['address'] = df['address'].map(lambda x: str(x)[0:n-1])
    df = df.drop_duplicates();
    
    print(str(n) + ": " + str(len(df.index)))
    
    n = n - 1