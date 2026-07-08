import streamlit as st
import requests

# 網頁配置
st.set_page_config(page_title="AI 歌詞排版神器", page_icon="🎵")
st.title("🎵 AI 歌詞完美排版神器")

# 你的 API Key
GEMINI_API_KEY = "AQ.Ab8RN6K-aJqr65fm5-roROhDkcmku_IYZt10BmBdQruuQSuuWQ"

# 輸入區
artist = st.text_input("請輸入歌手名稱：", value="汪蘇瀧")
song_name = st.text_input("請輸入歌曲名稱：", value="寫故事的人")

def ai_search_and_format(artist_name, song):
    # 使用 1.5-flash 模型
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    headers = {"Content-Type": "application/json"}
    
    # 指令
    prompt_text = f"請搜尋並輸出歌手「{artist_name}」的歌曲《{song}》完整歌詞。排版要求：1.一句一行 2.刪除所有幕後名單、時間戳與廢話。"
    
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
        st.text_area("排版結果", value=result, height=400)
