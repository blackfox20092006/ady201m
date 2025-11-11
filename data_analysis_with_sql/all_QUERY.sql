-- SQLite
/*1)Truy xuất 10 video đầu tiên thuộc label nào*/
SELECT V.video_id , Dt.video_name , LB.label_name
FROM Videos AS V 
JOIN Labels AS LB  ON LB.label_id = V.label_id 
JOIN Metadata AS DT  ON DT.video_id = V.video_id
LIMIT 10
GO 
-- 2)TÌM 5 VIDEO THUỘC LABEL SUÂT BẠO LỰC 
SELECT DT.video_name , LB.label_name
FROM Labels AS LB
JOIN Videos AS V ON LB.label_id = V.label_id
JOIN Metadata AS DT  ON DT.video_id = V.video_id
WHERE label_name = 'vio_violence'
LIMIT 5

GO 
-- 3)TÌM VIDEO CÓ TỶ LỆ BẠO LỰC CAO NHẤT
SELECT AR.video_id , DT.video_name , AR.violence_probability, LB.label_name
FROM Labels AS LB 
JOIN Videos AS VD ON LB.label_id = VD.label_id
JOIN Metadata AS DT ON VD.video_id = DT.video_id
JOIN Analysis_result AS AR ON DT.video_id = AR.video_id
WHERE AR.violence_probability = (SELECT MAX(violence_probability) FROM Analysis_result   )

GO 
-- 4) Thống kê mỗi mức FPS có bao nhiêu video
SELECT DT.fps , COUNT(DT.video_id)
FROM Metadata AS DT 
GROUP BY DT.FPS 
ORDER BY DT.FPS DESC

GO 
-- 5) VIDEO CÓ SIZE LỚN NHẤT VÀ NHỎ NHẤT
SELECT DT.video_name , DT.file_size AS 'VIDEO CÓ KÍCH THƯỚC LỚN NHẤT'
FROM Metadata AS DT 
WHERE DT.file_size = (SELECT MAX(DT.file_size) FROM Metadata AS DT)
UNION  
SELECT DT.video_name , DT.file_size AS 'VIDEO CÓ KÍCH THƯỚC NHỎ NHẤT'
FROM Metadata AS DT 
WHERE DT.file_size = (SELECT MIN(DT.file_size) FROM Metadata AS DT)


GO 
-- 6) SỐ LƯỢNG VIDEO CÓ TỈ LỆ BẠO LỰC CAO NHẤT 
SELECT COUNT(AR.violence_probability) AS 'SỐ LƯỢNG VIDEO CÓ TỈ LỆ BẠO LỰC CAO NHẤT ' 
FROM Analysis_result AS AR 
WHERE AR.violence_probability = (SELECT MAX(AR.violence_probability) FROM Analysis_result AS AR)
GO 

--7) ĐẾM SỐ LƯỢNG VIDEO VỚI MỖI LABEL
SELECT LB.label_name ,COUNT(video_id) AS 'SỐ LƯỢNG VIDEO'
FROM Labels AS LB JOIN Videos AS VD ON LB.label_id = VD.label_id
GROUP BY LB.label_id

GO 
-- 8) TÌM NHỮNG VIDEO TRONG LABEL NON_VIOLENCE NHƯNG CÓ TỈ LỆ BẠO LỰC CAO
SELECT VD.video_id , AR.violence_probability , LB.label_name
FROM Labels AS LB  
JOIN VIDEOS AS VD ON LB.label_id = VD.label_id
JOIN Analysis_result AS AR ON VD.video_id = AR.video_id
WHERE label_name = 'non_violence' AND AR.violence_probability > 0.8
ORDER BY AR.violence_probability DESC 




