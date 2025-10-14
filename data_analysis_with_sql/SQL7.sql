-- SQLite
/*7) ĐẾM SỐ LƯỢNG VIDEO VỚI MỖI LABEL*/
SELECT l.label_name, COUNT(v.video_id) AS so_luong_video
FROM Videos v
JOIN Labels l ON v.label_id = l.label_id
GROUP BY l.label_name;