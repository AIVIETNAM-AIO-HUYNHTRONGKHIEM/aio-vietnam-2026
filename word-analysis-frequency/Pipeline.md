### **WORD ANALYSIS FREQUENCY PROJECT PIPELINE**

### **1\. Cấu trúc Kho mã nguồn (Repository Structure)**

Chúng ta sẽ thiết kế repo theo chuẩn chung của các dự án Data Science để dễ dàng bảo trì và mở rộng.

*arxiv-word-frequency/*  
*│*  
*├── data/                   \# (Lưu ý: Không push thư mục này lên Github)*  
*│   ├── raw/                \# Chứa file gốc: arxiv-metadata-oai-snapshot.json*  
*│   └── processed/          \# Chứa file kết quả: top\_words\_2026.csv, yearly\_trends.json*  
*│*  
*├── src/                    \# Chứa mã nguồn cốt lõi (Các module của Pipeline)*  
*│   ├── \_\_init\_\_.py*  
*│   ├── ingestion.py        \# Code đọc file JSON dung lượng lớn (Lazy Loading)*  
*│   ├── preprocessing.py    \# Code dọn dẹp văn bản (Regex, Stop-words)*  
*│   └── frequency.py        \# Code đếm từ khóa, N-grams, TF-IDF*  
*│*  
*├── api/                    \# Chứa code phục vụ ứng dụng ngoài*  
*│   └── main.py             \# FastAPI server trả dữ liệu đã xử lý*  
*│*  
*├── app/                    \# Chứa code giao diện Demo (Frontend)*  
*│   └── dashboard.py        \# Code Streamlit tạo biểu đồ trực quan*  
*│*  
*├── notebooks/              \# Dành cho việc thử nghiệm nhanh (Jupyter)*  
*│   └── 01\_eda\_test.ipynb   \# File nháp để test thử Regex hoặc vẽ bậy bạ*  
*│*  
*├── run\_pipeline.py         \# Script trung tâm để bấm nút chạy toàn bộ luồng từ A-Z*  
*├── requirements.txt        \# Danh sách thư viện cần cài đặt*  
*├── .gitignore              \# Chặn push data/ và các file rác lên Git*  
*└── README.md               \# Tài liệu hướng dẫn sử dụng repo*

### **2\. Thiết lập Môi trường (Environment Setup)**

Để tránh xung đột thư viện với các dự án khác trên máy bạn, chúng ta cần một môi trường ảo (Virtual Environment) hoặc AnaConda.

\- Bước 1: Tạo và kích hoạt môi trường ảo (trên Terminal/CMD)

*\# Tạo môi trường ảo tên là 'venv'*

*python \-m venv venv*

*\# Kích hoạt (Trên Windows)*

*venv\\Scripts\\activate*

*\# Kích hoạt (Trên macOS/Linux)*

*source venv/bin/activate*

\- Bước 2: Cài đặt thư viện (File requirements.txt)

Tạo file requirements.txt với nội dung sau:  
*pandas==2.2.0*  
*nltk==3.8.1*  
*fastapi==0.109.0*  
*uvicorn==0.27.0*  
*streamlit==1.31.0*  
*matplotlib==3.8.2*  
*wordcloud==1.9.3*

Chạy lệnh cài đặt:  
*pip install \-r requirements.txt*

### **3\. Các Giai đoạn của Pipeline (Pipeline Stages)**

Luồng chạy thực tế trong file run\_pipeline.py sẽ tuân thủ nghiêm ngặt 4 giai đoạn (ETL \- Extract, Transform, Load):

1. **Stage 1 \- Extract (Trích xuất):** Quét file JSON 3.5GB. Lọc bỏ mọi bài báo không thuộc cs.AI, cs.LG, cs.CL, cs.CV, stat.ML. Trả về một luồng (stream) các cụm văn bản (Abstract) \+ Năm xuất bản.  
2. **Stage 2 \- Transform (Biến đổi):** Bắn các Abstract này qua bộ lọc Regex toán học, xóa dấu câu, số và Stop-words chuyên ngành.  
3. **Stage 3 \- Aggregate (Tổng hợp):** Đẩy các từ sạch vào bộ đếm collections.Counter, gom nhóm theo từng năm (ví dụ: đếm riêng cho 2024, đếm riêng cho 2025).  
4. **Stage 4 \- Load (Lưu trữ):** Ghi đè kết quả đếm cuối cùng ra file tĩnh (như data/processed/yearly\_trends.json). **Pipeline kết thúc nhiệm vụ tại đây.**

### **4\. Công cụ chạy Pipeline (Orchestration Tools)**

**Giải pháp MVP (Giai đoạn đầu):** Chỉ cần dùng chính file run\_pipeline.py kết hợp với thư viện argparse có sẵn của Python:

* python run\_pipeline.py \--year 2025 (chỉ chạy data 2025).  
  * python run\_pipeline.py \--all (chạy toàn bộ).

**Giải pháp Scale-up (Khi dự án phình to):** Nếu sau này muốn code tự động chạy mỗi tháng 1 lần khi arXiv cập nhật data, đề xuất tích hợp **Apache Airflow** hoặc **Prefect** để lập lịch (Scheduling) và theo dõi lỗi (Monitoring) qua giao diện web.

### **5\. App/Demo Dự kiến**

Chúng ta sẽ dựng một **Dashboard tương tác bằng Streamlit** (đặt trong app/dashboard.py).

**Mô tả kịch bản Demo:**

* **Giao diện:** Một trang web đơn giản. Bên trái là Sidebar (Thanh công cụ). Bên phải là vùng hiển thị.  
* **Thao tác:** Người dùng chọn "Năm" (2018 \- 2026\) và "Category" (cs.AI, cs.CV...) từ menu thả xuống (Dropdown).  
* **Kết quả hiển thị (Real-time):**  
  1. Một bức ảnh "Đám mây từ khóa" (Word Cloud) siêu to khổng lồ hiện ra. Từ nào tần suất cao (ví dụ: "Deep Learning", "Transformer") sẽ to và nằm ở giữa.  
  2. Một biểu đồ cột ngang (Bar Chart) Top 20 từ khóa thịnh hành nhất của năm đó.  
  3. Một bảng số liệu (Data Table) chi tiết để người dùng có thể tải về file Excel nếu muốn.

*(Lưu ý: Ứng dụng Demo này sẽ chỉ đọc dữ liệu nhẹ từ thư mục data/processed/ chứ tuyệt đối không đụng vào file gốc 3.5GB).*

