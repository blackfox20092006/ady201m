-- SQLite
/*1)Truy xuất 10 video đầu tiên thuộc label nào*/
SELECT V.video_id , Dt.video_name , LB.label_name
FROM Videos AS V 
JOIN Labels AS LB  ON LB.label_id = V.label_id 
JOIN Metadata AS DT  ON DT.video_id = V.video_id
LIMIT 10
