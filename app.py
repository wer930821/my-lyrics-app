import streamlit as st
from groq import Groq

st.title("🎵 歌詞自動檢索 (進階模式)")

api_key = st.secrets.get("GROQ_API_KEY")
client = Groq(api_key=api_key)

artist = st.text_input("歌手：", "汪蘇瀧")
song = st.text_input("歌名：", "寫故事的人")

if st.button("🚀 強制搜尋與獲取"):
    with st.spinner("AI 正在深度搜索與編寫歌詞..."):
        try:
            # 這裡我們不使用搜尋，直接讓擁有強大知識庫的 Llama-3.1 默寫歌詞
            # 這能避開所有爬蟲封鎖與網站驗證
            chat_completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "你是一位音樂百科全書。請直接默寫指定歌曲的完整歌詞。"},
                    {"role": "user", "content": f"請提供 {artist} 的歌曲《{song}》完整歌詞，並以清晰的段落排版。"}
                ],
                model="llama-3.1-8b-instant",
            )
            
            result = chat_completion.choices[0].message.content
            st.text_area("歌詞內容", value=result, height=400)
            
        except Exception as e:
            st.error(f"發生錯誤: {e}")
