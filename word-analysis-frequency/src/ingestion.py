import json
import os

def extract_ai_papers(input_path: str, output_path: str):
    """
    Hàm đọc file JSON khổng lồ và trích xuất các bài báo AI/ML
    được tối ưu hóa đặc biệt cho máy tính có RAM/CPU giới hạn.
    """
    # 5 category mục tiêu của dự án
    target_categories = {'cs.AI', 'cs.LG', 'cs.CL', 'cs.CV', 'stat.ML'}
    
    print("🚀 Khởi động Pipeline Ingestion...")
    print(f"📥 Nguồn: {input_path}")
    print(f"📤 Đích: {output_path}\n")

    count = 0
    
    # Mở song song 2 file: 1 để đọc (read), 1 để ghi (write)
    # encoding='utf-8' rất quan trọng trên máy Mac để không bị lỗi font
    with open(input_path, 'r', encoding='utf-8') as infile, \
         open(output_path, 'w', encoding='utf-8') as outfile:
        
        for line in infile:
            # TỐI ƯU HÓA CPU: Lọc thô siêu tốc
            # Kiểm tra xem dòng chữ này có chứa bất kỳ category mục tiêu nào không.
            # Nếu không có, bỏ qua luôn lệnh json.loads() nặng nề bên dưới.
            if not any(cat in line for cat in target_categories):
                continue
            
            # Nếu vượt qua bộ lọc thô, lúc này mới bắt đầu phân tích JSON
            try:
                paper = json.loads(line)
            except json.JSONDecodeError:
                continue # Bỏ qua nếu dòng JSON bị lỗi cấu trúc
                
            paper_cats = set(paper.get('categories', '').split())
            
            # Kiểm tra chéo lại một lần nữa cho chính xác tuyệt đối
            if target_categories.intersection(paper_cats):
                
                # Cắt tỉa dữ liệu: Chỉ lấy đúng 4 trường cần thiết, bỏ hết tên tác giả, link...
                clean_paper = {
                    'id': paper.get('id', ''),
                    'year': paper.get('update_date', '0000')[:4], # Lấy 4 ký tự đầu (năm)
                    'categories': paper.get('categories', ''),
                    'abstract': paper.get('abstract', '')
                }
                
                # TỐI ƯU HÓA RAM: Ghi thẳng kết quả xuống file ngay lập tức
                outfile.write(json.dumps(clean_paper) + '\n')
                count += 1
                
                # In thông báo mỗi khi xử lý xong 5000 bài để bạn biết máy chưa bị treo
                if count % 5000 == 0:
                    print(f"⏳ Đang xử lý... Đã thu thập được {count} bài báo học thuật.")

    print(f"\n✅ HOÀN TẤT! Đã ép từ file 3.5GB xuống thành công {count} bài báo AI/ML.")
    print(f"📁 Dữ liệu sạch đã sẵn sàng tại: {output_path}")

# --- KHỐI LỆNH CHẠY TRỰC TIẾP ---
if __name__ == "__main__":
    # Khai báo đường dẫn tương đối (đảm bảo bạn đang đứng ở thư mục gốc của dự án)
    FILE_GOC = "data/raw/arxiv-metadata-oai-snapshot.json"
    FILE_KET_QUA = "data/processed/ai_papers_filtered.json"
    
    # Đảm bảo thư mục đầu ra tồn tại trước khi chạy
    os.makedirs("data/processed", exist_ok=True)
    
    # Kích hoạt hệ thống
    extract_ai_papers(FILE_GOC, FILE_KET_QUA)