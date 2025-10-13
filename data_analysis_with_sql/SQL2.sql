-- SQLite
/*2)TÌM 5 VIDEO THUỘC LABEL SUÂT BẠO LỰC */
SELECT DT.video_name , LB.label_name
FROM Labels AS LB
JOIN Videos AS V ON LB.label_id = V.label_id
JOIN Metadata AS DT  ON DT.video_id = V.video_id
WHERE label_name = 'vio_violence'
LIMIT 5