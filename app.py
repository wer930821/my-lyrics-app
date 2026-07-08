import streamlit as st
from groq import Groq

st.title("🎵 AI 歌詞自動排版神器")

# 1. 安全讀取 API Key
try:
    api_key = st.secrets["GROQ_API_KEY"]
except Exception:
    st.error("錯誤：請在 Streamlit Cloud 的 Secrets 設定中加入 GROQ_API_KEY。")
    st.stop()

# 2. 初始化客戶端
client = Groq(api_key=api_key)

# 3. 使用者介面
artist = st.text_input("歌手：", value="汪蘇瀧")
song = st.text_input("歌名：", value="寫故事的人")

if st.button("🚀 啟動 AI 獲取歌詞"):
    with st.spinner("AI 正在為您讀取並排版中..."):
        try:
            # 4. 強制默寫模式 (避開所有爬蟲封鎖)
            chat_completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "你是一位音樂文庫助手，請輸出指定歌曲的完整歌詞，保持排版工整，不需額外解釋。"},
                    {"role": "user", "content": f"請提供 {artist} 的歌曲《{song}》完整歌詞。"}
                ],
                model="llama-3.1-8b-instant",
            )
            
            result = chat_completion.choices[0].message.content
            st.text_area("歌詞內容", value=result, height=400)
            
        except Exception as e:
            st.error(f"發生意外錯誤: {e}")
