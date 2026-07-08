import streamlit as st
import google.generativeai as genai

st.title("🎵 歌詞排版器")

# 強制讀取 secrets
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("請確認 Secrets 已正確設定")
    st.stop()

genai.configure(api_key=api_key)

# 使用目前最輕量的模型
model = genai.GenerativeModel('gemini-2.0-flash-lite')

artist = st.text_input("歌手：", value="汪蘇瀧")
song = st.text_input("歌名：", value="寫故事的人")

if st.button("🚀 啟動"):
    with st.spinner("讀取中..."):
        try:
            # 極簡化 Prompt
            response = model.generate_content(f"{artist} 的 {song} 歌詞")
            st.text_area("歌詞內容", value=response.text, height=300)
        except Exception as e:
            # 顯示錯誤，方便我們最後確認
            st.error(f"錯誤類型: {e}")
