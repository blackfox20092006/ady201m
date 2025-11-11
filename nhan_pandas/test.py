import pandas as pd
pd.options.display.max_rows = 9999
df = pd.read_csv('vgsales.csv')
print(df.head())