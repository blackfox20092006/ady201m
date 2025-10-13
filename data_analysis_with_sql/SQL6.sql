-- SQLite
/*6 VIDEO CÓ THỜI LƯỢNG DÀI NHẤT */
SELECT video_name , MAX(duration) AS 'VIDEO CÓ THỜI LƯỢNG DÀI NHẤT'
FROM Metadata 