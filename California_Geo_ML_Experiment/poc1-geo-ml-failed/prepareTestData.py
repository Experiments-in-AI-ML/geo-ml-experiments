
# coding: utf-8

# In[2]:


import pandas as pd
data = pd.read_csv("reference.csv")
input = pd.read_csv("input.csv")

#prepare keys
data.columns = map(lambda x:x.lower(),data.columns)
print "convert city...will take some time"
data.city = data.city.str.upper()
print "convert state...will take some time"
data.state = data.state.str.upper()
print "convert address...will take some time"
data.address = data.address.str.upper()

# merge input and reference
datamerge = pd.merge(data, input, on=['state', 'city',"zip","address"])

print "Test data is ready"

