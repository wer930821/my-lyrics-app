import streamlit as st
import requests

# 網頁配置
st.set_page_config(page_title="AI 歌詞排版神器", page_icon="🎵")
st.title("🎵 AI 歌詞完美排版神器")

# API Key
GEMINI_API_KEY = "AQ.Ab8RN6IyGKuv5spXFgcgH_U436HoMhmzpYlHItZ5SN-Mdk90Kg"

# 輸入區
artist = st.text_input("請輸入歌手名稱：", value="汪蘇瀧")
song_name = st.text_input("請輸入歌曲名稱：", value="寫故事的人")

def ai_search_and_format(artist_name, song):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent?key={GEMINI_API_KEY}"
    headers = {"Content-Type": "application/json"}
    prompt = f"搜尋並輸出歌手{artist_name}的歌曲{song}的完整歌詞。規則：1.只要歌詞 2.一句一行 3.刪除幕後名單與時間戳。"
    
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "tools": [{"googleSearch": {}}]
    }
    response = requests.post(url, headers=headers, json=payload, timeout=30)
    if response.status_code == 200:
        return response.json()['candidates'][0]['content']['parts'][0]['text']
    else:
        return "連線失敗"

if st.button("🚀 啟動排版"):
    with st.spinner("搜尋中..."):
        result = ai_search_and_format(artist, song_name)
        st.text_area("排版結果", value=result, height=400)
