import streamlit as st
import google.generativeai as genai

# 標題
st.title("🎵 AI 歌詞完美排版神器")

# 從 Secrets 讀取 API Key (請確保已在 Streamlit Cloud 設定好)
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("請在 Streamlit Secrets 設定中填入 GEMINI_API_KEY")
    st.stop()

# 初始化 SDK
genai.configure(api_key=api_key)

# 關鍵修正：確保 model 的定義正確且不帶過多路徑參數
model = genai.GenerativeModel('gemini-1.5-flash')

artist = st.text_input("請輸入歌手：", value="汪蘇瀧")
song = st.text_input("請輸入歌名：", value="寫故事的人")

if st.button("🚀 啟動排版"):
    with st.spinner("AI 正在處理中..."):
        try:
            # 發送請求
            prompt = f"請提供歌手「{artist}」的歌曲《{song}》完整歌詞。排版要求：一句一行，刪除所有幕後名單、時間戳與廢話。"
            response = model.generate_content(prompt)
            
            # 顯示結果
            st.text_area("排版結果", value=response.text, height=400)
        except Exception as e:
            st.error(f"連線錯誤: {e}")
