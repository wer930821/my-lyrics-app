import streamlit as st
import google.generativeai as genai

st.title("🎵 AI 歌詞完美排版神器")

# 讀取 Key
api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.error("請在 Streamlit Secrets 設定中填入 GEMINI_API_KEY")
    st.stop()

# 強制設定 API Key
genai.configure(api_key=api_key)

# 使用 gemini-1.5-flash (這是標準名稱)
model = genai.GenerativeModel('gemini-1.5-flash')

artist = st.text_input("請輸入歌手名稱：", value="汪蘇瀧")
song_name = st.text_input("請輸入歌曲名稱：", value="寫故事的人")

if st.button("🚀 啟動排版"):
    with st.spinner("AI 正在處理中..."):
        try:
            # 簡化請求，排除一切變數
            response = model.generate_content(f"請提供「{artist}」的歌曲《{song_name}》歌詞。只要歌詞，一句一行。")
            st.text_area("排版結果", value=response.text, height=400)
        except Exception as e:
            st.error(f"連線錯誤: {e}")
