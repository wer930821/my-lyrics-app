import streamlit as st
import google.generativeai as genai

st.title("🎵 AI 歌詞排版神器")

# 讀取 API Key
api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.error("請在 Streamlit Secrets 設定中填入 GEMINI_API_KEY")
    st.stop()

genai.configure(api_key=api_key)

# 改用你清單中明確存在的模型名稱
# 這裡嘗試使用 gemini-2.0-flash，這是目前許多帳號的首選
model = genai.GenerativeModel('models/gemini-2.0-flash')

artist = st.text_input("歌手：", value="汪蘇瀧")
song = st.text_input("歌名：", value="寫故事的人")

if st.button("🚀 啟動排版"):
    with st.spinner("AI 正在處理中..."):
        try:
            # 簡化 Prompt
            prompt = f"請提供 {artist} 的歌曲《{song}》完整歌詞，並以純文字呈現。"
            response = model.generate_content(prompt)
            st.text_area("排版結果", value=response.text, height=400)
        except Exception as e:
            st.error(f"執行錯誤: {e}")
