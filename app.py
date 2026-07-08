import streamlit as st
import requests
import os

# 1. 優先嘗試從 st.secrets 讀取，沒有則從環境變數讀取
api_key = st.secrets.get("GEMINI_API_KEY", os.getenv("GEMINI_API_KEY", ""))

st.title("🎵 AI 歌詞完美排版神器")

if not api_key:
    st.error("系統偵測不到 API Key！請檢查 Streamlit Secrets 設定。")
    st.stop()

# 2. 直接硬編碼路徑，確保不因變數拼寫錯誤導致 404
API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

artist = st.text_input("請輸入歌手：", value="汪蘇瀧")
song = st.text_input("請輸入歌名：", value="寫故事的人")

if st.button("🚀 啟動排版"):
    with st.spinner("連線中..."):
        headers = {"Content-Type": "application/json"}
        payload = {
            "contents": [{"parts": [{"text": f"請提供歌手「{artist}」的歌曲「{song}」歌詞。只需歌詞，一句一行，不要任何贅述。"}]}]
        }
        
        # 3. 把 Key 放在 Params 參數中，而不是 URL 裡，這樣更乾淨
        params = {"key": api_key}
        
        try:
            response = requests.post(API_URL, headers=headers, json=payload, params=params, timeout=30)
            
            if response.status_code == 200:
                result = response.json()['candidates'][0]['content']['parts'][0]['text']
                st.text_area("排版結果", value=result, height=400)
            else:
                st.error(f"連線失敗 (錯誤碼: {response.status_code})")
                st.write("回應內容:", response.text) # 把錯誤訊息印出來幫你除錯
        except Exception as e:
            st.error(f"程式崩潰: {e}")
