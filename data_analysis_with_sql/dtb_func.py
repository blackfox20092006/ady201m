import sqlite3
from dotenv import find_dotenv, load_dotenv
class dtb_func_struct:
    def __init__(self):
        load_dotenv(find_dotenv())
        self.db = sqlite3.connect('data.db')
        self.cur = self.db.cursor()
    def get_metadata(file_path):
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

        #video id
        self.cur.execute('select video_id from Videos')
        data = self.cur.fetchall()
        tmp_id, tml_label_id = data[-1]
        video_id = tmp_id + 1
        
        #video name
        video_name = (file_path.split('\\')[-1]).split('.')[0]

        return video_id, video_name, bitrate, codec, fps, resolution, time, format, duration, file_size, file_path
    def insert_ans(video_id, violence_probability):
        try:
            self.cur.execute(f'insert into Analysis_result (video_id, violence_probability) values ({video_id}, {violence_probability}})')
            self.db.commit()
            return True
        except:
            self.db.rollback()
            return False
    def insert_video(file_path, label_id):
        try:
            video_id, bitrate, codec, fps, resolution, time, file_format, duration, file_size = self.get_metadata(file_path)
            self.cur.execute(f'insert into Videos (video_id, , label_id) values ({video_id}, {label_id})')
            self.cur.execute(f'insert into Metadata (video_id, video_name, bitrate, codec, fps, resolution, time, format, duration, file_size, file_path) values ' + f"({count_Var}, '{i}', {bitrate}, '{codec}', {fps}, '{resolution}', {time}, '{file_format}', {duration}, {file_size}, '{file_path}')")
            self.db.commit()
        except:
            self.db.rollback()
            return False