-- SQLite
/*3)Thống kê mỗi kiểu format có bao nhiêu video*/
SELECT DT.format , COUNT(DT.video_id) AS SO_LUONG_VIDEO
FROM Metadata AS DT 
GROUP BY DT.format
GO
