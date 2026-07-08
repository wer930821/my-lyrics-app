import streamlit as st
import requests

st.title("🎵 AI 歌詞快速檢索")

artist = st.text_input("歌手：", value="汪蘇瀧")
song = st.text_input("歌名：", value="寫故事的人")

if st.button("🚀 獲取歌詞"):
    with st.spinner("正在連線至歌詞庫..."):
        # 使用 Lyrics.ovh，這個 API 不需要 Token，也不會被 Cloudflare 擋住
        url = f"https://api.lyrics.ovh/v1/{artist}/{song}"
        
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                lyrics = data.get('lyrics', '找不到歌詞內容')
                st.text_area("歌詞結果", value=lyrics, height=400)
            elif response.status_code == 404:
                st.error("找不到該歌曲，請嘗試檢查歌名或歌手拼字。")
            else:
                st.error(f"連線失敗，狀態碼: {response.status_code}")
        except Exception as e:
            st.error(f"發生錯誤: {e}")
