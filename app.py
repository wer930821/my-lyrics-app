import streamlit as st
import requests
import os

# 設定 API Key 與網址
# 修正重點：使用 v1 版本路徑
api_key = st.secrets.get("GEMINI_API_KEY", "")
API_URL = "https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent"

st.title("🎵 AI 歌詞完美排版神器")

if not api_key:
    st.error("系統偵測不到 API Key！請至 Streamlit Secrets 設定。")
    st.stop()

artist = st.text_input("請輸入歌手：", value="汪蘇瀧")
song = st.text_input("請輸入歌名：", value="寫故事的人")

if st.button("🚀 啟動排版"):
    with st.spinner("正在呼叫 AI..."):
        headers = {"Content-Type": "application/json"}
        payload = {
            "contents": [{"parts": [{"text": f"請提供歌手「{artist}」的歌曲「{song}」歌詞。只需歌詞，一句一行，不要任何贅述。"}]}]
        }
        params = {"key": api_key}
        
        try:
            response = requests.post(API_URL, headers=headers, json=payload, params=params, timeout=30)
            
            if response.status_code == 200:
                result = response.json()['candidates'][0]['content']['parts'][0]['text']
                st.text_area("排版結果", value=result, height=400)
            else:
                st.error(f"連線失敗 (錯誤碼: {response.status_code})")
                st.code(response.text)
        except Exception as e:
            st.error(f"程式錯誤: {e}")
