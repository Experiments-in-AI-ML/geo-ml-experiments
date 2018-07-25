#!/usr/bin/python3

import pandas as pd
import json

df = pd.read_csv('../data/address-geo.json', encoding='latin1', delimiter='|', names=['key','info'])

df['lat'] = df['info'].map(lambda str: json.loads(str)['latitude']) 

df['lon'] = df['info'].map(lambda str: json.loads(str)['longitude'])

df['address'] = df['key'].map(lambda str: str.split(',')[0])

df['zip'] = df['key'].map(lambda str: str.split(',')[3].strip()) 

df = df[['address', 'zip', 'lat', 'lon']]

df.to_csv('address-zip-lat-lon.data.csv', sep=',', encoding='utf-8', index=False)

df = df[['address', 'zip']]

df.to_csv('address-zip.data.csv', sep=',', encoding='utf-8', index=False)
