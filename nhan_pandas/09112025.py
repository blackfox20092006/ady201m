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
    def get_game_after_2010(self):
        print(self.pd_cursor[self.pd_cursor['Year']>2010])
    def get_top10_game_at_NASales(self):
        print(self.pd_cursor.sort_values(by=['NA_Sales']).tail(10))
    def get_action_game_more_10m(self):
        print(self.pd_cursor[(self.pd_cursor['Global_Sales']>10) & (self.pd_cursor['Genre']=='Action')])
    def get_game_jp_bigger_than_eu(self):
        print(self.pd_cursor[(self.pd_cursor['JP_Sales']) > (self.pd_cursor['EU_Sales'])])
    def sort_global_sales_descending(self):
        print(self.pd_cursor.sort_values(by=['Global_Sales']))
a = Pandas_analyzer()
a.sort_global_sales_descending()