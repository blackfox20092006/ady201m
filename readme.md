
# **DỰ ÁN PHÂN TÍCH, TRỰC QUAN VÀ PHÁT HIỆN BẠO LỰC TRONG VIDEO SỬ DỤNG THỊ GIÁC MÁY TÍNH VÀ HỌC SÂU**

**Giáo viên hướng dẫn**: Nguyễn Hoàng Linh 

| Thành viên nhóm  | [Hoàng Quang Nhân](https://github.com/blackfox20092006) \- Trưởng nhóm \- SE204283 |
| :---: | :---- |
|  | [Lê Phan Thanh Nghi](https://github.com/thanh-nghi) \- Thành viên \- SE203909  |
|  | [Bùi Xuân Hoan](https://github.com/DOMEMON) \- Thành viên \- SE204139  |
| Lớp | AI1912\_ADY201m\_FA25  |


Link PDF báo cáo: [click here](https://docs.google.com/document/d/1unzAM4F5qV1y0UpWdBj3Rz7bPOC8TwbpZF94WgIW8kM/edit?usp=sharing)

# **MỤC LỤC**

1. **Giới thiệu**  
   * 1.1 Bối cảnh & Vấn đề  
   * 1.2 Lý do chọn đề tài  
   * 1.3 Mục tiêu của dự án  
   * 1.4 Phương pháp luận  
2. **Thu thập, Hiểu và Chuẩn bị Dữ liệu**  
   * 2.1 Thu thập Dữ liệu  
   * 2.2 Lưu trữ Metadata  
   * 2.3 Gán nhãn Dữ liệu  
   * 2.4 Chuẩn hoá Dữ liệu  
   * 2.5 Phân chia Dữ liệu  
   * 2.6 Trích xuất Đặc trưng và Xác suất (Sử dụng MoViNet)  
   * 2.7 Định nghĩa các Hàm Trích xuất Đặc trưng Vật lý  
3. **Phân tích Dữ liệu với SQL**  
   * 3.1 Truy xuất N video đầu tiên theo nhãn  
   * 3.2 Đếm số lượng video theo FPS  
   * 3.3 Tìm video có kích thước file lớn nhất/nhỏ nhất  
   * 3.4 Tìm video có thời lượng dài nhất/ngắn nhất  
   * 3.5 Đếm số lượng video cho mỗi nhãn  
   * 3.6 Liệt kê video và nhãn tương ứng  
   * 3.7 Tìm video "Non-violence" có xác suất bạo lực cao  
4. **Phân tích Dữ liệu với Python**  
   * 4.1 Hiểu cấu trúc và sự sạch sẽ của dữ liệu  
   * 4.2 Kiểm tra sự cân bằng giữa các nhãn  
   * 4.3 So sánh xác suất dự đoán giữa hai lớp  
   * 4.4 Khám phá tương quan giữa đặc trưng và xác suất bạo lực  
   * 4.5 Kiểm tra xu hướng thời lượng và điểm bạo lực  
   * 4.6 Kiểm tra sự khác biệt FPS giữa các nhãn  
   * 4.7 Xác định video có dự đoán bạo lực cao nhất/thấp nhất  
   * 4.8 Kiểm tra tương quan của độ sáng/tương phản với bạo lực  
   * 4.9 Kiểm tra ảnh hưởng của độ mờ (blur)  
   * 4.10 Xác định mối quan hệ của cường độ chuyển động  
5. **Trực quan hoá Dữ liệu**  
   * 5.1 Heatmap: Ma trận tương quan giữa các đặc trưng  
   * 5.2 Scatter Plot: Optical Flow vs Frame Diff Mean  
   * 5.3 Line Chart: Xu hướng violence probability theo frame\_diff\_mean  
   * 5.4 Histogram: Phân bố xác suất bạo lực (violence\_probability)  
   * 5.5 Box Plot: Blur theo độ phân giải (res\_bucket)  
6. **Phân tích Hồi quy**  
   * 6.1 Mục tiêu Hồi quy  
   * 6.2 Chuẩn bị Dữ liệu cho Hồi quy  
   * 6.3 Kết quả Thực nghiệm và Phân tích  
7. **Kết luận và Hướng phát triển**  
   * 7.1 Tổng kết  
   * 7.2 Hạn chế  
   * 7.3 Hướng phát triển

8. ## **Kết luận và hướng phát triển**

   * 8.1 Tổng kết  
   * 8.2 Hạn chế  
   * 8.3 Hướng phát triển  
9. **Tài liệu tham khảo**

## **1\. Giới thiệu**

### **1.1 Bối cảnh và Vấn đề**

Trong bối cảnh xã hội hiện nay, vấn đề bạo lực, đặc biệt là bạo lực học đường và nơi công cộng, đang trở thành một mối lo ngại toàn cầu. Những hành vi bạo lực không chỉ gây tổn thương về thể chất mà còn để lại hậu quả nghiêm trọng về tinh thần, ảnh hưởng lâu dài đến cộng đồng và sự phát triển của con người.

Tại các trường học, trung tâm thương mại hay khu dân cư, hệ thống camera giám sát đã được triển khai rộng rãi nhằm đảm bảo an ninh. Tuy nhiên, việc giám sát và phát hiện bạo lực vẫn phụ thuộc chủ yếu vào con người — như giáo viên, giám thị hoặc bảo vệ. Những phương pháp truyền thống này tồn tại nhiều hạn chế rõ rệt:

* Con người không thể giám sát liên tục 24/7, đặc biệt là trong môi trường có hàng trăm camera.  
* Việc quan sát lâu dài dễ dẫn đến mệt mỏi, mất tập trung và bỏ sót sự cố quan trọng.  
* Các biện pháp hiện tại thường mang tính phản ứng, chỉ xử lý khi sự việc đã xảy ra thay vì phòng ngừa chủ động.

Do đó, nhu cầu về một hệ thống giám sát thông minh, tự động và đáng tin cậy ngày càng trở nên cấp thiết — một hệ thống có thể “hiểu” nội dung video, phát hiện hành vi bất thường, và cảnh báo kịp thời khi có dấu hiệu bạo lực.

### **1.2 Lý do chọn đề tài**

Sự bùng nổ của Trí tuệ nhân tạo (AI), đặc biệt trong lĩnh vực Thị giác máy tính (Computer Vision) và Học sâu (Deep Learning), đã mở ra khả năng biến giấc mơ này thành hiện thực. Các mô hình học sâu hiện nay có thể phân tích, nhận diện và hiểu được chuyển động, hành động, cảm xúc của con người trong video gần như tương đương — thậm chí vượt qua — khả năng quan sát của con người.

Bằng việc tận dụng sức mạnh của AI kết hợp hệ thống camera sẵn có, ta có thể xây dựng một giải pháp phát hiện bạo lực tự động, hoạt động liên tục, khách quan và hiệu quả hơn nhiều lần so với giám sát thủ công.

Đó chính là lý do nhóm lựa chọn đề tài “Phát hiện bạo lực trong video sử dụng mô hình học sâu MoViNet (Mobile Video Networks)” — một hướng nghiên cứu vừa mang tính thực tiễn cao, vừa đóng góp ý nghĩa xã hội rõ rệt.

### **1.3 Mục tiêu của dự án**

Dự án hướng tới việc phát triển một hệ thống thông minh có khả năng phân loại video thành hai nhóm chính:

* Violent (Bạo lực)

* Non-Violent (Không bạo lực)

Ngoài ra, hệ thống còn tập trung vào phân tích sâu đặc trưng của từng video, nhằm hiểu rõ hơn về các yếu tố vật lý và nội dung có liên quan đến hành vi bạo lực. Cụ thể, các mục tiêu chính bao gồm:

1. Phát hiện và phân loại video theo mức độ bạo lực dựa trên nội dung hình ảnh và chuyển động.  
2. Phân tích đặc trưng vật lý của video như:  
   * Mức độ chuyển động (motion intensity)  
   * Độ mờ (blur), độ sáng (brightness), độ tương phản (contrast)  
   * Dòng quang học (optical flow) thể hiện hướng và cường độ chuyển động  
3. Khai thác dữ liệu thống kê và trực quan hoá (EDA) để hiểu mối quan hệ giữa đặc trưng vật lý và xác suất bạo lực mà mô hình AI dự đoán.  
4. Cung cấp nền tảng dữ liệu và hiểu biết trực quan giúp mở rộng sang các mô hình phát hiện hành vi khác như: bắt nạt, gây rối, xô xát, hoặc hành vi bất thường trong môi trường công cộng.

### **1.4 Phương pháp tiếp cận**

Để đạt được các mục tiêu trên, nhóm triển khai một quy trình nghiên cứu gồm ba giai đoạn chính, kết hợp AI, kỹ thuật xử lý video, và phân tích dữ liệu:

**1.4.1 Huấn luyện và Tinh chỉnh mô hình (Fine-tuning)**

* Sử dụng MoViNet-A3 Stream, một kiến trúc hiện đại được thiết kế tối ưu cho video trên thiết bị di động.  
  * Mô hình này được pre-trained trên bộ dữ liệu lớn (Kinetics-600), sau đó tinh chỉnh (fine-tune) với bộ dữ liệu tùy chỉnh gồm hai nhãn: *Violent* và *Non-Violent*.

**1.4.2 Trích xuất xác suất bạo lực (Violence Probability Extraction)**

* Mỗi video được mô hình dự đoán một xác suất “bạo lực”, thể hiện mức độ mà mô hình tin rằng cảnh quay chứa hành vi bạo lực.  
  * Thông tin này được lưu trữ trong cơ sở dữ liệu SQLite để phục vụ các phân tích tiếp theo.

**1.4.3 Phân tích và Trực quan hóa dữ liệu (EDA)**

* Kết hợp giữa SQL, Python (Pandas, Seaborn, Matplotlib) và Power BI để phân tích, trực quan hóa các mối quan hệ giữa đặc trưng vật lý (như độ mờ, chuyển động, độ sáng...) và xác suất bạo lực.  
  * Mục tiêu là phát hiện xu hướng, outlier, và đưa ra giải thích định tính cho hành vi bạo lực dưới góc nhìn của dữ liệu.

### **1.5 Ý nghĩa thực tiễn**

Việc phát hiện bạo lực tự động không chỉ là một bài toán kỹ thuật, mà còn mang ý nghĩa xã hội sâu sắc:

* Giúp nhà trường, cơ quan, trung tâm an ninh giám sát chủ động, giảm thiểu rủi ro và phản ứng nhanh với các tình huống nguy hiểm.  
* Hỗ trợ xây dựng môi trường học tập và sinh hoạt an toàn hơn.  
* Tạo tiền đề cho các nghiên cứu mở rộng trong lĩnh vực phát hiện hành vi và cảm xúc bằng video.

## **2\. Thu thập, Hiểu và Chuẩn bị Dữ liệu**

Pipeline dữ liệu được thiết kế dạng chuỗi xử lý tự động từ khâu thu thập, trích xuất, chuẩn hóa, đến lưu trữ. Hệ thống gồm ba phần chính: crawling video, xử lý metadata, chuẩn hóa và phân tích đặc trưng.

### **2.1 Thu thập Dữ liệu**

Chương trình crawl\_main.py sử dụng đa luồng để truy xuất các trang hashtag của YouTube qua Selenium. Mỗi thread khởi tạo một trình duyệt Chrome chạy ở chế độ headless, tải trang hashtag, cuộn trang liên tục bằng Keys.END và thu thập ID video qua biểu thức regex “/watch?v=\[\\\\w-\]{11}”. Khi không còn video mới, thread kết thúc và lưu các liên kết duy nhất vào result.dat. Cấu trúc hàng đợi Queue điều phối các hashtag cho nhiều luồng, đồng bộ kết quả bằng threading.Lock. Hệ thống có thể mở rộng bằng cách tăng NUM\_THREADS hoặc thêm hashtag mới.

File download\_main.py đọc result.dat và sử dụng yt-dlp để tải video. Các tham số \--match-filter "duration \<= 100" giới hạn thời lượng, \--download-archive tránh tải trùng, \--no-overwrites bảo toàn dữ liệu cũ. Đầu ra là các video mp4 trong thư mục output, đảm bảo hai nhóm chính: violence và non\_violence.

Luồng hoạt động:

1. Đọc hashtags.  
2. Khởi động đa luồng để crawl.  
3. Lưu danh sách liên kết.  
4. Tải video bằng yt-dlp.  
5. Ghi log kết quả.

### **2.2 Lưu trữ Metadata**

File init\_dtb.py khởi tạo cơ sở dữ liệu SQLite data.db gồm bốn bảng:

* Labels(label\_id, label\_name, description)  
* Videos(video\_id, label\_id)  
* Metadata(video\_id, video\_name, bitrate, codec, fps, resolution, duration, file\_size, file\_path)  
* Analysis\_result(video\_id, violence\_probability, ...)

Các bảng liên kết bằng khóa ngoại, đảm bảo toàn vẹn dữ liệu. Script sử dụng ffmpeg.probe() để trích xuất metadata: bitrate, codec, fps, resolution, duration, file\_size, format. Mỗi video được gán video\_id theo dạng n\_1, v\_1 tương ứng với nhãn non\_violence hoặc violence. Dữ liệu chèn vào bảng bằng INSERT INTO, quá trình commit sau mỗi nhóm để tránh lock file. Việc bật PRAGMA foreign\_keys=ON duy trì quan hệ ràng buộc giữa video và metadata.

Logic xử lý:

1. Khởi tạo database, tạo bảng.  
2. Duyệt thư mục chứa video.  
3. Lấy metadata bằng ffmpeg.probe.  
4. Chèn vào Labels, Videos, Metadata.  
5. Commit, đóng kết nối.

### **2.3 Gán Nhãn Dữ Liệu**

Gán nhãn thủ công đảm bảo tính chính xác. Các video được xem xét và gán nhãn 0 hoặc 1, lưu vào Labels.csv, đồng thời cập nhật bảng Videos. Cấu trúc database đảm bảo mỗi video chỉ liên kết một nhãn duy nhất, phục vụ huấn luyện supervised.

### **2.4 Chuẩn Hóa Dữ Liệu**

File preprocessing\_main\_gpu.py chuẩn hóa video bằng ffmpeg có tăng tốc GPU. Hàm build\_ffmpeg\_command() cấu hình chuỗi lệnh \-vf scale=256:256:force\_original\_aspect\_ratio=decrease,pad=256:256:(ow-iw)/2:(oh-ih)/2:color=black,fps=12 để đồng nhất kích thước và FPS. Dữ liệu xuất ra stdout dạng byte stream RGB, đọc bằng Python, reshape thành tensor (num\_frames,256,256,3), chuẩn hóa \[0,1\], lưu dưới dạng .npy.

File sử dụng multiprocessing để chia video thành nhiều task, mỗi process gọi process\_single\_video() đọc input, kiểm tra dimension, chạy ffmpeg, lưu numpy tensor. Lỗi hoặc video quá nhỏ sẽ bị bỏ qua. Quá trình tận dụng \-hwaccel cuda để giải mã bằng GPU, giảm thời gian xử lý trung bình xuống dưới 2s/video.

Luồng xử lý:

1. Duyệt thư mục input.  
2. Tạo danh sách task (input\_path, output\_path, GPU\_TYPE).  
3. Multiprocessing Pool khởi chạy các process.  
4. Mỗi process chạy ffmpeg → đọc byte stream → reshape numpy → lưu file.  
5. Tổng hợp kết quả.

### **2.5 Phân Chia Dữ Liệu**

Sau khi chuẩn hóa, danh sách .npy được chia theo tỉ lệ 70:15:15 bằng train\_test\_split. Quá trình này sử dụng seed cố định để đảm bảo reproducibility.

### **2.6 Trích Xuất Đặc Trưng và Xác Suất**

Hai file VideoWorker.py và init\_features.py xử lý bước trích xuất đặc trưng và inference.

VideoWorker.py định nghĩa hàm extract(video\_input) trả về dictionary gồm các đặc trưng:

* frame\_diff\_mean / frame\_diff\_var: độ thay đổi giữa các frame.  
* brightness / contrast: trung bình và độ lệch chuẩn pixel.  
* blur: phương sai Laplacian đo độ sắc nét.  
* optical\_flow: độ lớn vector chuyển động từ cv2.calcOpticalFlowFarneback.

Hàm get\_vio\_prob(video\_path) dùng TensorFlow Lite interpreter để chạy mô hình MoViNet. Video được resize về (224x224), chia clip, chạy từng phần, lấy logits qua runner(\*\*states, image=clip), áp dụng softmax để tính \[P(Fight), P(NoFight)\], xác suất bạo lực \= P(Fight).

File init\_features.py kết nối SQLite, thêm cột đặc trưng vào Analysis\_result bằng ALTER TABLE, chạy ThreadPoolExecutor 10 luồng, mỗi luồng đọc file video, chạy extract(), gọi get\_vio\_prob(), chèn hoặc cập nhật dữ liệu vào bảng. Hàm kiểm tra nếu video\_id đã tồn tại thì update, chưa có thì insert.

Luồng hoạt động:

1. Kết nối database, đảm bảo schema đủ cột.  
2. Lấy danh sách video từ bảng Metadata.  
3. ThreadPoolExecutor chạy process\_video() cho từng video.  
4. Mỗi luồng:  
   * Mở video, đọc khung hình (cv2.VideoCapture).  
   * Resize frame, chọn bước lấy khung theo FPS gốc/12.  
   * Tạo numpy array frame.  
   * Gọi extract() để tính đặc trưng vật lý.  
   * Gọi get\_vio\_prob() để lấy xác suất.  
   * Update Analysis\_result.  
5. Commit kết quả, đóng kết nối.

### **2.7 Tính Toán Đặc Trưng Vật Lý**

Các đặc trưng vật lý được tính toán từ video nhằm mô tả hành vi chuyển động, ánh sáng, và chất lượng hình ảnh của từng cảnh quay. Đây là các yếu tố có tương quan mạnh với hành vi bạo lực — ví dụ: cảnh đánh nhau thường có chuyển động nhanh, rung mạnh, độ mờ cao và tương phản thay đổi đột ngột.  
Toàn bộ quá trình được hiện thực trong hàm extract(video\_input) của file VideoWorker.py, sử dụng OpenCV và NumPy để tính toán frame-level features.

#### **2.7.1 Frame Difference Mean (Trung bình độ khác biệt khung hình)**

* Đo lường mức độ thay đổi trung bình giữa hai khung hình liên tiếp.  
* Biểu hiện tổng quát cho mức độ chuyển động tổng thể trong video.  
* Giá trị cao → có nhiều chuyển động mạnh, cảnh quay sôi động, thường gặp trong hành vi xô xát hoặc đánh nhau.  
* Giá trị thấp → cảnh tĩnh, ít hoạt động, như người đi bộ hoặc nói chuyện bình thường.

#### **2.7.2 Frame Difference Variance (Phương sai độ khác biệt khung hình)**

* Đo sự không đồng đều trong chuyển động giữa các khu vực của ảnh.  
* Phản ánh mức độ đột ngột, giật cục, hoặc hỗn loạn của chuyển động.  
* Giá trị cao → có sự thay đổi mạnh ở một số vùng cục bộ (tay vung nhanh, camera rung), thường gắn với hành vi bạo lực.  
* Giá trị thấp → chuyển động đều, mượt, không có hành vi bất thường.

#### **2.7.3 Brightness (Độ sáng trung bình)**

* Đo độ sáng tổng thể của khung hình.  
* Cho biết mức độ chiếu sáng của cảnh quay – sáng, tối, hay thiếu sáng.  
* Cảnh quay tối thường xuất hiện trong môi trường thực tế như bãi giữ xe, ngõ hẹp, hoặc nơi không có ánh sáng tốt – những tình huống dễ xảy ra xung đột.  
* Độ sáng ổn định thể hiện môi trường bình thường, ít biến động.

#### **2.7.4 Contrast (Độ tương phản)**

* Đánh giá sự chênh lệch giữa vùng sáng và vùng tối trong khung hình.  
* Độ tương phản cao → xuất hiện nhiều thay đổi mạnh về ánh sáng (ví dụ: đèn nhấp nháy, chuyển động nhanh qua vùng sáng/tối).  
* Độ tương phản thấp → khung hình đều màu, tĩnh, không có biến động ánh sáng.  
* Đặc trưng này giúp phát hiện những đoạn video có nhiều chuyển động nhanh làm thay đổi ánh sáng, thường trùng với các cảnh bạo lực.

#### **2.7.5 Blur Level (Mức độ mờ ảnh)**

* Đánh giá độ sắc nét của khung hình.  
* Hình ảnh bị mờ khi có rung mạnh, di chuyển nhanh hoặc lấy nét kém.  
* Giá trị thấp (ảnh mờ) thường thấy trong cảnh quay hỗn loạn, camera rung do chuyển động đột ngột.  
* Giá trị cao (ảnh rõ) xuất hiện khi cảnh tĩnh hoặc camera cố định.  
* Đây là đặc trưng quan trọng vì video bạo lực thường bị rung hoặc mất nét do hành vi đột ngột.

#### **2.7.6 Optical Flow Magnitude (Độ lớn dòng quang học)**

* Đo lường tốc độ và hướng chuyển động tổng thể của các đối tượng trong cảnh.  
* Phản ánh “năng lượng chuyển động” của khung hình.  
* Giá trị cao → có chuyển động nhanh, hỗn loạn, đa hướng (tay chân vung mạnh, camera xoay).  
* Giá trị thấp → chuyển động nhẹ, đều (đi bộ, quay đầu, cử chỉ nhỏ).  
* Đặc trưng này giúp nhận diện hành vi bạo lực thông qua các mẫu chuyển động nhanh và không ổn định.

Các đặc trưng này phản ánh hành vi chuyển động, ánh sáng và chất lượng hình ảnh, giúp mô hình học được các pattern vật lý có liên quan đến hành vi bạo lực.

### **2.8 Chuẩn Hóa Dữ Liệu Phân Tích**

Sau khi trích xuất, dữ liệu trong Analysis\_result được làm sạch và điều chỉnh xác suất bằng biểu thức:

Với α\_non \= 0.7, α\_vio \= 1.3, giúp tái phân bổ xác suất theo độ tin cậy của mô hình. Giá trị cuối cùng bị giới hạn trong \[0.05, 0.95\] để tránh cực trị. Dữ liệu sau cùng được dùng cho giai đoạn hồi quy và trực quan hóa trong phần EDA.

Pipeline trên hình thành một chuỗi khép kín: thu thập → phân tích → lưu trữ → dự đoán → chuẩn hóa. Mỗi giai đoạn được tối ưu bằng đa luồng hoặc đa tiến trình, đảm bảo toàn bộ hệ thống có thể xử lý hàng trăm video trong thời gian ngắn với tính toàn vẹn dữ liệu và khả năng tái lập cao.

## **3\. Phân tích Dữ liệu với SQL (Exploratory Data Analysis – EDA)**

Phần này mô tả quy trình khai thác và phân tích dữ liệu video đã được lưu trong cơ sở dữ liệu SQLite (data.db) bằng cách sử dụng các truy vấn SQL. Toàn bộ phân tích tập trung vào việc hiểu cấu trúc dữ liệu, kiểm tra chất lượng thông tin, và phát hiện các mẫu hoặc bất thường trong mô hình dự đoán.

Các bảng chính được sử dụng trong CSDL:

* Labels: lưu thông tin về nhãn (violence, non\_violence).  
* Videos: ánh xạ giữa video và nhãn (video\_id, label\_id).  
* Metadata: lưu các thuộc tính kỹ thuật như fps, duration, resolution, file\_size.  
* AnalysisFeatures: chứa các giá trị xác suất và đặc trưng vật lý (frame\_diff, blur, brightness...).

### **3.1 Truy xuất N video đầu tiên theo nhãn**

Mục tiêu là xem nhanh các video thuộc một nhóm nhãn cụ thể để kiểm tra chất lượng gán nhãn hoặc chạy đánh giá mẫu.  
Quy trình:

1. Kết nối bảng Videos (chứa mã nhãn) với Labels (chứa tên nhãn thật).  
2. Lọc dữ liệu bằng điều kiện WHERE theo tên nhãn mong muốn.  
3. Giới hạn số lượng kết quả bằng LIMIT để chỉ lấy N video đầu tiên (ví dụ: 5).

Luồng xử lý giúp kiểm tra xem các video có được gán đúng nhãn không, đồng thời hỗ trợ xem mẫu đầu tiên của từng lớp dữ liệu.

![][image1]

![][image2]

### **3.2 Đếm số lượng video theo FPS (Frames Per Second)**

Bước này nhằm phân tích sự phân bố tốc độ khung hình trong toàn bộ tập dữ liệu, giúp phát hiện sự không đồng nhất (nếu có).  
 Cách thực hiện:

1. Truy cập bảng Metadata – nơi lưu thông tin kỹ thuật.  
2. Gom nhóm (GROUP BY) theo giá trị fps.  
3. Đếm (COUNT) số lượng video tương ứng mỗi nhóm.  
4. Sắp xếp kết quả theo số lượng giảm dần (ORDER BY).

Dữ liệu thu được giúp đánh giá xem phần lớn video nằm ở mức FPS nào (ví dụ 24fps, 30fps, 60fps). Nếu phân bố không đồng đều, cần chuẩn hóa trước khi huấn luyện để tránh bias theo tốc độ khung hình.

![][image3]

![][image4]

### **3.3 Tìm video có kích thước file lớn nhất và nhỏ nhất**

Mục tiêu

Mục tiêu của truy vấn này là xem nhanh hai trường hợp dữ liệu cực đoan: video có kích thước file (file\_size) lớn nhất và video có kích thước file nhỏ nhất. Việc này giúp kiểm tra sự phân bố của dữ liệu và xác định các điểm ngoại lai (outliers).

Quy trình

1. Tìm Giá trị Cực trị: Sử dụng hàm tổng hợp MAX() và MIN() để tìm ra kích thước file lớn nhất và nhỏ nhất từ bảng Metadata.  
2. Lọc dữ liệu: Lọc bảng Metadata bằng mệnh đề WHERE để chọn ra các video có kích thước khớp với giá trị cực trị tìm được.  
3. Hợp nhất Kết quả: Sử dụng toán tử UNION ALL để kết hợp kết quả của hai truy vấn riêng biệt (một cho MAX, một cho MIN) thành một bảng duy nhất.  
4. Gán Nhãn: Dùng AS để tạo cột THUOC\_TINH nhằm phân loại rõ ràng dòng nào là "LỚN NHẤT" và dòng nào là "NHỎ NHẤT".  
     
   ![][image5]  
   ![][image6]

### **3.4 Video có tỉ lệ bạo lực cao nhất** 

Mục tiêu là tìm tất cả các video mà mô hình đã dự đoán có xác suất bạo lực (violence\_probability) cao nhất trong toàn bộ tập dữ liệu. Việc này giúp kiểm tra chất lượng và sự phân loại của các mẫu dữ liệu cực đoan.

Quy trình

1. Tìm Giá trị Cực trị: Sử dụng truy vấn con (SELECT MAX()) để xác định giá trị violence\_probability lớn nhất (ví dụ: $0.95$).  
2. JOIN Bảng: Thực hiện phép JOIN giữa 4 bảng (Analysis\_result, Metadata, Videos, Labels) để lấy đầy đủ thông tin: ID, Tên video, Xác suất, và Tên nhãn.  
3. Lọc dữ liệu: Lọc kết quả bằng mệnh đề WHERE để chỉ hiển thị các video có xác suất khớp với giá trị cực trị.

![][image7]

![][image8]

### **3.5 Đếm số lượng video cho mỗi nhãn**

Bước này nhằm kiểm tra độ cân bằng của dữ liệu (class balance) – yếu tố quan trọng trong mô hình phân loại.  
 Luồng xử lý:

1. Kết nối bảng Videos với Labels bằng khóa label\_id.  
2. Gom nhóm (GROUP BY) theo tên nhãn (label\_name).  
3. Đếm (COUNT) số lượng video mỗi nhóm.

Kết quả cho thấy liệu dữ liệu có bị lệch nhãn không (ví dụ: 70% non-violence, 30% violence). Nếu mất cân bằng, cần điều chỉnh bằng kỹ thuật oversampling hoặc class weighting khi huấn luyện.

![][image9]

![][image10]

### **3.6 Số lượng video có tỉ lệ bạo lực cao nhất** 

Xác định tổng số lượng video có chung giá trị xác suất bạo lực cao nhất (0.95).

Quy trình

1. Tìm Giá trị Cực trị: Tương tự như trên, dùng MAX() để tìm xác suất cao nhất.  
2. Đếm: Sử dụng hàm COUNT() để đếm số lượng bản ghi có xác suất khớp với giá trị đó.  
   ![][image11]  
   ![][image12]

### **3.7 Tìm video “Non-Violence” có xác suất bạo lực cao**

Đây là một trong những truy vấn quan trọng nhất trong quá trình phân tích lỗi mô hình (Model Error Analysis).  
Mục tiêu: phát hiện các trường hợp mô hình dự đoán sai nghiêm trọng (False Positive).

Cách thực hiện:

1. Kết nối bảng Videos (chứa nhãn thật) với AnalysisFeatures (chứa xác suất mô hình).  
2. Lọc các video có label\_id \= 0 (non-violence).  
3. Lọc thêm điều kiện violence\_probability \> 0.8 – tức là mô hình rất “chắc chắn” rằng video này là bạo lực.  
4. Sắp xếp giảm dần theo xác suất để xem các mẫu “lỗi nặng” trước.

Luồng xử lý cho phép nhóm nghiên cứu phân tích:

* Vì sao mô hình nhầm lẫn? (do ánh sáng, chuyển động nhanh, nhiều người, camera rung…)  
* Những video nào cần gán nhãn lại hoặc loại bỏ khỏi dataset.

Đây là bước đánh giá hiệu suất mô hình theo hướng định tính, giúp tinh chỉnh dữ liệu huấn luyện, tái cân bằng class, hoặc điều chỉnh ngưỡng dự đoán (threshold tuning).

![][image13]

![][image14]

## **4\. Phân tích Dữ liệu với Python (Exploratory Data Analysis – EDA)**

Phần này sử dụng Python cùng các thư viện Pandas, NumPy, và Matplotlib/Seaborn để phân tích sâu bộ dữ liệu Analysis\_result.csv và các bảng liên quan (Metadata, Labels, Videos). Toàn bộ quá trình được hiện thực trong script analyzer.py,cho phép tự động hoá toàn bộ EDA qua các hàm yc1 → yc11.

### **4.1 Hiểu cấu trúc và sự sạch sẽ của dữ liệu**

Mục tiêu là đánh giá cấu trúc, kiểu dữ liệu, và độ sạch của các tệp CSV.  
Hàm yc1() lần lượt tải 4 bảng (Metadata, Videos, Labels, Analysis\_result) bằng pandas.read\_csv(). Sau đó, mỗi DataFrame được gọi .info() để hiển thị:

* Tổng số dòng (entries) và số cột (columns).  
* Kiểu dữ liệu (int64, float64, object, v.v).  
* Số lượng giá trị non-null trên từng cột.

Điều này giúp xác định:

* Có cột nào chứa giá trị bị thiếu (NaN).  
* Có cột nào bị đọc sai kiểu (ví dụ fps bị đọc thành chuỗi).  
* Đảm bảo mỗi bảng khớp logic về số dòng (video\_id trùng giữa Metadata và Analysis\_result).

Nếu phát hiện lỗi (ví dụ thiếu violence\_probability hoặc frame\_diff\_mean), dữ liệu được làm sạch bằng .dropna() hoặc .astype() để chuyển về đúng kiểu trước khi phân tích.

![][image15]

![][image16]

![][image17]![][image18]

![][image19]

### **4.2 Kiểm tra sự cân bằng giữa các nhãn (Label Balance)**

Hàm yc2() kiểm tra phân bố giữa hai lớp “Violent” và “Non-Violent”.

* Tải hai bảng Videos.csv và Labels.csv.  
* Gộp lại (pd.merge) qua label\_id để ánh xạ mỗi video với tên nhãn (label\_name).

* Đếm số lượng bằng .value\_counts().

Bước này xác định liệu tập dữ liệu có bị mất cân bằng (imbalanced) không.  
Nếu số lượng video non-violence \>\> violence, mô hình dễ bị bias, dự đoán lệch về lớp chiếm đa số.  
Kết quả thống kê này là cơ sở để áp dụng kỹ thuật cân bằng dữ liệu như class weighting, oversampling, hoặc focal loss trong huấn luyện MoViNet.

![][image20]

![][image21]

### **4.3 So sánh xác suất dự đoán giữa hai lớp**

Hàm yc3() dùng để so sánh mức dự đoán trung bình của mô hình cho từng nhóm nhãn.

* Gộp Analysis\_result và Videos qua video\_id.  
* Gom nhóm theo label\_id bằng .groupby('label\_id').  
* Tính trung bình violence\_probability cho mỗi nhóm.

Nếu mô hình hoạt động tốt, ta mong đợi:

* Trung bình của nhóm Violent ≈ 0.8–1.0.  
* Trung bình của nhóm Non-Violent ≈ 0.0–0.2.

Nếu hai giá trị gần nhau, điều đó cho thấy mô hình đang khó phân biệt hoặc overfit theo yếu tố nhiễu (ví dụ ánh sáng, độ mờ, camera rung).

![][image22]

![][image23]

### **4.4 Khám phá tương quan giữa đặc trưng và xác suất bạo lực**

Hàm yc4() tính ma trận tương quan Pearson giữa violence\_probability và các đặc trưng vật lý (frame\_diff\_mean, frame\_diff\_var, blur, brightness, contrast, optical\_flow).  
Kết quả biểu thị mức độ liên hệ tuyến tính giữa từng đặc trưng và khả năng dự đoán bạo lực:

* Giá trị tương quan dương cao (+) → đặc trưng tăng khi bạo lực tăng (ví dụ optical\_flow, frame\_diff).  
* Giá trị âm (-) → đặc trưng giảm khi bạo lực tăng (ví dụ brightness hoặc sharpness).  
* Gần 0 → không có tương quan tuyến tính rõ ràng.

Phân tích này giúp xác định đặc trưng vật lý nào có ảnh hưởng mạnh nhất đến kết quả dự đoán, từ đó hỗ trợ trực quan hóa bằng biểu đồ heatmap trong Power BI hoặc Seaborn.

![][image24]

![][image25]

### **4.5 Kiểm tra xu hướng thời lượng và điểm bạo lực**

Hàm yc5() kiểm tra xem video dài hơn có xu hướng nhận điểm bạo lực cao hơn hay không.

* Gộp Analysis\_result và Metadata qua video\_id.  
* Tính hệ số tương quan giữa duration và violence\_probability.

Nếu giá trị tương quan dương rõ rệt (\>0.3), mô hình có thể đang đánh giá thiên lệch theo độ dài video, thay vì nội dung.  
Ngược lại, nếu tương quan thấp, độ dài không ảnh hưởng đáng kể đến kết quả — chứng tỏ đặc trưng động học và nội dung khung hình mới là yếu tố chi phối.

![][image26]

![][image27]

### **4.6 Kiểm tra sự khác biệt FPS giữa các nhãn**

Hàm yc6() dùng để phát hiện thiên lệch về tốc độ khung hình (Frame Rate Bias) giữa các lớp.

* Lọc video “violence” và “non-violence” dựa trên tiền tố v và n trong video\_id.  
* Tính FPS trung bình từng nhóm bằng .mean().

Nếu FPS trung bình của nhóm violence cao hơn đáng kể (ví dụ 60 FPS so với 30 FPS), mô hình có thể “vô tình” học rằng FPS cao \= bạo lực, gây sai lệch khi áp dụng thực tế.  
Phân tích này giúp quyết định việc chuẩn hóa FPS về cùng mức (ví dụ 12\) trong pipeline preprocessing.

![][image28]

![][image29]

### **4.7 Xác định video có dự đoán bạo lực cao nhất**

Hàm yc7() sắp xếp DataFrame Analysis\_result theo violence\_probability và lấy ra 10 video cuối cùng (cao nhất).  
Các video này là những mẫu mà mô hình “rất chắc chắn” là bạo lực.  
 Mục đích:

* Kiểm tra thủ công để xác nhận mô hình đánh giá đúng không.  
* Phát hiện mẫu sai (ví dụ video non-violence nhưng có chuyển động mạnh khiến AI nhầm).  
* Dùng làm mẫu benchmark khi huấn luyện lại.

![][image30]

![][image31]

### **4.8 Xác định video có dự đoán bạo lực thấp nhất**

Ngược lại với yc7(), hàm yc8() lấy ra 10 video có xác suất thấp nhất.  
Các video này là “ít bạo lực nhất” hoặc False Negative (bạo lực thật nhưng mô hình không phát hiện).  
Phân tích này giúp nhận biết mô hình bỏ sót các hành vi nhẹ (như đẩy nhẹ, giằng co ngắn).

![][image32]

![][image33]

### **4.9 Kiểm tra tương quan độ sáng và tương phản với xác suất bạo lực**

Hàm yc9() tập trung vào mối quan hệ giữa ánh sáng (brightness), tương phản (contrast) và dự đoán của mô hình.

* Lọc 3 cột violence\_probability, brightness, contrast.  
* Tính ma trận tương quan và in ra hệ số.

Kết quả thường cho thấy:

* Brightness có tương quan âm: cảnh tối hơn → mô hình đánh giá bạo lực cao hơn (do video thiếu sáng dễ làm nhòe chuyển động).  
* Contrast có tương quan dương nhẹ: video có độ tương phản cao dễ thể hiện rõ biên chuyển động → mô hình phát hiện mạnh mẽ hơn.

Phân tích này gợi ý rằng mô hình nên được huấn luyện thêm các video có điều kiện ánh sáng đa dạng để tránh bias môi trường.

![][image34]

![][image35]

### **4.10 Kiểm tra ảnh hưởng của độ mờ (Blur)**

Hàm yc10() kiểm tra xem độ sắc nét (sharpness) ảnh hưởng thế nào đến dự đoán bạo lực.

* Tính tương quan giữa blur và violence\_probability.  
* In ra ma trận con hai cột.

Nếu giá trị tương quan dương rõ (\>0.3), mô hình có thể liên hệ độ mờ cao với hành vi bạo lực — hợp lý vì video bạo lực thường bị rung hoặc mất nét.  
Nếu tương quan âm hoặc gần 0, mô hình không bị ảnh hưởng bởi chất lượng hình ảnh — điều này thể hiện khả năng ổn định cao.

![][image36]

![][image37]

### **4.11 Phân tích mối quan hệ giữa chuyển động và bạo lực**

Đây là phần quan trọng nhất – đánh giá trực tiếp ảnh hưởng của đặc trưng động học.  
Hàm yc11() đo tương quan giữa violence\_probability với:

* optical\_flow: cường độ chuyển động vật thể.  
* frame\_diff\_mean: mức thay đổi trung bình giữa khung hình.  
* frame\_diff\_var: độ biến động chuyển động không đều.

Kết quả tương quan cho biết:

* Nếu optical\_flow và frame\_diff\_mean có tương quan dương cao (≈ \+0.5), chứng tỏ hành vi bạo lực gắn liền với chuyển động mạnh, liên tục, đa hướng.  
* Nếu frame\_diff\_var cao → cảnh bạo lực có chuyển động không ổn định, giật cục.

Đây là bằng chứng định lượng củng cố giả thuyết rằng “bạo lực \= chuyển động mạnh \+ hỗn loạn”.  
Những giá trị này được dùng làm nền cho việc trực quan hoá correlation matrix và scatter plot trong notebook analysis.ipynb, giúp giải thích vì sao mô hình MoViNet học tốt trên các đặc trưng động học.

![][image38]

![][image39]

### **4.12 Tổng kết quá trình phân tích Python**

1. Từ đọc dữ liệu (yc1) → kiểm tra cân bằng (yc2) → đánh giá xác suất (yc3) tạo nền cho hiểu mô hình.  
2. Từ yc4–yc11 tập trung xác định mối quan hệ giữa đặc trưng vật lý, thông số video và dự đoán của mô hình.  
3. Toàn bộ pipeline giúp:  
   * Kiểm tra tính nhất quán dữ liệu.  
   * Phát hiện thiên lệch hoặc lỗi mô hình.  
   * Đưa ra cơ sở trực quan cho Power BI, heatmap hoặc scatter analysis.

Kết quả phân tích cung cấp góc nhìn định lượng về hành vi của mô hình AI và mối tương quan giữa các đặc trưng vật lý của video và xác suất bạo lực, giúp nhóm tinh chỉnh thuật toán hoặc dataset cho giai đoạn xử lí tiếp theo.

## **5\. Phân tích trực quan dữ liệu**

Phần này trình bày chi tiết việc trực quan hóa các đặc trưng được trích xuất từ quá trình xử lý video trong tập dữ liệu bạo lực, nhằm hiểu sâu hơn về mối quan hệ giữa các đặc trưng vật lý (blur, optical flow, brightness, contrast, frame difference, v.v.) và xác suất bạo lực (violence\_probability) mà mô hình dự đoán.  
Các biểu đồ được vẽ bằng thư viện Seaborn và Matplotlib trên dữ liệu từ tệp Analysis\_result.csv, với các biểu đồ minh họa cho từng loại phân tích như sau.

### **5.1 Box Plot: Phân bố độ mờ (Blur) theo độ phân giải (res\_bucket)**

Biểu đồ hộp thể hiện sự thay đổi của chỉ số blur (độ mờ) trong các nhóm độ phân giải khác nhau. Các nhóm được chia theo mức: \<480p, 720p, 1080p, và 1440p+.

#### **5.1.1 Phân tích chi tiết**

* Trung bình giá trị blur tăng nhẹ theo độ phân giải, từ dưới 480p đến 1440p+.

* Ở nhóm 1440p+ xuất hiện nhiều điểm ngoại lai (outlier) có giá trị rất cao, vượt quá 40.000, cho thấy có những video có độ mờ bất thường.

* Nhóm 720p và 1080p có độ phân tán thấp hơn, cho thấy giá trị blur ở mức trung bình khá ổn định.

#### **5.1.2 Giải thích nguyên nhân**

* Khi độ phân giải cao hơn, lượng chi tiết trong mỗi khung hình tăng, khiến giá trị phương sai Laplacian (Laplacian variance) — chỉ số dùng để đo độ mờ — cũng tăng. Do đó, giá trị blur cao không nhất thiết có nghĩa là hình ảnh “mờ” về mặt cảm nhận, mà do sự nhạy cảm của phép đo.

* Một số video 1440p+ có thể bị nén hoặc xử lý qua các bộ lọc làm sắc nét, dẫn đến các giá trị cực trị.

* Ngoài ra, độ mờ còn chịu ảnh hưởng bởi các yếu tố khác như tốc độ chuyển động máy quay, điều kiện ánh sáng, và độ sâu trường ảnh (depth of field). 

* Một lý do khác của vấn đề nhóm 1440+ có nhiều giá trị outliers là do nguồn dữ liệu của nhóm là từ Youtube, đa số clip bạo lực đều bị người dùng che mờ một số phần để tránh bị nền tảng gỡ bỏ. Tuy nhiên do vẫn nhận dạng được hành động bạo lực nên nhóm quyết định giữ lại thay vì loại bỏ để có nhiều thông tin hữu ích hơn.

#### **5.1.3 Kết luận**

Không nên so sánh trực tiếp chỉ số blur giữa các nhóm độ phân giải, bởi sự khác biệt này phần lớn xuất phát từ cấu trúc pixel chứ không phải mức độ mờ thật.  
Để đánh giá công bằng hơn, cần chuẩn hóa chỉ số blur theo độ phân giải trước khi sử dụng trong mô hình hoặc trong phân tích thống kê.

![][image40]

![][image41]

### 

### **5.2 Heatmap: Ma trận tương quan giữa các đặc trưng**

Biểu đồ nhiệt thể hiện mối tương quan giữa các đặc trưng vật lý của video và xác suất bạo lực. Mỗi ô vuông biểu diễn hệ số tương quan Pearson trong khoảng từ \-1 (tương quan âm mạnh) đến \+1 (tương quan dương mạnh).

#### **5.2.1 Phân tích chi tiết**

* Hai đặc trưng frame\_diff\_mean và frame\_diff\_var có tương quan dương cao (0.69), điều này hợp lý vì cả hai cùng đo mức thay đổi giữa các khung hình.  
* contrast tương quan mạnh với frame\_diff\_var (0.73), chứng tỏ khi chuyển động tăng, độ tương phản giữa các khung hình cũng tăng.  
* optical\_flow có tương quan vừa phải (0.48–0.49) với cả frame\_diff\_mean và frame\_diff\_var, nghĩa là optical flow và frame difference đều phản ánh chuyển động nhưng ở hai cấp độ khác nhau.  
* violence\_probability có tương quan âm nhẹ với hầu hết các đặc trưng, dao động từ \-0.16 đến \-0.28.

#### **5.2.2 Giải thích nguyên nhân**

* Các video bạo lực thường có chuyển động cục bộ (local motion) thay vì chuyển động toàn khung hình (global motion). Do đó, optical flow trung bình hoặc contrast tổng thể có thể thấp hơn.  
* Một số video phi bạo lực như thể thao hoặc vlog lại có chuyển động lớn, khiến mô hình học nhầm rằng “chuyển động mạnh \= không bạo lực”.

#### **5.2.3 Kết luận**

Kết quả cho thấy mô hình hiện tại có thể thiên lệch ngược đối với các đặc trưng chuyển động.  
Để khắc phục, có thể xem xét:

* Tăng cường đặc trưng ngữ cảnh như âm thanh hoặc đối tượng (vũ khí, khuôn mặt, hành động).  
* Điều chỉnh trọng số hoặc thêm tầng phân tích chi tiết vùng chuyển động (region-based motion).

![][image42]

![][image43]

### **5.3 Histogram: Phân bố xác suất bạo lực (violence\_probability)**

Biểu đồ histogram mô tả phân bố tần suất của xác suất bạo lực mà mô hình dự đoán cho từng video.

#### **5.3.1 Phân tích chi tiết**

* Phân bố có dạng lệch trái: đa số video có xác suất thấp (\<0.3).  
* Một số lượng nhỏ video nằm ở vùng xác suất cao (\>0.8), cho thấy mô hình vẫn có khả năng nhận biết chính xác các trường hợp bạo lực rõ ràng.  
* Đường KDE (đường mật độ) thể hiện dạng phân bố không đối xứng, nghiêng về phía xác suất thấp.

#### **5.3.2 Giải thích nguyên nhân**

* Dữ liệu đầu vào có thể mất cân bằng, chứa nhiều video không bạo lực hơn, khiến mô hình có xu hướng dự đoán “an toàn”.  
* Các mẫu có xác suất cao thường có đặc trưng cực đoan, ví dụ ánh sáng gắt, độ tương phản thấp, hoặc chuyển động hỗn loạn – đây là những tín hiệu mà mô hình học được từ dữ liệu huấn luyện.

#### **5.3.3 Kết luận**

Phân bố này cho thấy mô hình thiên về lớp không bạo lực, một vấn đề phổ biến trong nhận dạng hành vi.  
Cần thực hiện các biện pháp cân bằng dữ liệu (oversampling, class weights) để mô hình đưa ra các dự đoán phân bố đều hơn và phản ánh đúng thực tế hơn.

![][image44]

![][image45]

### **5.4 Scatter Plot: Optical Flow và Frame Difference Mean**

Biểu đồ phân tán thể hiện mối quan hệ giữa hai đặc trưng chuyển động: optical\_flow (mức độ dịch chuyển điểm ảnh) và frame\_diff\_mean (mức thay đổi trung bình giữa các khung hình).

#### **5.4.1 Phân tích chi tiết**

* Các điểm dữ liệu tạo thành xu hướng dương rõ rệt: optical\_flow tăng thì frame\_diff\_mean cũng tăng.  
* Tuy nhiên, tồn tại một số ngoại lệ (optical\_flow cao nhưng frame\_diff\_mean thấp), thường là các video có chuyển động đều hoặc camera di chuyển ổn định.  
* Độ phân tán tăng dần theo optical\_flow, nghĩa là khi tốc độ chuyển động lớn hơn, độ biến thiên giữa các khung hình cũng đa dạng hơn.

#### **5.4.2 Giải thích nguyên nhân**

* Cả optical\_flow và frame\_diff\_mean đều đo chuyển động, nhưng optical\_flow tập trung vào vector dịch chuyển, trong khi frame\_diff\_mean phản ánh cường độ thay đổi pixel.

* Ngoại lệ xuất hiện khi khung hình thay đổi vị trí mà không đổi nội dung (ví dụ camera pan hoặc zoom chậm), khiến optical\_flow cao nhưng frame\_diff\_mean vẫn thấp.

#### **5.4.3 Kết luận**

Hai đặc trưng này phản ánh hai khía cạnh khác nhau của chuyển động và khi kết hợp sẽ mang lại thông tin phong phú hơn cho mô hình.  
Điều này xác nhận rằng việc giữ lại cả hai đặc trưng trong pipeline phân tích video là cần thiết để mô hình phân biệt được giữa chuyển động ổn định và chuyển động hỗn loạn.

![][image46]

![][image47]

### **5.5 Line Chart: Xu hướng xác suất bạo lực theo Frame Difference Mean**

Biểu đồ đường thể hiện mối quan hệ giữa mức thay đổi trung bình khung hình (frame\_diff\_mean) và xác suất bạo lực (violence\_probability) trung bình.

#### **5.5.1 Phân tích chi tiết**

* Khi frame\_diff\_mean tăng, xác suất bạo lực trung bình giảm dần từ khoảng 0.55 xuống 0.30.  
* Một vài đoạn dao động nhẹ (tăng đột ngột tại vùng 170–200), có thể do số lượng mẫu trong bin thấp dẫn đến trung bình không ổn định.  
* Xu hướng tổng thể là nghịch biến, tức là video có chuyển động mạnh hơn không đồng nghĩa với mức độ bạo lực cao hơn.

#### **5.5.2 Giải thích nguyên nhân**

* Nhiều video có chuyển động lớn nhưng không bạo lực, ví dụ thể thao, nhảy múa, hoặc video hành động nhanh.

* Cảnh bạo lực thật thường tập trung vào vùng nhỏ (tay, vật thể, khuôn mặt), trong khi cảnh nền ít thay đổi → giá trị frame\_diff\_mean nhỏ.

* Do đó, chỉ sử dụng chuyển động tổng thể không đủ để xác định bạo lực.

#### **5.5.3 Kết luận**

Xu hướng giảm này hợp lý và phản ánh đúng bản chất của dữ liệu: chuyển động mạnh toàn cảnh không nhất thiết là bạo lực.  
Cần phát triển thêm các đặc trưng local motion hoặc spatial attention để phát hiện những vùng chuyển động có tính chất bạo lực cụ thể.

![][image48]

![][image49]

## **6\. Phân tích hồi quy (Regression Analysis)**

Phần này nhằm kiểm tra khả năng dự đoán xác suất bạo lực (violence\_probability) dựa hoàn toàn trên các đặc trưng vật lý của video (như blur, contrast, brightness, optical flow, frame difference).  
Phương pháp sử dụng là hồi quy tuyến tính (Linear Regression) – mô hình đơn giản nhất trong học máy – để đánh giá xem liệu giữa các đặc trưng vật lý và mức độ bạo lực có tồn tại mối quan hệ tuyến tính hay không.

Dữ liệu được lấy trực tiếp từ Analysis\_result.csv, trong đó mỗi dòng tương ứng với một video đã được phân tích và gán xác suất bạo lực bởi mô hình MoViNet.

### **6.1 Mục tiêu của hồi quy**

Mục tiêu chính là đánh giá mức độ ảnh hưởng tuyến tính của các yếu tố vật lý (như độ mờ, độ sáng, mức chuyển động) tới xác suất bạo lực.  
Nếu mối quan hệ này tuyến tính, mô hình hồi quy sẽ giải thích được một phần đáng kể phương sai (variance) của violence\_probability.

Tuy nhiên, nếu chỉ số đánh giá thấp (R² gần 0), điều đó chứng tỏ mối quan hệ là phi tuyến tính, tức là hành vi bạo lực không thể được mô tả bằng một đường thẳng trong không gian đặc trưng vật lý.

### **6.2 Chuẩn bị dữ liệu cho hồi quy**

#### **6.2.1 Xác định biến và chia tập dữ liệu**

* Đầu vào (X):  
  Các đặc trưng vật lý gồm optical\_flow, frame\_diff\_mean, frame\_diff\_var, blur, brightness, contrast.  
  Đây là những đặc trưng mô tả chuyển động, ánh sáng và chất lượng hình ảnh của từng video.  
* Đầu ra (y):  
  Biến mục tiêu là violence\_probability, tức là xác suất mà mô hình MoViNet đánh giá video là bạo lực.  
* Phân chia dữ liệu:  
  Dữ liệu được chia thành hai tập:  
  * 80%  dùng để huấn luyện mô hình (X\_train, y\_train).  
  * 20% còn lại dùng để kiểm thử (X\_test, y\_test)  
     Việc chia ngẫu nhiên bằng train\_test\_split(..., random\_state=199) giúp đảm bảo khả năng tái lập kết quả  
    main.

#### **6.2.2 Chuẩn hóa đặc trưng (Standard Scaling)**

Do các đặc trưng có thang đo khác nhau (ví dụ blur hàng nghìn, contrast chỉ vài chục), việc chuẩn hóa bằng StandardScaler là cần thiết.  
 Bộ biến đổi này đưa mọi đặc trưng về trung bình 0 và độ lệch chuẩn 1, đảm bảo không đặc trưng nào chiếm ưu thế trong quá trình huấn luyện.

* Quy trình kỹ thuật:  
  Scaler được fit trên tập huấn luyện (để học trung bình và độ lệch chuẩn) và transform cả hai tập train/test.  
  Điều này giúp tránh data leakage – tức là không để dữ liệu kiểm thử ảnh hưởng đến mô hình trong giai đoạn huấn luyện.

### **6.3 Kết quả thực nghiệm và phân tích**

#### **6.3.1 Huấn luyện mô hình hồi quy tuyến tính**

Mô hình LinearRegression trong thư viện scikit-learn được huấn luyện với dữ liệu đã chuẩn hóa.  
Sau khi huấn luyện, mô hình được dùng để dự đoán xác suất bạo lực trên tập kiểm thử (y\_pred).  
Kết quả được đánh giá bằng hai chỉ số:

* R² (Coefficient of Determination): đo lường phần trăm phương sai của y được giải thích bởi mô hình.

* MAE (Mean Absolute Error): độ chênh lệch trung bình tuyệt đối giữa dự đoán và thực tế.

Trong thí nghiệm, các giá trị thu được như sau:

* R² ≈ 0.085 – 0.093

* MAE ≈ 0.21

  #### **6.3.1.1 Phân tích kết quả**

Sau khi thực hiện hồi quy bằng phương pháp tuyến tính, các chỉ số đánh giá  hiệu suất của mô hình đã được thu thập và trình bày trong bảng kết quả dưới đây.	

| Test size | Random state  | R²  | MAE  | RMSE  |
| :---- | :---- | :---- | :---- | :---- |
| 0.2 | 42 | 0.0232 | 0.2107 | 0.2455 |
| 0.2 | 100 | 0.0267 | 0.2107 | 0.2590 |
| 0.3 | 42 | 0.0869 | 0.2087 | 0.2450 |
| **0.3** | **100** | **0.0934**  | **0.2075**  | **0.2468** |

	

Các chỉ số đánh giá chính bao gồm:

- **R² (R-squared):** Chỉ số xác định. Đo lường mức độ các biến độc lập giải thích được sự biến thiên của biến phụ thuộc. Giá trị càng gần 1 càng tốt.  
- **MAE (Mean Absolute Error):** Sai số tuyệt đối trung bình. Càng thấp càng tốt.  
- **RMSE (Root Mean Squared Error):** Căn bậc hai của sai số bình phương trung bình. Chỉ số này phạt nặng hơn cho các lỗi dự đoán lớn. Càng thấp càng tốt.

Để thử nghiệm xem có thể cải thiện mô hình bằng cách thay đổi tham số hay không, phần này sẽ tiến hành phân tích ảnh hưởng của text\_size (tỷ lệ dữ liệu kiểm thử) và  (giá trị khởi tạo ngẫu nhiên) đến các chỉ số đánh giá.

##### **6.3.1.2 Phân tích chi tiết các thử nghiệm**

Các trường hợp trong bảng được phân tích theo trình tự thay đổi tham số:

**Trường hợp 1: test\_size \= 0.2 và random\_state \= 42 (Cơ sở)**

* **R²:** 0.0232 (2.32%)  
* **MAE:** 0.2107  
* **RMSE:** 0.2455

**Nhận xét:** Đây là cấu hình cơ sở. Giá trị **R² cực kỳ thấp** (chỉ 2.32%), cho thấy mô hình gần như không giải thích được sự biến thiên của dữ liệu và hoạt động rất kém.

**Trường hợp 2: Thay đổi random\_state (từ 42 thành 100\)**

* **Cấu hình:** test\_size \= 0.2, random\_state \= 100  
* **R²:** 0.0267 (tăng nhẹ)  
* **MAE:** 0.2107 (không đổi)  
* **RMSE:** 0.2590 (tăng)

**Nhận xét:** Khi giữ nguyên tỷ lệ chia 80-20 nhưng thay đổi cách chia ngẫu nhiên, R² tăng nhẹ nhưng RMSE lại tăng đáng kể. Điều này cho thấy mô hình **không ổn định (unstable)**. Tùy thuộc vào việc các điểm dữ liệu nào được chọn vào tập huấn luyện/kiểm thử, hiệu suất có thể thay đổi.

**Trường hợp 3: Thay đổi test\_size (từ 0.2 thành 0.3)**

* **Cấu hình:** test\_size \= 0.3, random\_state \= 42  
* **R²:** 0.0869 (tăng đáng kể)  
* **MAE:** 0.2087 (giảm nhẹ)  
* **RMSE:** 0.2450 (giảm nhẹ)

**Nhận xét:** Khi tăng test\_size lên 0.3 (giảm dữ liệu huấn luyện từ 80% xuống 70%), hiệu suất mô hình cải thiện rõ rệt. R² tăng gần 4 lần (từ 2.32% lên 8.69%). Cả hai chỉ số lỗi MAE và RMSE đều giảm.

**Trường hợp 4: Thay đổi cả hai tham số**

* **Cấu hình:** test\_size \= 0.3, random\_state \= 100  
* **R²:** 0.0934 (cao nhất)  
* **MAE:** 0.2075 (thấp nhất)  
* **RMSE:** 0.2468 (tăng so với trường hợp 3\)

**Nhận xét:** Đây là cấu hình cho ra **R² cao nhất (9.34%)** và **MAE thấp nhất (0.2075)** trong bốn thử nghiệm. Tuy nhiên, tương tự trường hợp 2, việc chuyển sang random\_state \= 100 lại làm tăng RMSE (so với random\_state \= 42 ở trường hợp 3), một lần nữa cho thấy sự thiếu ổn định của mô hình.

##### **6.3.1.3 Kết luận chung từ phân tích**

Từ việc phân tích bảng kết quả, có thể rút ra các nhận xét sau:

1. **Hiệu suất mô hình rất thấp:** Mặc dù đã có sự cải thiện khi thay đổi tham số, giá trị **R² cao nhất cũng chỉ đạt 0.0934** (khoảng 9.3%). Con số này nhất quán với kết quả tổng quát (R² ≈ 0.085 – 0.093) đã nêu ở mục 6.3.1. Điều này khẳng định mô hình hồi quy tuyến tính hiện tại **hoạt động không hiệu quả**, không có khả năng giải thích hoặc dự đoán biến mục tiêu.  
2. **Sự dao động của R² (Mô hình không ổn định):** Việc thay đổi random\_state (tức thay đổi cách chia dữ liệu) gây ra biến động đáng kể trong kết quả (ví dụ: R² dao động từ 0.0232 đến 0.0934). Điều này chứng tỏ mô hình **không ổn định (high variance)**. Một mô hình tốt nên cho kết quả tương đối nhất quán.  
3. **Ảnh hưởng của test\_size:** Việc tăng test\_size từ 0.2 lên 0.3 (giảm dữ liệu huấn luyện) đã cải thiện hiệu suất.  
4. **Hướng cải thiện:** Do R² quá thấp, cần xem xét lại toàn bộ mô hình. Các bước tiếp theo có thể bao gồm:  
   * Thử nghiệm các thuật toán hồi quy khác (ví dụ: Random Forest Regression, Gradient Boosting).  
   * Thực hiện thêm kỹ thuật xử lý đặc trưng (feature engineering).  
   * Kiểm tra lại xem các biến đầu vào (features) có thực sự liên quan đến biến mục tiêu (target) hay không.

#### **6.3.2 Huấn luyện mô hình hồi quy Random forest**

Do mô hình Hồi quy tuyến tính (Linear Regression) ở phần trước cho kết quả rất thấp  , không có khả năng giải thích dữ liệu, một thuật toán mạnh mẽ hơn là **Random Forest Regression** (Hồi quy Rừng ngẫu nhiên) được đưa vào thử nghiệm để xem có thể cải thiện hiệu suất hay không.

Thuật toán này hoạt động bằng cách xây dựng nhiều cây quyết định (estimators) trong quá trình huấn luyện và xuất ra giá trị trung bình của các cây. Các tham số chính được tinh chỉnh bao gồm n estimators (số lượng cây) và max\_depth (độ sâu tối đa của mỗi cây).

Kết quả thử nghiệm với các tham số khác nhau được trình bày trong bảng dưới đây:

| Test size | Random state | N estimators | Max depth | R²  | MAE | RMSE  |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| 0.2 | 100 | 100 | 3 | 0.0585 | 0.2106 | 0.2515 |
| 0.3 | 100 | 200 | 3 | 0.0741 | 0.2106 | 0.2494 |
| 0.3 | 100 | 500 | 3 | 0.0767 | 0.2106 | 0.2491 |
| **0.3** | **100** | **100** | **2** | **0.0850**  | **0.2106** | **0.2480**  |

**6.3.2.1 Phân tích chi tiết các thử nghiệm**  
**Trường hợp 1: Cấu hình cơ sở**

* **Cấu hình:** test\_size \= 0.2, random\_state \= 100, n\_estimators \= 100, max\_depth \= 3  
* **R²:** 0.0585  
* **MAE:** 0.2106  
* **RMSE:** 0.2515

**Nhận xét:** Với cấu hình cơ sở, mô hình Random Forest cho kết quả  **R²(5.85%)** còn thấp hơn cả Hồi quy tuyến tính. Chỉ số lỗi RMSE cũng cao hơn.

**Trường hợp 2: Tăng test\_size (0.3) và n\_estimators (200)**

* **Cấu hình:** test\_size \= 0.3, random\_state \= 100, n\_estimators \= 200, max\_depth \= 3  
* **R²:** 0.0741 (tăng)  
* **MAE:** 0.2106 (không đổi)  
* **RMSE:** 0.2494 (giảm nhẹ)

**Nhận xét:** Việc tăng test\_size (tương tự như Hồi quy tuyến tính) và tăng số lượng cây (từ 100 lên 200\) giúp cải thiện **R²**và RMSE, cho thấy mô hình ổn định hơn một chút.

**Trường hợp 3: Tăng mạnh n estimators (500)**

* **Cấu hình:** test\_size \= 0.3, random\_state \= 100, n\_estimators \= 500, max\_depth \= 3  
* **R²:** 0.0767 (tăng nhẹ)  
* **MAE:** 0.2106 (không đổi)  
* **RMSE:** 0.2491 (giảm nhẹ)

**Nhận xét:** Tăng số lượng cây lên 500 chỉ mang lại cải thiện không đáng kể so với 200 cây. Điều này cho thấy n\_estimators \= 200 có thể đã đủ, hoặc max\_depth \= 3 đang là yếu tố giới hạn hiệu suất.

**Trường hợp 4: Giảm max\_depth (2)**

* **Cấu hình:** test\_size \= 0.3, random\_state \= 100, n\_estimators \= 100, max\_depth \= 2  
* **R²:** 0.0850 (cao nhất)  
* **MAE:** 0.2106 (không đổi)  
* **RMSE:** 0.2480 (thấp nhất)

**Nhận xét:** Đây là cấu hình cho kết quả tốt nhất trong các thử nghiệm, với **R² đạt 0.085** và **RMSE thấp nhất (0.2480)**. Đáng chú ý, một mô hình *đơn giản hơn* (độ sâu max\_depth \= 2\) lại hoạt động hiệu quả hơn mô hình phức tạp (max\_depth \= 3).

**6.3.2.2 Kết luận chung**

1. **Mô hình vẫn thất bại:** Mặc dù đã sử dụng một thuật toán phức tạp và mạnh hơn là Random Forest, chỉ số **R² cao nhất cũng chỉ đạt 0.0850**. Kết quả này tương đương với mô hình Hồi quy tuyến tính (vốn cũng đạt **R² \= 0.09**).  
2. **MAE không đổi:** Một điểm bất thường là chỉ số MAE giữ nguyên giá trị **0.2106** trong mọi thử nghiệm của Random Forest.  
3. **Kết luận cuối cùng:** Việc cả hai mô hình (Tuyến tính và Rừng ngẫu nhiên) đều thất bại trong việc dự đoán, với chỉ số **R²** rất thấp (dưới 0.1), cho thấy vấn đề không nằm ở việc lựa chọn thuật toán. Nguyên nhân chính gần như chắc chắn là do **các đặc trưng (features) đầu vào không có đủ khả năng giải thích hoặc không có mối quan hệ đủ mạnh** với biến mục tiêu cần dự đoán.

   #### **6.3.3 Huấn luyện mô hình hồi quy Gradient boosting**

Tiếp tục nỗ lực tìm kiếm một mô hình phù hợp, thuật toán **Gradient Boosting Regression** được đưa vào thử nghiệm. Đây là một thuật toán boosting mạnh mẽ, hoạt động bằng cách xây dựng các mô hình (cây quyết định) một cách tuần tự, trong đó mỗi mô hình mới sẽ cố gắng sửa lỗi của mô hình trước đó.

Các tham số được tinh chỉnh bao gồm n estimators (số lượng cây) và learning rate (tỷ lệ học, kiểm soát mức độ đóng góp của mỗi cây).

Kết quả thử nghiệm được trình bày trong bảng dưới đây:

| Test size | Random state |  Estimators | Learning rate | Max depth | R²  | MAE  | RMSE  |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| 0.3 | 100 | 100 | 0.1 | 3 | 0.0079 | 0.2114 | 0.2582 |
| 0.3 | 100 | 500 | 0.01 | 3 | 0.0540 | 0.2093 | 0.2521 |
| 0.2 | 100 | 500 | 0.01 | 3 | 0.0203 | 0.2257 | 0.2668 |
| **0.3** | **100** | **100** | **0.01** | **2** | **0.0756**  | **0.2091**  | **0.2492**  |

**6.3.3.1 Phân tích chi tiết các thử nghiệm**  
**Trường hợp 1: Cấu hình cơ sở**

* **Cấu hình:** test\_size \= 0.3, n\_estimators \= 100, learning\_rate \= 0.1  
* **R²:** 0.0079  
* **MAE:** 0.2114  
* **RMSE:** 0.2582

**Nhận xét:** Với cấu hình này, mô hình cho kết quả **R²** gần như bằng 0 (chỉ 0.79%). Đây là kết quả tệ nhất trong tất cả các thử nghiệm cho đến nay, cho thấy mô hình hoàn toàn không học được gì từ dữ liệu.

**Trường hợp 2: Tăng n\_estimators (500) và giảm learning\_rate (0.01)**

* **Cấu hình:** test\_size \= 0.3, n\_estimators \= 500, learning\_rate \= 0.01  
* **R²:** 0.0540 (tăng)  
* **MAE:** 0.2093 (thấp nhất)  
* **RMSE:** 0.2521 (giảm)

**Nhận xét:** Việc tăng số lượng cây và giảm tỷ lệ học giúp cải thiện đáng kể **R²**và giảm cả hai chỉ số lỗi. Đây là cấu hình tốt nhất cho Gradient Boosting, tuy nhiên, **R²**(5.4%) vẫn ở mức rất thấp.

**Trường hợp 3: Thay đổi test\_size (0.2)**

* **Cấu hình:** test\_size \= 0.2, n\_estimators \= 500, learning\_rate \= 0.01  
* **R²:** 0.0203 (giảm mạnh)  
* **MAE:** 0.2257 (tăng mạnh)  
* **RMSE:** 0.2668 (tăng mạnh)

**Nhận xét:** Khi giữ nguyên các tham số tốt nhất của mô hình (từ trường hợp 2\) nhưng giảm test\_size xuống 0.2 (tăng dữ liệu huấn luyện lên 80%), hiệu suất giảm sút nghiêm trọng. Điều này một lần nữa củng cố nhận định từ các mô hình trước: việc sử dụng nhiều dữ liệu huấn luyện hơn (80%) dường như đang gây hại cho hiệu suất, có thể do *overfitting* hoặc dữ liệu nhiễu.

**Trường hợp 4: Giảm learning rate (0.01) và giảm max depth(2)** 

* **Cấu hình:** test\_size \= 0.3, n\_estimators \= 100, learning\_rate \= 0.01  
* **R²:** **0.0756** (Tăng mạnh)  
* **MAE: 0.2091 (**giảm**)**  
* **RMSE:** **0.2492** (Thấp nhất)

**Nhận xét:** Mô hình Gradient Boosting Regression  đạt kết quả tốt nhất (**R²** cao nhất) với cấu hình: learning\_rate=0.01 và max\_depth=2.Sự kết hợp này giúp **R²** đạt 7.56% và RMSE thấp nhất là 0.2492.Chiến lược quan trọng nhất là giảm max\_depth xuống 2\. Điều này buộc mô hình giữ các quy tắc cực kỳ đơn giản và nông, giúp nó tránh học vẹt (overfitting) các chi tiết nhiễu ngẫu nhiên, từ đó nâng cao khả năng khái quát hóa.

		**6.3.3.2 Kết luận chung**

1. **Gradient Boosting thất bại:** Tương tự như Hồi quy tuyến tính và Random Forest, mô hình Gradient Boosting cũng **hoàn toàn thất bại**. Kết quả **R²** tốt nhất mà nó đạt được (0.0540) thậm chí còn thấp hơn cả hai mô hình trước đó.  
2. **Kết luận cuối cùng về hồi quy:** Sau khi thử nghiệm ba thuật toán hồi quy với các bản chất khác nhau (Tuyến tính, Bagging \- Random Forest, và Boosting \- Gradient Boosting), tất cả đều cho chỉ số **R²** dưới 0.1. Điều này cung cấp bằng chứng mạnh mẽ rằng **vấn đề không nằm ở việc lựa chọn mô hình**. Nguyên nhân gốc rễ là **các đặc trưng (features) đầu vào không chứa đủ thông tin hoặc không có mối tương quan đủ mạnh để có thể dự đoán được biến mục tiêu.**

### **6.4 Kết luận chung về các mô hình hồi quy**

Sau khi tiến hành thử nghiệm với ba thuật toán hồi quy có bản chất khác nhau:

1. Hồi quy tuyến tính (Linear Regression)  
2. Hồi quy Rừng ngẫu nhiên (RandomForestRegressor)  
3. Hồi quy Tăng cường Gradient (GradientBoostingRegressor)

Có thể rút ra một kết luận chung và rõ ràng: Không có mô hình nào trong số này hoạt động hiệu quả trên tập dữ liệu được cung cấp.

Phân tích tổng hợp

* Chỉ số R² (R-squared) cực kỳ thấp: Chỉ số **R²** tốt nhất đạt được trong tất cả các thử nghiệm là 0.0934 (từ mô hình Hồi quy tuyến tính, Trường hợp 4). Các thuật toán phức tạp hơn như Random Forest (**R²** cao nhất \= 0.0850) và Gradient Boosting (**R²** cao nhất \= 0.0540) thậm chí còn cho kết quả tệ hơn.  
* Ý nghĩa: Một giá trị **R²** dưới 0.1 cho thấy rằng các mô hình (ngay cả mô hình tốt nhất) chỉ có thể giải thích được dưới 10% sự biến thiên của biến mục tiêu. Điều này đồng nghĩa với việc các dự đoán của mô hình gần như không có giá trị và không tốt hơn đáng kể so với việc chỉ dự đoán bằng giá trị trung bình của dữ liệu.  
* Vấn đề không nằm ở thuật toán: Việc cả ba loại mô hình (tuyến tính, bagging, và boosting) đều thất bại cho thấy vấn đề không nằm ở việc *lựa chọn thuật toán*. Việc sử dụng các mô hình phi tuyến, phức tạp (Random Forest, Gradient Boosting) đã không mang lại bất kỳ cải thiện nào so với mô hình tuyến tính đơn giản.  
* Lý do các mô hình không đạt được kết quả cao là do chỉ số xác suất bạo lực được lấy ra từ một mô hình Deep Learning được huấn luyện để nhận biệt các khung xương chuyển động nhằm phân loại bạo lực hay không. Chính vì vậy, nên các đặc trưng vật lý như độ sáng, độ mờ,... chỉ phản ánh một phần tương quan rất nhỏ so với xác suất bạo lực. 

## **7\. Trực Quan Hóa Kết Quả Trên PowerBI:**

### **7.1 Trực quan hóa biểu đồ trên power BI**

	

![][image50]

![][image51]

![][image52]

![][image53]

### **7.2 Trực quan hóa so sánh hiệu suất các mô hình hồi quy trên power BI**

![][image54]

![][image55]

![][image56]

## **8\. Kết luận và hướng phát triển**

### **8.1 Tổng kết**

Dự án đã triển khai một quy trình hoàn chỉnh gồm:

* Thu thập và xử lý video;  
* Fine-tuning mô hình MoViNet;  
* Trích xuất đặc trưng và phân tích chuyên sâu bằng SQL, Python, và các biểu đồ thống kê;  
* Kiểm tra mối quan hệ tuyến tính giữa các đặc trưng vật lý và xác suất bạo lực.

Qua quá trình phân tích (EDA) và thực nghiệm hồi quy, dự án đã rút ra được những kết luận quan trọng:

1. **Mô hình Học sâu (MoViNet) hoạt động dựa trên các đặc trưng phức tạp:** Quá trình phân tích trực quan cho thấy các mối quan hệ không trực quan. Ví dụ, video có chuyển động tổng thể (frame\_diff\_mean) cao hơn lại có xu hướng nhận xác suất bạo lực *thấp hơn* . Điều này cho thấy MoViNet đã học được cách phân biệt "chuyển động hỗn loạn" của bạo lực (thường là cục bộ) với "chuyển động cao" của các hoạt động phi bạo lực (như thể thao, nhảy múa).  
2. **Đặc trưng vật lý không đủ để giải thích bạo lực:** Đây là phát hiện cốt lõi của dự án. Trong Phân tích hồi quy , ba mô hình khác nhau (Linear Regression, Random Forest, và Gradient Boosting) đã được thử nghiệm để dự đoán violence\_probability (đầu ra của MoViNet) chỉ dựa trên các đặc trưng vật lý (blur, brightness, optical\_flow, v.v.).  
3. **Tất cả các mô hình hồi quy đều thất bại:** Kết quả tốt nhất thu được chỉ đạt **R² \=** 0.0934. Chỉ số **R²** dưới 0.1 khẳng định rằng **không có mối quan hệ tuyến tính (hoặc phi tuyến đơn giản) nào** giữa các đặc trưng vật lý và khả năng phát hiện bạo lực của mô hình học sâu.

**Kết luận cuối cùng:** Mô hình MoViNet đang nhận diện bạo lực dựa trên các mẫu (pattern) trừu tượng, phức tạp và phi tuyến tính (như tư thế con người, sự tương tác giữa các đối tượng, hoặc các thay đổi chuyển động vi mô) mà các chỉ số thống kê vật lý đơn giản không thể nắm bắt được. Điều này khẳng định giá trị và sự cần thiết của phương pháp học sâu cho bài toán phức tạp này.

### **8.2 Hạn chế**

1. Dữ liệu nhỏ và mất cân bằng:  
    Số lượng video chưa đủ lớn, tỉ lệ giữa hai lớp lệch nhiều, ảnh hưởng mạnh đến khả năng khái quát.  
2. Gán nhãn thủ công:  
    Việc gán nhãn có tính chủ quan, đặc biệt với các video hành động hoặc thể thao – dễ gây nhiễu cho mô hình.  
3. Đặc trưng giới hạn:  
    Chỉ dựa trên đặc trưng hình ảnh, bỏ qua âm thanh và ngữ cảnh hành vi, vốn là yếu tố quan trọng trong nhận dạng bạo lực.

### **8.3 Hướng phát triển**

1. Mở rộng mô hình hồi quy phi tuyến:  
    Áp dụng các mô hình mạnh hơn như Random Forest, XGBoost, hoặc mạng Neural Network để mô hình hóa mối quan hệ phi tuyến giữa đặc trưng vật lý và xác suất bạo lực.  
2. Tích hợp đặc trưng âm thanh:  
    Kết hợp đặc trưng âm thanh như MFCC, năng lượng phổ, hoặc nhịp điệu (beat) để bổ sung yếu tố cảm xúc và âm thanh bạo lực.  
3. Phát hiện đối tượng trong khung hình:  
    Dùng các mô hình phát hiện như YOLOv8 hoặc Detectron2 để nhận diện các đối tượng cụ thể (vũ khí, nắm đấm, khuôn mặt).  
4. Mô hình đa phương thức (Multimodal):  
    Kết hợp thông tin hình ảnh, âm thanh và chuyển động để tăng độ tin cậy trong nhận diện bạo lực.  
5. Triển khai thời gian thực:  
    Tối ưu hóa pipeline của MoViNet (vốn được thiết kế cho mobile/edge) để phân tích video trực tuyến, tự động phát hiện và cảnh báo khi có hành vi bạo lực trong camera giám sát.

**9\. Tài liệu tham khảo**

\[1\] D. Hassner, Y. Itcher, and O. Klafper, “Violent Flows: Real-Time Detection of Violent Crowd Behavior,” *CVPR Workshops*, 2012\.

\[2\] F. Nievas, M. Suarez, G. Gambardella, and R. Montes, “Violence Detection in Video Using Computer Vision Techniques,” *CIARP*, 2011\.

\[3\] M. Bilinski et al., “A Survey on Violence Detection in Videos,” *Multimedia Tools and Applications*, Springer, 2021\.

\[4\] D. Kondratyuk, L. Guo, B. Zoph et al., “MoViNets: Mobile Video Networks for Efficient Video Recognition,” *CVPR*, 2021\.

\[5\] J. Carreira and A. Zisserman, “Quo Vadis, Action Recognition? A New Model and the Kinetics Dataset,” *CVPR*, 2017\.

\[6\] A. Krizhevsky et al., “Imagenet Classification with Deep Convolutional Neural Networks,” *NeurIPS*, 2012\.

\[7\] G. Farnebäck, “Two-Frame Motion Estimation Based on Polynomial Expansion,” *Scandinavian Conference on Image Analysis*, 2003\.

\[8\] A. Bovik, *Handbook of Image and Video Processing*, Academic Press, 2010\.

\[9\] S. Sultani, C. Chen, and M. Shah, “Real-World Anomaly Detection in Surveillance Videos,” *CVPR*, 2018\.

\[10\] G. James, D. Witten, T. Hastie, and R. Tibshirani, *An Introduction to Statistical Learning*, Springer, 2021\.

\[11\] L. Breiman, “Random Forests,” *Machine Learning*, 2001\.

\[12\] J. Friedman, “Greedy Function Approximation: A Gradient Boosting Machine,” *Annals of Statistics*, 2001\.

\[14\] TensorFlow Lite Team, “TensorFlow Lite: Deploy Machine Learning Models on Mobile and Edge Devices,” *Google Developers*, 2020\.

\[15\] R. Sahu, S. Verma, and A. Tiwari, “Violence Detection in Surveillance Videos: A Deep Learning Perspective,” *IEEE Access*, 2022\.

\[16\] S. Tripathi et al., “Human Violence Detection Using Deep Learning in Surveillance Videos,” *Neurocomputing*, 2023\.
