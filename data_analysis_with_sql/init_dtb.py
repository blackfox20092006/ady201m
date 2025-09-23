import sqlite3
db = sqlite3.connect('data.db')
cur = db.cursor()
cur.execute('drop table if exists Videos')
cur.execute('drop table if exists Metadata')
cur.execute('drop table if exists Analysis_result')
#create tables
queries = [
    '''
    create table Videos(
        video_id int not null primary key,
        label_id int not null  
    );
    ''',
    '''
    create table Metadata(
        video_id int not null primary key,
        video_name nvarchar(200) not null,
        bitrate int,
        codec nvarchar(6),
        fps int,
        resolution nvarchar(10),
        time date,
        format nvarchar(6),
        duration int, 
        file_size int,
        file_path nvarchar(1000) not null
    );
    ''',
    '''
    create table Analysis_result(
        video_id int not null primary key,
        violence_probability float not null,
        time date
    );
    '''
] #duration in second / resolution in format: (xxxx,yyyy) / file_size in kB
for i in queries:
    cur.execute(i)
cur.close()