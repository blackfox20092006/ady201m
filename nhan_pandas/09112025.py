import pandas as pd
class Pandas_analyzer:
    def __init__(self):
        self.pd_cursor = pd.read_csv('vgsales.csv')
    def get_first_5_rows(self):
        print(self.pd_cursor.head(5))
    def count_null(self):
        print(self.pd_cursor.isnull().sum())
    def get_column_name(self):
        print([i for i in self.pd_cursor.keys()])
    def get_unique_game_types_in_genre(self):
        print(list(set(self.pd_cursor['Genre'])))
    def get_describe_for_columns(self):
        print(self.pd_cursor.describe())
    def get_game_with_max_global_sales(self):
        max_value = max(list(self.pd_cursor['Global_Sales']))
        data = []
        i = 0
        while True:
            try:
                if self.pd_cursor.loc[i]['Global_Sales'] == max_value:
                    data += [self.pd_cursor.loc[i]['Name']]
                i += 1
            except:
                break
        print(list(set(data)))
    def get_earliest_and_latest_pulish(self):
        print(int(self.pd_cursor['Year'].max()))
        print(int(self.pd_cursor['Year'].min()))
    def 
a = Pandas_analyzer()
a.get_earliest_and_latest_pulish()