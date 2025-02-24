import google.generativeai as genai
import streamlit as st
import os
from serpapi import GoogleSearch

# ====== Đọc API key từ file hoặc biến môi trường ======
def get_api_key():
    try:
        with open("apikey.txt", "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            st.error("Không tìm thấy Gemini API key. Hãy đặt API key trong file `apikey.txt` hoặc biến môi trường `GEMINI_API_KEY`.")
            st.stop()
        return api_key

# Cấu hình Gemini API Key
GEMINI_API_KEY = get_api_key()
genai.configure(api_key=GEMINI_API_KEY)

SERPAPI_KEY = os.getenv("SERPAPI_KEY", "your-serpapi-key")  # Thay bằng API key của bạn

# ====== Tìm kiếm thông tin từ Google bằng SerpAPI ======
def search_web(query):
    st.write("🔎 Đang tìm kiếm thông tin trên Internet...")
    params = {
        "q": query,
        "hl": "vi",  # Ngôn ngữ tiếng Việt
        "gl": "vn",  # Vị trí Việt Nam
        "api_key": SERPAPI_KEY
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    
    if "organic_results" in results:
        snippets = [result["snippet"] for result in results["organic_results"][:5]]  # Lấy 5 kết quả đầu tiên
        return "\n".join(snippets)
    
    return "Không tìm thấy thông tin phù hợp."

# ====== Tạo bài viết chuyên sâu với Gemini ======
def generate_article(title, context):
    prompt = f"""Dựa trên thông tin tham khảo dưới đây, hãy viết một bài viết chuyên sâu khoảng 1200 từ về chủ đề: "{title}".

Thông tin tham khảo từ web:
{context}

Yêu cầu bài viết:
- **Mở bài**: Giới thiệu chủ đề, bối cảnh.
- **Thân bài**:
  - Giải thích chi tiết về chủ đề.
  - Phân tích sâu bằng cách chia nhỏ thành các phần.
  - Đưa ra ví dụ thực tế hoặc số liệu (nếu có).
- **Kết bài**: Tóm tắt lại nội dung, nêu quan điểm hoặc hướng phát triển.

Hãy viết bài một cách logic, có cấu trúc rõ ràng và dễ hiểu.
"""
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)
    return response.text  # Trả về nội dung bài viết

# ====== Giao diện ứng dụng Streamlit ======
def main():
    st.title("📝 Tạo bài viết chuyên sâu tự động với Gemini")
    title = st.text_input("Nhập tiêu đề bài viết:")

    if st.button("Tạo bài viết") and title:
        # Tìm kiếm thông tin từ web
        context = search_web(title)
        
        # Hiển thị thông tin tìm được
        st.subheader("🔍 Thông tin tìm được từ Internet:")
        st.text_area("Thông tin từ web:", context, height=200)

        # Bắt đầu tạo bài viết
        st.write("✍️ **Đang tạo bài viết...**")
        article_text = generate_article(title, context)

        # Hiển thị bài viết hoàn chỉnh
        st.subheader("📄 Bài viết hoàn chỉnh:")
        st.text_area("Bài viết:", article_text, height=400)

if __name__ == "__main__":
    main()
    