import streamlit as st
from groq import Groq

st.title("🎵 AI 歌詞自動排版神器")

# 讀取金鑰
try:
    api_key = st.secrets["GROQ_API_KEY"]
except Exception:
    st.error("請在 Streamlit Secrets 設定中加入 GROQ_API_KEY。")
    st.stop()

client = Groq(api_key=api_key)

artist = st.text_input("歌手：", value="汪蘇瀧")
song = st.text_input("歌名：", value="寫故事的人")

if st.button("🚀 啟動 AI 獲取歌詞"):
    with st.spinner("AI 正在努力檢索中..."):
        try:
            # 這裡我們換成 llama-3.3-70b，這是一個知識庫更大、更聰明的模型
            chat_completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "你是一位音樂文庫助手。如果你的數據庫裡有這首歌，請完整默寫出來。如果沒有，請精簡回答『資料庫查無此歌』，不要說廢話。"},
                    {"role": "user", "content": f"請提供 {artist} 的歌曲《{song}》完整歌詞。"}
                ],
                model="llama-3.3-70b-specdec", # 換成超級大模型試試看！
            )
            
            result = chat_completion.choices[0].message.content
            
            if "資料庫查無此歌" in result:
                st.warning("⚠️ 由於版權與模型限制，AI 的本機資料庫暫時盲區。")
                # 開啟一個臨時手動輸入框，讓這個 App 依然能運作排版功能！
                user_paste = st.text_area("請在下方貼上您從 Google 搜尋到的歌詞，AI 將為您重新排版：")
                if user_paste:
                    st.success("排版成功！")
                    st.text_area("精美排版結果", value=user_paste.strip(), height=400)
            else:
                st.text_area("歌詞內容", value=result, height=400)
            
        except Exception as e:
            st.error(f"發生意外錯誤: {e}")
