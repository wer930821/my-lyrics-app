import streamlit as st
import google.generativeai as genai

st.title("🎵 AI 歌詞完美排版神器")

api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.error("請在 Streamlit Secrets 設定中填入 GEMINI_API_KEY")
    st.stop()

genai.configure(api_key=api_key)

# 直接使用你清單中明確存在的模型名稱
model = genai.GenerativeModel('gemini-3.5-flash')

artist = st.text_input("請輸入歌手名稱：", value="汪蘇瀧")
song_name = st.text_input("請輸入歌曲名稱：", value="寫故事的人")

if st.button("🚀 啟動排版"):
    with st.spinner("AI 正在處理中..."):
        try:
            prompt = f"請提供歌手「{artist}」的歌曲《{song_name}》完整歌詞。排版要求：一句一行，刪除所有幕後名單、時間戳與廢話。"
            response = model.generate_content(prompt)
            st.text_area("排版結果", value=response.text, height=400)
        except Exception as e:
            st.error(f"執行錯誤: {e}")
