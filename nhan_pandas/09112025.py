import pandas as pd
class Pandas_analyzer:
    def __init__(self):
        self.pd_cursor = pd.read_csv('vgsales.csv') #đọc file csv
        print(self.pd_cursor)
    def get_first_5_rows(self):
        return self.pd_cursor.head(5) #lấy 5 dòng đầu
a = Pandas_analyzer()
    