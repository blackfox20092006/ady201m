import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error
import sqlite3, os, ffmpeg
import pandas as pd
import numpy as np
from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())
root = os.getenv('ROOT')
data_path = os.path.join(root, 'data_understand_and_preprocessing', 'data', 'Analysis_result.csv')
df = pd.read_csv(data_path)

df.columns = df.columns.str.strip()
x = df[['optical_flow','frame_diff_mean','frame_diff_var','blur','brightness','contrast']]
y = df['violence_probability']

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=199)
scaler = StandardScaler()
x_train = scaler.fit_transform(x_train)
x_test = scaler.transform(x_test)

model = LinearRegression().fit(x_train, y_train)
y_pred = model.predict(x_test)

print("R2:", r2_score(y_test, y_pred))
print("MAE:", mean_absolute_error(y_test, y_pred))
