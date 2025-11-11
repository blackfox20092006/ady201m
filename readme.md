# **PROJECT: ANALYSIS, VISUALIZATION, AND VIOLENCE DETECTION IN VIDEOS USING COMPUTER VISION AND DEEP LEARNING**

**Instructor**: Nguyễn Hoàng Linh  

| Team Members | [Hoàng Quang Nhân](https://github.com/blackfox20092006) - Team Leader - SE204283 |
| :---: | :---- |
|  | [Lê Phan Thanh Nghi](https://github.com/thanh-nghi) - Member - SE203909 |
|  | [Bùi Xuân Hoan](https://github.com/DOMEMON) - Member - SE204139 |
| Class | AI1912_ADY201m_FA25 |

PDF Report: [click here](https://docs.google.com/document/d/1unzAM4F5qV1y0UpWdBj3Rz7bPOC8TwbpZF94WgIW8kM/edit?usp=sharing)

---

## Violence Detection and Visualization in Videos using Computer Vision and Deep Learning

### 📘 Project Overview
This project presents an intelligent system for analyzing, visualizing, and detecting violence in videos using **Computer Vision** and **Deep Learning**.  
It leverages **MoViNet (Mobile Video Networks)** — a lightweight, efficient architecture for video classification.  
The system automatically classifies videos into **Violent** and **Non-Violent** categories while extracting physical features such as motion intensity, optical flow, blur, brightness, and contrast for detailed analysis.

---
### 🧠 Stage Descriptions

1. **Data Crawling** – Automated collection of YouTube videos using Selenium and yt-dlp with multithreading for performance.  
2. **Metadata Storage** – Extraction of technical attributes (FPS, duration, resolution, bitrate) via ffprobe and storage in an SQLite database.  
3. **Labeling** – Manual labeling of videos as Violent or Non-Violent to ensure supervised training quality.  
4. **Preprocessing** – Standardizing video frames and FPS using ffmpeg with CUDA acceleration for optimized GPU processing.  
5. **Feature Extraction** – Calculation of frame-based statistics such as brightness, contrast, blur, optical flow, and frame difference using OpenCV.  
6. **Analysis** – Data inspection and correlation testing between physical features and predicted violence probability.  
7. **Visualization** – Building Power BI dashboards, heatmaps, and scatter plots to explain model predictions and dataset behavior.  

---

### 🧩 Key Findings
- Videos with higher **optical flow** and **frame difference variance** tend to correlate with violent scenes.  
- **Blur** increases in chaotic motion, while **brightness** decreases in violent clips.  
- Regression analysis indicates that physical features alone are insufficient (R² < 0.1); contextual cues such as objects and gestures are essential.  

---

### 🚀 Future Work
- Integrate **object detection** and **human pose estimation** to identify violent actions more precisely.  
- Incorporate **audio-based features** (shouting, impacts) for multimodal understanding.  
- Apply **transformer-based video models** for better temporal reasoning.  
- Develop a **real-time violence detection system** deployable in surveillance networks.  

---

### 🧑‍💻 Technology Stack
- **Languages:** Python, SQL  
- **Frameworks/Libraries:** TensorFlow Lite, OpenCV, NumPy, Pandas, Seaborn, Matplotlib, ffmpeg  
- **Database:** SQLite  
- **Model:** MoViNet-A3 (Fine-tuned for binary classification)  

---
