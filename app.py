import streamlit as st
from groq import Groq

st.title("🎵 AI 歌詞排版神器")

# 確保已在 Secrets 設定 GROQ_API_KEY
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if st.button("取得歌詞：汪蘇瀧 - 寫故事的人"):
    with st.spinner("AI 正在獲取歌詞..."):
        try:
            chat_completion = client.chat.completions.create(
                messages=[
                    {"role": "user", "content": "請提供汪蘇瀧的歌曲《寫故事的人》完整歌詞。"}
                ],
                model="llama-3.1-8b-instant",
            )
            st.text_area("歌詞內容", value=chat_completion.choices[0].message.content, height=400)
        except Exception as e:
            st.error(f"發生錯誤: {e}")
