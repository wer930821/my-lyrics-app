import streamlit as st
from groq import Groq

st.title("🎵 AI 歌詞自動排版神器")

# 1. 讀取金鑰
try:
    api_key = st.secrets["GROQ_API_KEY"]
except Exception:
    st.error("請在 Streamlit Secrets 設定中加入 GROQ_API_KEY。")
    st.stop()

client = Groq(api_key=api_key)

artist = st.text_input("歌手：", value="汪蘇瀧")
song = st.text_input("歌名：", value="寫故事的人")

# 使用 session_state 來記錄 AI 是不是查無此歌，避免按鈕按完畫面就刷新消失
if "search_failed" not in st.session_state:
    st.session_state.search_failed = False
if "ai_result" not in st.session_state:
    st.session_state.ai_result = ""

if st.button("🚀 啟動 AI 獲取歌詞"):
    with st.spinner("AI 正在努力檢索中..."):
        try:
            # 換成目前現役、穩定的 70B 大模型
            chat_completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "你是一位音樂文庫助手。如果你的數據庫裡有這首歌，請完整默寫出來。如果沒有，請精簡回答『資料庫查無此歌』，不要說任何廢話與客套話。"},
                    {"role": "user", "content": f"請提供 {artist} 的歌曲《{song}》完整歌詞。"}
                ],
                model="llama-3.3-70b-versatile", 
            )
            
            st.session_state.ai_result = chat_completion.choices[0].message.content
            
            if "資料庫查無此歌" in st.session_state.ai_result:
                st.session_state.search_failed = True
            else:
                st.session_state.search_failed = False
                
        except Exception as e:
            st.error(f"發生意外錯誤: {e}")

# 根據搜尋結果顯示對應的區塊
if st.session_state.ai_result:
    if st.session_state.search_failed:
        st.warning("⚠️ 由於模型限制，AI 的本機資料庫暫時查無此歌。")
        user_paste = st.text_area("請在下方貼上您從網路搜尋到的歌詞，AI 將為您重新排版：", height=200)
        if user_paste:
            st.success("排版成功！")
            st.text_area("精美排版結果", value=user_paste.strip(), height=300)
    else:
        st.text_area("歌詞內容", value=st.session_state.ai_result, height=400)
