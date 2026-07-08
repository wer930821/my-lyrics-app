import streamlit as st
import google.generativeai as genai

st.title("🎵 AI 歌詞完美排版神器")

# 讀取 Secrets 中的 Key
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("請確認已在 Streamlit Secrets 設定中填入 GEMINI_API_KEY")
    st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.0-flash')

artist = st.text_input("請輸入歌手：", value="汪蘇瀧")
song = st.text_input("請輸入歌名：", value="寫故事的人")

if st.button("🚀 啟動排版"):
    with st.spinner("AI 正在處理中..."):
        try:
            prompt = f"請提供歌手「{artist}」的歌曲《{song}》歌詞，以純文字格式呈現。"
            response = model.generate_content(prompt)
            st.text_area("排版結果", value=response.text, height=400)
        except Exception as e:
            if "429" in str(e):
                st.error("額度已達上限，請稍後再試或使用新的 API Key。")
            else:
                st.error(f"執行錯誤: {e}")
