#!/usr/bin/python3

import pandas as pd
reference = pd.read_csv('../data/reference.csv', encoding='latin1')
input = pd.read_csv('../data/input.csv', encoding='latin1')

#prepare keys
reference.columns = map(lambda x:x.lower(),reference.columns)
reference.city = reference.city.str.upper()
reference.state = reference.state.str.upper()
reference.address = reference.address.str.upper()

# merge input and reference
datamerge = pd.merge(input, reference, on=['address', 'zip'], how='left')

datamerge = datamerge[['address', 'zip', 'latitude', 'longitude']]
#datamerge.drop_duplicates()

datamerge.to_csv('../data/address-zip-geo.csv', sep=',', encoding='utf-8')

# conclusion, this data is garbage. Only 9,000 matches