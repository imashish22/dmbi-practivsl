import pandas as pd

df = pd.read_csv('tree.csv')
print(df.head())

print(df.isnull().sum())