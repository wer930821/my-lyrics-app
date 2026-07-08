import streamlit as st
import google.generativeai as genai
import os

st.title("🎵 AI 歌詞排版器")

# 強制將 API 版本設定為 v1，這是最穩定的路徑
os.environ["GOOGLE_API_VERSION"] = "v1"

api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.error("請設定 API Key")
    st.stop()

genai.configure(api_key=api_key)

# 使用 gemini-2.0-flash，這是目前穩定性極高的選擇
model = genai.GenerativeModel('gemini-2.0-flash')

artist = st.text_input("歌手：", value="汪蘇瀧")
song = st.text_input("歌名：", value="寫故事的人")

if st.button("🚀 啟動"):
    with st.spinner("獲取中..."):
        try:
            # 簡化指令，避免 AI 產生拒絕回應
            prompt = f"請提供 {artist} 歌曲《{song}》的歌詞，以純文字格式呈現。"
            response = model.generate_content(prompt)
            st.text_area("結果", value=response.text, height=400)
        except Exception as e:
            st.error(f"錯誤: {e}")
