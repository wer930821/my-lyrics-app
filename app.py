import streamlit as st
import google.generativeai as genai

st.title("🎵 AI 歌詞完美排版神器")

api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("請在 Streamlit Secrets 設定中填入 GEMINI_API_KEY")
    st.stop()

# 直接進行設定
genai.configure(api_key=api_key)

# 改用 'gemini-1.5-flash-002'，這是目前最穩定的版本名稱
model = genai.GenerativeModel('gemini-1.5-flash-002')

artist = st.text_input("請輸入歌手名稱：", value="汪蘇瀧")
song_name = st.text_input("請輸入歌曲名稱：", value="寫故事的人")

if st.button("🚀 啟動排版"):
    with st.spinner("AI 正在處理中..."):
        try:
            prompt = f"請搜尋歌手「{artist}」的歌曲《{song_name}》並輸出完整歌詞。要求：一句一行，刪除所有時間軸、製作名單與廢話。"
            response = model.generate_content(prompt)
            st.text_area("排版結果", value=response.text, height=400)
        except Exception as e:
            st.error(f"發生錯誤: {e}")
