import pandas as pd
pd.options.display.max_rows = 9999      
pd.options.display.max_columns = None  
pd.options.display.width = 0           
pd.options.display.max_colwidth = None
df = pd.read_csv('vgsales.csv')
print(df.head())