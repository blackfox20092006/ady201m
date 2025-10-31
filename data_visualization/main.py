import matplotlib.pyplot as plt
import seaborn as sns
import sys
import sqlite3, os, ffmpeg
import pandas as pd
import numpy as np
from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())
root = os.getenv('ROOT')
data_path = os.path.join(root, 'data_understand_and_preprocessing', 'data', 'data.db')


class VideoAnalysis:
    
    def __init__(self, data):
        self.data = data
        self.df = None
        sns.set_theme(style="whitegrid")
        if not os.path.exists(self.data):
             print(f"Error: Database file not found at {self.data}")
             sys.exit(1)

    def load_data(self):
        print("Loading data...")
        try:
            conn = sqlite3.connect(self.data)
            query = """
            SELECT 
                ar.video_id,
                ar.violence_probability,
                ar.frame_diff_mean,
                ar.frame_diff_var,
                ar.blur,
                ar.brightness,
                ar.contrast,
                ar.optical_flow,
                m.resolution
            FROM Analysis_result AS ar
            LEFT JOIN Metadata AS m ON ar.video_id = m.video_id
            """
            self.df = pd.read_sql_query(query, conn)
            conn.close()
            print(f"Load successful. Total records: {len(self.df)}")
        except Exception as e:
            self.df = None
            print(f"Fatal error: Could not load data from {self.data}. Error: {e}")
            sys.exit(1)
            
    def prepare_data(self):
        if self.df is None:
            return
        self._preprocess_resolution()

    def _preprocess_resolution(self):
        res_h = self.df['resolution'].astype(str).str.extract(r'x(\d+)', expand=False)
        res_height = pd.to_numeric(res_h, errors='coerce')
        bins = [0, 480, 720, 1080, np.inf]
        labels = ['<480p', '720p', '1080p', '1440p+']
        self.df['res_bucket'] = pd.cut(res_height, bins=bins, labels=labels, include_lowest=True)

    def plot_correlation_heatmap(self):
        if self.df is None: 
            return
        
        features = [
            'violence_probability',
            'frame_diff_mean', 
            'frame_diff_var', 
            'blur', 
            'brightness', 
            'contrast', 
            'optical_flow'
        ]
        
        plt.figure(figsize=(10, 8))
        sns.heatmap(
            self.df[features].corr(method='pearson'), 
            annot=True, 
            fmt=".2f",
            vmin=-1, 
            vmax=1, 
            cmap='vlag', 
            square=True, 
            cbar_kws={"shrink": .8}
        )
        
        plt.title('HEATMAP: Correlation Between Features', fontsize=16)
        plt.tight_layout()
        plt.savefig("correlation_heatmap.png")
        plt.close()
        print("Saved correlation_heatmap.png")

    def plot_probability_distribution(self):
        if self.df is None: 
            return
        
        plt.figure(figsize=(10, 6))
        sns.histplot(
            data=self.df,
            x='violence_probability',
            bins=20, 
            kde=True 
        )
        plt.title('Histogram of violence_probability', fontsize=16)
        plt.xlabel('Violence Probability')
        plt.ylabel('Video Count')
        plt.savefig("probability_distribution.png")
        plt.close()
        print("Saved probability_distribution.png")

    def plot_trend_line(self):
        if self.df is None: 
            return

        df_temp = self.df.copy()
        df_temp['frame_diff_bin'] = pd.cut(df_temp['frame_diff_mean'], bins=12)
        line_data = df_temp.groupby('frame_diff_bin', observed=True)['violence_probability'].mean().reset_index()
        line_data['frame_diff_mid'] = line_data['frame_diff_bin'].apply(lambda x: x.mid).astype(float)

        plt.figure(figsize=(10, 6))
        sns.lineplot(
            data=line_data,
            x='frame_diff_mid',
            y='violence_probability',
            marker='o'
        )
        plt.title('Line Chart: Trend of Average Violence Probability by Frame Diff Mean', fontsize=16)
        plt.xlabel('Frame Diff Mean (Binned)')
        plt.ylabel('Average Violence Probability')
        plt.savefig("trend_line.png")
        plt.close()
        print("Saved trend_line.png")

    def plot_blur_by_resolution(self):
        if self.df is None or 'res_bucket' not in self.df.columns:
            return

        plt.figure(figsize=(10, 8))
        box_data = self.df[['blur', 'res_bucket']].dropna()
        
        sns.boxplot(data=box_data, x='res_bucket', y='blur')
        sns.stripplot(
            data=box_data, 
            x='res_bucket', 
            y='blur', 
            size=3, 
            color="black", 
            alpha=0.4
        )
        
        plt.title('BOX PLOT: blur by res_bucket', fontsize=16)
        plt.xlabel('Resolution Bucket')
        plt.ylabel('Blur')
        plt.tight_layout()
        plt.savefig("blur_by_resolution.png")
        plt.close()
        print("Saved blur_by_resolution.png")

    def plot_scatter_example(self):
        if self.df is None: 
            return
        
        plt.figure(figsize=(10, 6))
        sns.scatterplot(
            data=self.df,
            x='optical_flow',
            y='frame_diff_mean',
            alpha=0.6,
            s=35
        )
        plt.title('SCATTER PLOT: optical_flow vs frame_diff_mean', fontsize=14)
        plt.xlabel('Optical Flow')
        plt.ylabel('Frame Diff Mean')
        plt.tight_layout()
        plt.savefig("scatter_example.png")
        plt.close()
        print("Saved scatter_example.png")

if __name__ == "__main__":
    
    DATA_DB_PATH = data_path

    analyzer = VideoAnalysis(data=DATA_DB_PATH)
    analyzer.load_data()
    
    if analyzer.df is not None:
        analyzer.prepare_data()

        analyzer.plot_correlation_heatmap()
        analyzer.plot_scatter_example()
        analyzer.plot_trend_line()
        analyzer.plot_probability_distribution()
        analyzer.plot_blur_by_resolution()
        
    else:
        print("Exiting program due to data loading failure.")