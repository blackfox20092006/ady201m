import sqlite3
db = sqlite3.connect('data.db')
cur = db.cursor()
#create tables
queries = [
    '''PRAGMA foreign_keys = ON;''',
    '''drop table if exists Videos;''',
    '''drop table if exists Metadata;''',
    '''drop table if exists Analysis_result;''',
    '''
    create table Labels(
        label_id int not null primary key,
        label_name nvarchar(20),
        description nvarchar
    );
    ''',
    '''
    create table Videos(
        video_id int not null primary key,
        label_id int not null,
        foreign key (label_id) references Labels(label_id) on delete cascade
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
        file_path nvarchar(1000) not null,
        foreign key (video_id) references Videos(video_id) on delete cascade
    );
    ''',
    '''
    create table Analysis_result(
        video_id int not null primary key,
        violence_probability float not null,
        time date,
        foreign key (video_id) references Videos(video_id) on delete cascade,
        foreign key (video_id) references Metadata(video_id) on delete cascade
    );
    '''
] #duration in second / resolution in format: (xxxx,yyyy) / file_size in kB
for i in queries:
    cur.execute(i)
cur.close()