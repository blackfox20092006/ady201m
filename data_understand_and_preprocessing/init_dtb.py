import sqlite3, os, ffmpeg
from dotenv import find_dotenv, load_dotenv
#begin init
load_dotenv(find_dotenv())
root = os.getenv('ROOT')
non_dataset_path = os.path.join(root, 'data_understand_and_preprocessing', 'preprocessing', 'dataset', 'non_violence')
vio_dataset_path = os.path.join(root, 'data_understand_and_preprocessing', 'preprocessing', 'dataset', 'violence')
db = sqlite3.connect(os.path.join('data', 'data.db'))
cur = db.cursor()
cur.execute('PRAGMA foreign_keys = ON;')
#create tables
#drop tu leaves => root
queries = [
    '''drop table if exists Analysis_result;''',
    '''drop table if exists Metadata;''',
    '''drop table if exists Videos;''',
    '''drop table if exists Labels;''',
    '''
    create table Labels(
        label_id int not null primary key,
        label_name nvarchar(20),
        description nvarchar
    );
    ''',
    '''
    create table Videos(
        video_id nvarchar not null primary key,
        label_id int not null,
        foreign key (label_id) references Labels(label_id) on delete cascade
    );
    ''',
    '''
    create table Metadata(
        video_id nvarchar not null primary key,
        video_name nvarchar(200) not null,
        bitrate int,
        codec nvarchar(6),
        fps int,
        resolution nvarchar(10),
        time date,
        format nvarchar(6),
        duration int, 
        file_size int,
        file_path nvarchar(1000) not null,
        foreign key (video_id) references Videos(video_id) on delete cascade
    );
    ''',
    '''
    create table Analysis_result(
        video_id nvarchar not null primary key,
        violence_probability float not null,
        foreign key (video_id) references Videos(video_id) on delete cascade,
        foreign key (video_id) references Metadata(video_id) on delete cascade
    );
    '''
] #duration in second / resolution in format: (xxxx,yyyy) / file_size in kB
for i in queries:
    cur.execute(i)
#end init

query = 'insert into {} {} values {}' 
count_Var = 1

#begin load non
os.chdir(non_dataset_path)
label_id = '0'
label_name = 'non_violence'
desc = 'non violence video'
cur.execute(query.format('Labels', '(label_id, label_name, description)', f"({label_id}, '{label_name}', '{desc}')"))
for i in os.listdir():
    if i.split('.')[-1] not in ['mp4', 'mov', 'avi', 'mkv', 'wmv', 'flv', 'webm']:
        continue
    file_path = os.path.join(non_dataset_path, i)
    tmp_probe = ffmpeg.probe(file_path)
    tmp_probe_data = tmp_probe['format']
    video_stream_data = next(stream for stream in tmp_probe['streams'] if stream['codec_type'] == 'video')
    bitrate = int(tmp_probe_data['bit_rate']) // 1000
    codec = video_stream_data['codec_name']
    fps = eval(video_stream_data['avg_frame_rate'])
    resolution = f"{video_stream_data['width']}x{video_stream_data['height']}"
    time = os.path.getctime(file_path)
    file_format = i.split('.')[-1]
    duration = float(tmp_probe_data['duration'])
    file_size = os.path.getsize(file_path) // 1024
    cur.execute(query.format('Videos', '(video_id, label_id)', f'("n_{count_Var}", {label_id})'))
    cur.execute(query.format('Metadata', '(video_id, video_name, bitrate, codec, fps, resolution, time, format, duration, file_size, file_path)', f"('n_{count_Var}', '{i}', {bitrate}, '{codec}', {fps}, '{resolution}', {time}, '{file_format}', {duration}, {file_size}, '{file_path}')"))
    count_Var += 1
#end load non
db.commit()
#begin load vio
os.chdir(vio_dataset_path)
label_id = '1'
label_name = 'vio_violence'
desc = 'violence video'
count_Var = 1
cur.execute(query.format('Labels', '(label_id, label_name, description)', f"({label_id}, '{label_name}', '{desc}')"))
for i in os.listdir():
    if i.split('.')[-1] not in ['mp4', 'mov', 'avi', 'mkv', 'wmv', 'flv', 'webm']:
        continue
    file_path = os.path.join(vio_dataset_path, i)
    tmp_probe = ffmpeg.probe(file_path)
    tmp_probe_data = tmp_probe['format']
    video_stream_data = next(stream for stream in tmp_probe['streams'] if stream['codec_type'] == 'video')
    bitrate = int(tmp_probe_data['bit_rate']) // 1000
    codec = video_stream_data['codec_name']
    fps = eval(video_stream_data['avg_frame_rate'])
    resolution = f"{video_stream_data['width']}x{video_stream_data['height']}"
    time = os.path.getctime(file_path)
    file_format = i.split('.')[-1]
    duration = float(tmp_probe_data['duration'])
    file_size = os.path.getsize(file_path) // 1024
    cur.execute(query.format('Videos', '(video_id, label_id)', f'("v_{count_Var}", {label_id})'))
    cur.execute(query.format('Metadata', '(video_id, video_name, bitrate, codec, fps, resolution, time, format, duration, file_size, file_path)', f"('v_{count_Var}', '{i}', {bitrate}, '{codec}', {fps}, '{resolution}', {time}, '{file_format}', {duration}, {file_size}, '{file_path}')"))
    count_Var += 1
db.commit()
#end load vio
cur.close()
db.close()