class analystic_with_python:
    def __init__(self):
        pass
    def readcsv(self,file): #Get a general understanding of your dataset structure and cleanliness.
        df = pd.read_csv('file')
        return df
    def yc1(self):
        metadata = self.readcsv('Metadata.csv')
        videos = self.readcsv('Videos.csv')
        labels = self.readcsv('Labels.csv')
        analysis_result = self.readcsv('Analysis_result.csv')
        print(metadata.info())
        print(videos.info())
        print(labels.info())
        print(analysis_result.info())
        
    def yc2(self): #Examine balance between “Violent” and “Non-Violent” samples. (File_3: Labels.csv)
        videos = self.readcsv('Videos.csv')
        labels = self.readcsv('Labels.csv')
        df = pd.merge(videos,labels,on='label_id',how='inner')
        print(df['label_name'].value_counts())
        
    def yc3(self): #Compare predicted probabilities between the two classes.
        analysis_result = self.readcsv('Analysis_result.csv')
        videos = self.readcsv('Videos.csv')
        df = pd.merge(analysis_result,videos,on='video_id',how='inner')
        print(df.groupby('label_id')['violence_probability'].mean())
    
    def yc4(self): #Explore which features correlate with violence probability.
        df = self.readcsv('Analysis_result.csv')
        corr = df[['violence_probability','frame_diff_mean','frame_diff_var','blur','brightness','contrast','optical_flow']].corr()
        print(corr['violence_probability'])
        
    def yc5(self): #See if longer videos tend to have higher violence scores.
        analysis_result = self.readcsv('Analysis_result.csv')
        metadata = self.readcsv('Metadata.csv')
        df = pd.merge(analysis_result,metadata,on='video_id',how='inner')
        corr = df[['duration','violence_probability']].corr()
        print(corr)
        
    def yc6(self): #Test if frame rate differs between classes. 
        metadata = self.readcsv('Metadata.csv')
        violence = metadata[metadata['video_id'].str.startswith('v')]['fps'].mean()
        non_violence = metadata[metadata['video_id'].str.startswith('n')]['fps'].mean()
        print(f'Frame rate của violence: {violence}')
        print(f'Frame rate của non_violence: {non_violence}')
        
    def yc7(self):#Identify which videos are predicted most violent.
        df = self.readcsv('Analysis_result.csv')
        violent_video = df.sort_values(by='violence_probability').tail(10)
        print(violent_video)
        
    def yc8(self): #Same as above but for lowest scores.
        df = self.readcsv('Analysis_result.csv')
        nonviolent_video = df.sort_values(by='violence_probability').head(10)
        print(nonviolent_video)
        
    def yc9(self): #Examine whether brightness or contrast correlates with violence.
        df = self.readcsv('Analysis_result.csv')
        print('Phân tích tương quan \n')
        col_features = ['violence_probability', 'contrast', 'brightness']
        correlation_matrix = df[col_features].corr()
        print(f'bảng tương quan giữa contrast , brightness , violence_probability: \n {correlation_matrix}')
        print('\n')
        correlation_w_violence = correlation_matrix['violence_probability']
        print(f"Tương quan giữa brightness và violence_probability:{correlation_w_violence['brightness']:.4f}")
        print(f"Tương quan giữa contrast và violence_probability:{correlation_w_violence['contrast']:.4f}")
        
    def yc10(self): #Check if blur (focus quality) influences model predictions.
        df = self.readcsv('Analysis_result.csv')
        col_features = ['violence_probability', 'blur']
        correlation_matrix = df[col_features].corr()
        print(f"Bảng tương quan giữa violence_probability và blur :\n {correlation_matrix}")
        print("\n")
        correlation_w_vioprob = correlation_matrix["violence_probability"]
        print(f"Tương quan giữa violence_probability và blur:{correlation_w_vioprob["blur"]}")
    
    
    def yc11(self): #Determine whether motion intensity relates to violence.
        df = self.readcsv('Analysis_result.csv')
        col_of_features = ['violence_probability','optical_flow', 'frame_diff_var', 'frame_diff_mean']
        correlation_matrix = df[col_of_features].corr()
        print(f"Bảng tương quan giữa violence_probability,frame_diff_mean,frame_diff_var và optical flow: \n {correlation_matrix}")
        print("\n")
        correlate_w_vioprob = correlation_matrix['violence_probability']
        print(f"Tương quan giữa violence probability với optical flow :{correlate_w_vioprob['optical_flow']:.4f}")
        print(f"Tương quan giữa violence probability với frame_diff_var :{correlate_w_vioprob['frame_diff_var']:.4f}")
        print(f"Tương quan giữa violence probability với frame_diff_mean :{correlate_w_vioprob['frame_diff_mean']:.4f} ")
        

