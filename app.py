import streamlit as st
import google.generativeai as genai

# 網頁設定
st.set_page_config(page_title="AI 歌詞排版神器", page_icon="🎵")
st.title("🎵 AI 歌詞完美排版神器")

# 從 Streamlit Cloud 的 Secrets 讀取 API Key
# 請務必確認你在 Streamlit 專案設定的 Secrets 中填入了 GEMINI_API_KEY
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("系統偵測不到 API Key！請確認已在 Streamlit 的 Secrets 設定中填入 GEMINI_API_KEY")
    st.stop()

# 使用官方 SDK 初始化，自動處理路徑問題
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

# 輸入介面
artist = st.text_input("請輸入歌手名稱：", value="汪蘇瀧")
song_name = st.text_input("請輸入歌曲名稱：", value="寫故事的人")

if st.button("🚀 啟動排版"):
    if not artist or not song_name:
        st.warning("請填寫歌手與歌名")
    else:
        with st.spinner("AI 正在為你排版中..."):
            try:
                prompt = f"搜尋並輸出歌手「{artist}」的歌曲《{song_name}》完整歌詞。排版要求：一句一行，刪除所有幕後名單、時間戳與廢話。"
                response = model.generate_content(prompt)
                st.text_area("排版結果（長按可複製）", value=response.text, height=400)
            except Exception as e:
                st.error(f"連線錯誤: {e}")
