import streamlit as st
import requests

# 網頁配置
st.set_page_config(page_title="AI 歌詞排版神器", page_icon="🎵")
st.title("🎵 AI 歌詞完美排版神器")

# 從 Streamlit 雲端設定的 Secrets 讀取 API Key (請確保雲端已設定該 Key)
try:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
except:
    st.error("系統找不到 API Key，請至 Streamlit Secrets 設定中填入 GEMINI_API_KEY")
    st.stop()

# 輸入區
artist = st.text_input("請輸入歌手名稱：", value="汪蘇瀧")
song_name = st.text_input("請輸入歌曲名稱：", value="寫故事的人")

def ai_search_and_format(artist_name, song):
    # 使用 Gemini 1.5-flash 模型
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    headers = {"Content-Type": "application/json"}
    
    # 簡化 Prompt 確保穩定性
    prompt_text = f"搜尋並輸出歌手「{artist_name}」的歌曲《{song}》完整歌詞。排版要求：一句一行，刪除所有幕後名單、時間戳與前言廢話。若找不到請直接回：找不到歌詞"
    
    payload = {
        "contents": [{"parts": [{"text": prompt_text}]}]
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        if response.status_code == 200:
            return response.json()['candidates'][0]['content']['parts'][0]['text']
        else:
            return f"連線失敗 (錯誤碼: {response.status_code})"
    except Exception as e:
        return f"發生錯誤: {str(e)}"

# 按鈕與結果顯示
if st.button("🚀 啟動排版"):
    with st.spinner("AI 正在搜尋與排版中..."):
        result = ai_search_and_format(artist, song_name)
        st.text_area("排版結果（長按可全選複製）", value=result, height=400)
