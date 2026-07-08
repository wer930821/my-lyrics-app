import streamlit as st
import requests

# 設定網頁標題
st.set_page_config(page_title="AI 歌詞排版神器", page_icon="🎵")
st.title("🎵 AI 歌詞完美排版神器")

# 從 Streamlit 雲端讀取 API Key (請確保在 Secrets 設定過)
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except:
    st.error("系統找不到 API Key，請至 Streamlit Secrets 設定中填入 GEMINI_API_KEY")
    st.stop()

# 使用正確的 Gemini 1.5-flash 路徑 (修正 404 錯誤)
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"

# 輸入區
artist = st.text_input("請輸入歌手名稱：", value="汪蘇瀧")
song_name = st.text_input("請輸入歌曲名稱：", value="寫故事的人")

def get_lyrics(artist_name, song):
    headers = {"Content-Type": "application/json"}
    prompt = f"搜尋並輸出歌手「{artist_name}」的歌曲《{song}》完整歌詞。排版要求：一句一行，刪除所有幕後名單、時間戳與前言廢話。"
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        if response.status_code == 200:
            return response.json()['candidates'][0]['content']['parts'][0]['text']
        else:
            return f"連線失敗 (錯誤碼: {response.status_code})"
    except Exception as e:
        return f"程式錯誤: {str(e)}"

# 執行按鈕
if st.button("🚀 啟動排版"):
    with st.spinner("AI 正在搜尋與排版中..."):
        result = get_lyrics(artist, song_name)
        st.text_area("排版結果（長按可全選複製）", value=result, height=400)
