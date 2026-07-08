import streamlit as st
from groq import Groq

st.title("🎵 AI 歌詞排版神器 (Groq版)")

# 讀取 Secrets 中的 API Key
api_key = st.secrets.get("GROQ_API_KEY")
if not api_key:
    st.error("請在 Streamlit Secrets 設定中填入 GROQ_API_KEY")
    st.stop()

client = Groq(api_key=api_key)

artist = st.text_input("歌手：", value="汪蘇瀧")
song = st.text_input("歌名：", value="寫故事的人")

if st.button("🚀 啟動排版"):
    with st.spinner("AI 正在快速生成中..."):
        try:
            # 呼叫 Groq API
            chat_completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "你是一個專業的歌詞整理助手，請提供完整歌詞，只需輸出歌詞內容。"},
                    {"role": "user", "content": f"請提供 {artist} 的歌曲《{song}》完整歌詞。"}
                ],
                model="llama-3.1-8b-instant",
            )
            
            result = chat_completion.choices[0].message.content
            st.text_area("排版結果", value=result, height=400)
            
        except Exception as e:
            st.error(f"執行錯誤: {e}")
