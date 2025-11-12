import pandas as pd
df = pd.read_excel('doanh_thu_cong_ty.xlsx')
df['Lợi nhuận'] = df['Doanh thu (VNĐ)'] - df['Chi phí (VNĐ)']
print(df.groupby('Mã công ty')['Lợi nhuận'].sum().head(6))