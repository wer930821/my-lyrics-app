import streamlit as st
import requests

# 讀取雲端安全金鑰
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]

# 使用正確的 Gemini 1.5-flash API 路徑
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"

st.title("🎵 AI 歌詞完美排版神器")

artist = st.text_input("請輸入歌手名稱：")
song_name = st.text_input("請輸入歌曲名稱：")

if st.button("🚀 啟動排版"):
    if not artist or not song_name:
        st.warning("請輸入歌手與歌名！")
    else:
        with st.spinner("AI 正在處理中..."):
            prompt = f"請搜尋歌手「{artist}」的歌曲《{song_name}》並輸出完整歌詞。要求：一句一行，刪除所有時間軸、製作名單與廢話。"
            payload = {"contents": [{"parts": [{"text": prompt}]}]}
            
            try:
                response = requests.post(API_URL, json=payload)
                if response.status_code == 200:
                    data = response.json()
                    lyrics = data['candidates'][0]['content']['parts'][0]['text']
                    st.text_area("排版結果", value=lyrics, height=400)
                else:
                    st.error(f"連線失敗 (錯誤碼: {response.status_code})")
            except Exception as e:
                st.error(f"發生錯誤: {e}")
