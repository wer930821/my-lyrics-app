import streamlit as st
import requests
from urllib.parse import quote

st.title("🎵 真正全自動完整歌詞獲取器")

artist = st.text_input("歌手：", value="汪蘇瀧")
song = st.text_input("歌名：", value="寫故事的人")

if st.button("🚀 讓系統自己去網路搜尋完整歌詞"):
    with st.spinner("系統正在全網調取完整歌詞，請稍候..."):
        
        # 使用專門給開源音樂軟體用的公開無防禦 API（不會有 403 錯誤）
        # 這裡使用一個最常見的公開歌詞檢索節點
        encoded_artist = quote(artist)
        encoded_song = quote(song)
        
        # 第一備份渠道：Lyrics.ovh 公開數據庫
        url = f"https://api.lyrics.ovh/v1/{encoded_artist}/{encoded_song}"
        
        try:
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                lyrics = data.get("lyrics", "")
                
                if lyrics.strip():
                    st.success("✨ 系統已成功自動尋找到完整歌詞！")
                    st.text_area("完整歌詞內容", value=lyrics, height=500)
                    st.stop()
            
            # 第二備份渠道：如果上者無，改用開源音樂網路（不吃 Cloudflare 驗證的公共節點）
            st.info("第一渠道未命中，系統正自動切換至公共音樂節點搜尋...")
            
            search_api = f"https://lrclib.net/api/search?artist={encoded_artist}&track={encoded_song}"
            res = requests.get(search_api, timeout=10)
            
            if res.status_code == 200 and res.json():
                # 取得搜尋結果的第一筆歌曲資料
                track_data = res.json()[0]
                # 優先拿有時間軸或純文字的歌詞
                lyrics = track_data.get("syncedLyrics") or track_data.get("plainLyrics")
                
                if lyrics:
                    st.success("✨ 系統已透過公共音樂節點自動抓取到完整歌詞！")
                    st.text_area("完整歌詞內容", value=lyrics, height=500)
                else:
                    st.warning("系統自動找到了歌曲資料，但該歌曲在公共庫中尚未錄入歌詞文字。")
            else:
                st.error("系統自動全網搜尋失敗：各大歌詞網均對自動化程式進行了封鎖，且公共節點暫無此歌收錄。")
                
        except Exception as e:
            st.error(f"自動化程序發生錯誤: {e}")
