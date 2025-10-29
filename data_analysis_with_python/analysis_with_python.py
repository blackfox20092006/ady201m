class analystic_with_python:
    def __init__(self):
        pass
    def yc1(self,file): #Get a general understanding of your dataset structure and cleanliness.
        df = pd.read_csv('file')
        print(df.info())
        return df
    def yc2(self,file_1,file_2,file_3): #Examine balance between “Violent” and “Non-Violent” samples. (File_3: Labels.csv)
        df_1 = self.yc1(file_1)
        df_2 = self.yc1(file_2)
        df_3 = self.yc1(file_3)
        df = pd.merge(df_1,df_2,on='video_id',how='inner').merge(df_3,on='label_id',how='inner')
        print(df['label_name'].value_counts())
        
    def yc3(self,file_1,file_2): #Compare predicted probabilities between the two classes.
        df_1 = self.yc1(file_1)
        df_2 = self.yc1(file_2)
        df = pd.merge(df_1,df_2,on='video_id',how='inner')
        print(df.groupby('label_id')['violence_probability'].mean())
    
    def yc4(self,file): #Explore which features correlate with violence probability.
        df = self.yc1(file)
        corr = df[['violence_probability','frame_diff_mean','frame_diff_var','blur','brightness','contrast','optical_flow']].corr()
        print(corr['violence_probability'])
        
    def yc5(self,file_1,file_2): #See if longer videos tend to have higher violence scores.
        df_1 = self.yc1(file_1)
        df_2 = self.yc1(file_2)
        df = pd.merge(df_1,df_2,on='video_id',how='inner')
        corr = df[['duration','violence_probability']].corr()
        print(corr)
        
    def yc6(self,file): #Test if frame rate differs between classes. Metadata.csv
        metadata = self.yc1(file)
        violence = metadata[metadata['video_id'].str.startswith('v')]['fps'].mean()
        non_violence = metadata[metadata['video_id'].str.startswith('n')]['fps'].mean()
        print(f'Frame rate của violence: {violence}')
        print(f'Frame rate của non_violence: {non_violence}')
        
    def yc7(self,file):#Identify which videos are predicted most violent.
        df = self.yc1(file)
        violent_video = df.sort_values(by='violence_probability').tail(10)
        print(violent_video)
        
    def yc8(self,file): #Same as above but for lowest scores.
        df = self.yc1(file)
        nonviolent_video = df.sort_values(by='violence_probability').head(10)
        print(nonviolent_video)
        
    def yc9(self,file): #Examine whether brightness or contrast correlates with violence.
        df = self.yc1(file)
        print('Phân tích tương quan \n')
        col_features = ['violence_probability', 'contrast', 'brightness']
        correlation_matrix = df[col_features].corr()
        print(f'bảng tương quan giữa contrast , brightness , violence_probability: \n {correlation_matrix}')
        print('\n')
        correlation_w_violence = correlation_matrix['violence_probability']
        print(f"Tương quan giữa brightness và violence_probability:{correlation_w_violence['brightness']:.4f}")
        print(f"Tương quan giữa contrast và violence_probability:{correlation_w_violence['contrast']:.4f}")
        
    def yc10(self,file): #Check if blur (focus quality) influences model predictions.
        df = self.yc1(file)
        col_features = ['violence_probability', 'blur']
        correlation_matrix = df[col_features].corr()
        print(f"Bảng tương quan giữa violence_probability và blur :\n {correlation_matrix}")
        print("\n")
        correlation_w_vioprob = correlation_matrix["violence_probability"]
        print(f"Tương quan giữa violence_probability và blur:{correlation_w_vioprob["blur"]}")
    
    
    def yc11(self,file): #Determine whether motion intensity relates to violence.
        df = self.yc1(file)
        col_of_features = ['violence_probability','optical_flow', 'frame_diff_var', 'frame_diff_mean']
        correlation_matrix = df[col_of_features].corr()
        print(f"Bảng tương quan giữa violence_probability,frame_diff_mean,frame_diff_var và optical flow: \n {correlation_matrix}")
        print("\n")
        correlate_w_vioprob = correlation_matrix['violence_probability']
        print(f"Tương quan giữa violence probability với optical flow :{correlate_w_vioprob['optical_flow']:.4f}")
        print(f"Tương quan giữa violence probability với frame_diff_var :{correlate_w_vioprob['frame_diff_var']:.4f}")
        print(f"Tương quan giữa violence probability với frame_diff_mean :{correlate_w_vioprob['frame_diff_mean']:.4f} ")
        
