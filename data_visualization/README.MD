🎬 1. Box Plot: Blur theo độ phân giải (res_bucket)

Quan sát:

Blur tăng nhẹ từ <480p → 720p → 1080p → 1440+.

1440p+ có nhiều outlier cực lớn (blur > 30k).

Nguyên nhân:

Khi độ phân giải cao hơn, ảnh/video chứa nhiều chi tiết hơn, nên giá trị đo độ mờ (blur index, thường tính bằng Laplacian variance) cũng lớn hơn dù video không thực sự “mờ”.

Các video độ phân giải cao có thể bị nén, upscale hoặc sharpen giả tạo, tạo ra biến động lớn → sinh ra outlier.

Blur còn phụ thuộc vào điều kiện quay (chuyển động máy, tiêu điểm, ánh sáng), nên cùng độ phân giải nhưng độ mờ khác nhau rất nhiều.

Kết luận:
Không nên so blur giữa các độ phân giải trực tiếp vì ảnh hưởng cấu trúc pixel. Cần chuẩn hoá blur theo resolution bucket để so sánh công bằng.

🔥 2. Heatmap: Ma trận tương quan giữa các đặc trưng

Quan sát nổi bật:

frame_diff_mean và frame_diff_var tương quan cao (0.69) → cùng phản ánh mức chuyển động.

contrast tương quan mạnh với frame_diff_var (0.73) → khi có nhiều chuyển động, contrast giữa khung hình tăng.

violence_probability có tương quan âm nhẹ với hầu hết các đặc trưng (−0.16 đến −0.28).

Nguyên nhân:

Clip “bạo lực” thật thường có ít chuyển động camera hơn, hoặc chuyển động bị “tĩnh” do cảnh quay cận.

Còn clip non-violent (VD vlog, thể thao) có optical flow và contrast cao → dễ khiến mô hình hiểu nhầm là non-violent.

Điều này cho thấy mô hình violence hiện tại có thể đang thiên vị ngược với motion features.

Kết luận:
Cần xem lại cách gán nhãn hoặc huấn luyện model để giảm bias. Có thể thêm feature ngữ cảnh (âm thanh, khuôn mặt, vật thể) để cân bằng.

📊 3. Histogram: Phân bố xác suất bạo lực (violence_probability)

Quan sát:

Phân bố hơi lệch về trái (nhiều video có xác suất thấp), nhưng vẫn rải rác đến vùng cao (≈ 0.9).

Nguyên nhân:

Bộ dữ liệu có thể thiên về video không bạo lực → mô hình học xu hướng “an toàn” hơn.

Phần đuôi bên phải (xác suất cao) thể hiện các clip có đặc trưng cực đoan — ví dụ ánh sáng mạnh, contrast thấp, chuyển động đặc biệt.

Kết luận:
Phân bố như này hợp lý nếu dữ liệu thực tế có tỉ lệ bạo lực thấp. Nhưng khi huấn luyện, cần cân bằng nhãn hoặc dùng weighting / oversampling.

💫 4. Scatter Plot: Optical Flow vs Frame Diff Mean

Quan sát:

Tương quan dương rõ rệt: khi optical flow (chuyển động điểm ảnh) tăng thì frame_diff_mean cũng tăng.

Có vài điểm ngoại lệ (flow cao nhưng diff thấp).

Nguyên nhân:

Cả hai đều là chỉ số đo mức độ chuyển động, nên có xu hướng cùng tăng.

Ngoại lệ xuất hiện khi video có chuyển động đồng đều (camera pan) — optical flow cao, nhưng frame_diff_mean nhỏ vì các frame gần như giống nhau.

Kết luận:
Cả hai đo lường khía cạnh khác nhau của motion: optical_flow đo “hướng và tốc độ”, frame_diff_mean đo “mức thay đổi tổng thể”. Khi kết hợp → đặc trưng chuyển động mạnh hơn.

📈 5. Line Chart: Xu hướng violence probability theo frame_diff_mean

Quan sát:

Khi frame_diff_mean tăng, violence_prob giảm dần, từ ~0.55 → ~0.30.

Có vài điểm dao động (nhảy nhẹ lên giữa khoảng 170–200).

Nguyên nhân:

Các video có chuyển động mạnh thường không phải bạo lực (VD thể thao, hành động nhanh, nhảy múa).

Ngược lại, cảnh bạo lực thường diễn ra trong không gian ít chuyển động toàn cảnh, nhưng có chuyển động chi tiết (tay, vật).

Các điểm nhấp nhô là do số lượng mẫu ít ở một vài bin, khiến trung bình dao động.

Kết luận:
Xu hướng này hợp lý, cho thấy chuyển động mạnh không đồng nghĩa với bạo lực. Mô hình nên chú trọng hơn vào loại chuyển động (local motion) chứ không chỉ magnitude tổng thể.