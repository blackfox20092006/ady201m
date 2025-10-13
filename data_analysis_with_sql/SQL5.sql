-- SQLite
/*5) VIDEO CÓ SIZE LỚN NHẤT*/
SELECT video_name , MAX(file_size) AS 'VIDEO CÓ SIZE LỚN NHẤT'
FROM Metadata

