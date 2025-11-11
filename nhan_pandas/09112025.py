'''
1-10.
Đọc file CSV vào DataFrame.

Hiển thị 5 dòng đầu tiên của dữ liệu.

Kiểm tra số lượng dòng và cột.

Xem kiểu dữ liệu của từng cột.

Đếm số lượng giá trị null ở mỗi cột.

Liệt kê tên tất cả các cột.

Lấy danh sách các thể loại game (cột Genre) không trùng lặp.

Xem thống kê mô tả (describe()) cho các cột số.

Tìm game có doanh số toàn cầu (Global_Sales) cao nhất.

Tìm năm phát hành sớm nhất và muộn nhất.

11-20
Lọc các game phát hành sau năm 2010.

Lấy top 10 game có doanh số tại Bắc Mỹ cao nhất.

Tìm các game thuộc thể loại “Action” có doanh số toàn cầu > 10 triệu.

Đếm bao nhiêu game có doanh số tại Nhật lớn hơn tại châu Âu.

Sắp xếp DataFrame theo Global_Sales giảm dần.

Lọc ra tất cả game được phát hành bởi Nintendo.

Tìm doanh số trung bình tại Bắc Mỹ của từng Platform.

Lọc ra các game có doanh số tại châu Âu > 1 triệu nhưng tại Nhật < 0.1 triệu.

Đếm số lượng game theo từng năm (Year).

Tìm 5 game có doanh số “Other_Sales” thấp nhất.

21-30
Tính tổng doanh số toàn cầu của mỗi Genre.

Tính trung bình Global_Sales của từng Publisher.

Tính tổng doanh số theo từng năm (Year).

Với mỗi Platform, tìm game có doanh số toàn cầu cao nhất.

Đếm số lượng game được phát hành bởi mỗi nhà phát hành (Publisher).

Tính doanh số trung bình theo từng Genre và Year.

Với mỗi Genre, tìm năm có tổng doanh số cao nhất.

Vẽ biểu đồ cột so sánh doanh số trung bình giữa các Genre.

Tìm top 5 Publisher có tổng doanh số cao nhất mọi thời đại.

Vẽ biểu đồ đường biểu diễn tổng doanh số toàn cầu qua các năm.
'''
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
        print(self.pd_cursor.sort_values(by=['Global_Sales'], ascending=False))
    def get_Nintendo_pulisher(self):
        print(self.pd_cursor[self.pd_cursor['Publisher']=='Nintendo'])
    def get_sum_by_platform(self):
        print(self.pd_cursor.groupby('Platform')['Global_Sales'].max())
    def get_avg_per_platform_in_NA_Sales(self):
        print(self.pd_cursor.groupby('Platform')['NA_Sales'].mean())
    def q18(self):
        print(self.pd_cursor[(self.pd_cursor['EU_Sales']>1) & (self.pd_cursor['JP_Sales']<0.1)])
    def q19(self):
        print(self.pd_cursor.groupby('Year').count())
    def q20(self):
        print(self.pd_cursor.sort_values(by=['Other_Sales'], ascending=True).head(5))
    def q21(self):
        print(self.pd_cursor.groupby('Genre').sum()['Global_Sales'])
    def q22(self):
        print(self.pd_cursor.groupby('Publisher')['Global_Sales'].mean())
    def q23(self):
a = Pandas_analyzer()
a.q22()