import re

def clean_arxiv_abstract(abstract_text: str) -> list:
    """
    Ham lam sach chuyen dung cho cac bai bao khoa hoc tren arXiv.
    """

    text_no_math = re.sub(r'\$.*?\$', ' ', abstract_text)

    text_lower = text_no_math.lower()

    text_letters_only = re.sub(r'[^a-z]', ' ', text_lower)

    words = text_letters_only.split()

    stop_words = {
        # Stop-words cơ bản
        "the", "a", "an", "and", "or", "in", "on", "at", "to", "for", "with", 
        "of", "by", "as", "is", "are", "was", "were", "be", "been", "that", 
        "this", "these", "those", "it", "its", "we", "our",
        
        # Stop-words chuyên ngành học thuật (không mang ý nghĩa xu hướng công nghệ)
        "paper", "propose", "show", "method", "results", "model", "using",
        "approach", "two", "one", "new", "state", "art", "performance"
    }

    final_words = [word for word in words if word not in stop_words and len(word) > 2]

    return final_words

# Chay thu nghiem truc tiep 
if __name__ == "__main__":
    # Một đoạn tóm tắt giả định chứa công thức và dấu câu phức tạp
    test_abstract = """
    In this paper, we propose a new Deep Learning method for Computer Vision! 
    It improves the state-of-the-art performance by 15.5%. 
    We optimize the equation $\alpha + \beta = \gamma$ and use a Neural Network.
    """
    
    print("Văn bản gốc:")
    print(test_abstract)
    print("-" * 30)
    print("Danh sách từ khóa sau khi qua 'Máy giặt':")
    ket_qua = clean_arxiv_abstract(test_abstract)
    print(ket_qua)