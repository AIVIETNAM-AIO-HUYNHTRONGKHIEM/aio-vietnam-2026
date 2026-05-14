import json
import re
from collections import Counter
import os
import nltk
from nltk.corpus import stopwords

# Tự động tải bộ từ điển stop-words của NLTK (chỉ tải lần đầu tiên)
nltk.download('stopwords', quiet=True)

def get_professional_stopwords():
    """
    Kết hợp từ điển chuẩn quốc tế và bộ lọc chuyên ngành học thuật
    """
    # Lấy ~179 từ dừng tiếng Anh cơ bản từ NLTK
    base_stops = set(stopwords.words('english'))
    
    # Bổ sung các từ vô nghĩa thường gặp trong bài báo khoa học
    academic_stops = {
        "paper", "propose", "show", "method", "results", "model", "using",
        "approach", "two", "one", "new", "state", "art", "performance",
        "also", "however", "showed", "used", "based", "proposed", "can",
        "may", "different", "well", "work", "study", "data", "set", "problem",
        "algorithm", "algorithms", "models", "methods", "task", "tasks", "framework"
    }
    
    # Gộp 2 tập hợp lại thành một lưới lọc siêu mạnh
    return base_stops.union(academic_stops)

def clean_text(text: str, stop_words: set) -> list:
    """Phiên bản 'Máy giặt' đã được nâng cấp"""
    text = re.sub(r'\$.*?\$', ' ', text) # Xóa công thức
    text = re.sub(r'[^a-z]', ' ', text.lower()) # Xóa dấu câu, số
    return [w for w in text.split() if w not in stop_words and len(w) > 2]

def run_frequency_engine(input_file: str, output_file: str):
    """
    Trái tim của Pipeline: Đọc dữ liệu, đếm tần suất và nhóm theo năm.
    """
    print("⚙️ Khởi động Lõi Phân tích Tần suất (Frequency Engine)...")
    
    stop_words = get_professional_stopwords()
    
    # Dictionary chứa kết quả: { "2024": Counter({'ai': 500, 'learning': 450}), "2025": ... }
    yearly_trends = {}
    
    count = 0
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            paper = json.loads(line)
            year = paper.get('year', 'Unknown')
            abstract = paper.get('abstract', '')
            
            # 1. Gọi máy giặt
            clean_words = clean_text(abstract, stop_words)
            
            # 2. Phân loại theo năm và Đếm
            if year not in yearly_trends:
                yearly_trends[year] = Counter()
                
            yearly_trends[year].update(clean_words)
            
            count += 1
            if count % 2000 == 0:
                print(f"🔄 Đã phân tích {count} bài báo...")

    print("\n✅ Phân tích hoàn tất! Đang trích xuất Top 50 từ khóa mỗi năm...")
    
    # 3. Đóng gói kết quả: Chỉ lấy Top 50 từ hot nhất của mỗi năm để file nhẹ
    final_report = {}
    for year, word_counter in sorted(yearly_trends.items()):
        # most_common(50) trả về dạng list [(word, count), ...], chuyển sang dict cho dễ đọc
        final_report[year] = dict(word_counter.most_common(50))
        
    # LƯU KẾT QUẢ XUỐNG Ổ CỨNG
    with open(output_file, 'w', encoding='utf-8') as f:
        # indent=4 giúp file JSON được định dạng đẹp, con người dễ đọc
        json.dump(final_report, f, indent=4)
        
    print(f"🎉 Thành công! Báo cáo xu hướng đã được lưu tại: {output_file}")

# --- KHỐI LỆNH CHẠY TRỰC TIẾP ---
if __name__ == "__main__":
    # Đọc file đã lọc ở Ngày 1
    FILE_INPUT = "data/processed/ai_papers_filtered.json" 
    
    # Xuất ra file Báo cáo cuối cùng
    FILE_OUTPUT = "data/processed/yearly_trends.json"
    
    # Nếu file input chưa có (bạn chưa chạy bước Ingestion), báo lỗi ngay
    if not os.path.exists(FILE_INPUT):
        print(f"❌ LỖI: Không tìm thấy file {FILE_INPUT}. Hãy chạy 'python src/ingestion.py' trước!")
    else:
        run_frequency_engine(FILE_INPUT, FILE_OUTPUT)
