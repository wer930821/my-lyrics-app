import streamlit as st
import google.generativeai as genai

# 設定網頁標題
st.title("🎵 AI 歌詞完美排版神器")

# 從 Secrets 讀取 API Key
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("請在 Streamlit Secrets 設定中填入 GEMINI_API_KEY")
    st.stop()

# 使用 Google 官方 SDK 初始化，這樣就不會再有 API URL 404 問題
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

artist = st.text_input("請輸入歌手：", value="汪蘇瀧")
song = st.text_input("請輸入歌名：", value="寫故事的人")

if st.button("🚀 啟動排版"):
    with st.spinner("AI 正在處理中..."):
        try:
            prompt = f"搜尋並輸出歌手「{artist}」的歌曲《{song}》完整歌詞。排版要求：一句一行，刪除所有幕後名單、時間戳與廢話。"
            response = model.generate_content(prompt)
            st.text_area("排版結果", value=response.text, height=400)
        except Exception as e:
            st.error(f"連線錯誤: {e}")
