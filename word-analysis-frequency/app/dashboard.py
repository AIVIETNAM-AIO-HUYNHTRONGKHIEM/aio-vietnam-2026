import streamlit as st
import json 
import pandas as pd 
import matplotlib.pyplot as plt 
from wordcloud import WordCloud 
import os 

# 1. Cấu hình trang web cơ bản
st.set_page_config(page_title="ArXiv AI Trends", layout="wide")
st.title("📈 Bảng điều khiển Xu hướng Công nghệ AI (ArXiv)")
st.markdown("Dự án phân tích tần suất từ khóa từ các bài báo khoa học lĩnh vực AI/ML.")

# 2. Hàm đọc dữ liệu an toàn
@st.cache_data # Kỹ thuật cache giúp web không phải đọc lại file mỗi khi bạn bấm nút
def load_data():
    file_path = 'data/processed/yearly_trends.json'
    if not os.path.exists(file_path):
        return None
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

data = load_data()

# Nếu chưa có data, báo lỗi để người dùng biết
if not data:
    st.error("Không tìm thấy dữ liệu! Hãy đảm bảo bạn đã chạy xong src/frequency.py")
    st.stop()

# 3. Tạo thanh công cụ bên trái (Sidebar)
st.sidebar.header("Tùy chỉnh Báo cáo")
# Lấy danh sách các năm có trong file JSON và cho người dùng chọn
available_years = sorted(list(data.keys()), reverse=True)
selected_year = st.sidebar.selectbox("Chọn Năm cần xem:", available_years)

top_n = st.sidebar.slider("Hiển thị Top bao nhiêu từ?", min_value=10, max_value=50, value=20)

# Lấy dữ liệu của năm được chọn
year_data = data[selected_year]

# Chuyển Dictionary thành dạng Bảng (DataFrame) cho dễ xử lý
df = pd.DataFrame(list(year_data.items()), columns=['Từ khóa', 'Tần suất'])
df = df.sort_values(by='Tần suất', ascending=False).head(top_n)

# 4. Chia màn hình thành 2 cột (Cột Trái: Biểu đồ, Cột Phải: Bảng & Wordcloud)
col1, col2 = st.columns([6, 4])

with col1:
    st.subheader(f"📊 Top {top_n} từ khóa nổi bật năm {selected_year}")
    # Dùng biểu đồ cột ngang có sẵn của Streamlit
    st.bar_chart(df.set_index('Từ khóa'))

with col2:
    st.subheader("🔠 Đám mây từ khóa (Word Cloud)")
    
    # Tạo Word Cloud
    wordcloud = WordCloud(width=800, height=400, background_color='white', colormap='viridis').generate_from_frequencies(year_data)
    
    # Vẽ lên Streamlit bằng Matplotlib
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    st.pyplot(fig)
    
    # Hiển thị bảng số liệu chi tiết bên dưới
    st.subheader("📋 Bảng số liệu chi tiết")
    st.dataframe(df, use_container_width=True)