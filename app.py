import openai
import streamlit as st
import os

# Đọc API key từ file
def get_api_key():
    try:
        with open("apikey.txt", "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        return os.getenv("OPENAI_API_KEY", "your-api-key")

# Thiết lập API key
openai.api_key = get_api_key()

def generate_article(title):
    prompt = f"Viết một bài viết 1200 từ về chủ đề: {title}"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "Bạn là một nhà văn chuyên nghiệp."},
                  {"role": "user", "content": prompt}],
        max_tokens=1600,
        temperature=0.7,
        stream=True
    )
    return response

def main():
    st.title("Tạo bài viết tự động")
    title = st.text_input("Nhập tiêu đề bài viết:")
    if st.button("Tạo bài viết") and title:
        st.write("**Bài viết:**")
        response = generate_article(title)
        article_text = ""
        for chunk in response:
            if "choices" in chunk and chunk["choices"]:
                text_chunk = chunk["choices"][0]["delta"].get("content", "")
                article_text += text_chunk
                st.write(text_chunk, end="", flush=True)
        st.text_area("Bài viết hoàn chỉnh:", article_text, height=400)

if __name__ == "__main__":
    main()
