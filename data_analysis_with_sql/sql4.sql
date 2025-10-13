-- SQLite
/*4) Thống kê mỗi mức FPS có bao nhiêu video*/
SELECT  fps , COUNT(video_name) AS SO_LUONG_VIDEO 
FROM Metadata AS DT 
GROUP BY DT.fps
ORDER BY DT.fps