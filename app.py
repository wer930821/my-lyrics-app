import streamlit as st
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

st.title("🎵 全自動歌詞快速獲取器")

artist = st.text_input("歌手：", value="汪蘇瀧")
song = st.text_input("歌名：", value="寫故事的人")

# 使用 Streamlit 的表單（Form）機制，確保按鈕送出時 100% 觸發，不漏接
with st.form(key="lyrics_form"):
    submit_button = st.form_submit_button(label="🚀 開始全自動無痕搜尋")

if submit_button:
    # 建立一個狀態提示框
    status_text = st.empty()
    status_text.info("⏳ 正在啟動後端引擎...")
    
    encoded_artist = quote(artist)
    encoded_track = quote(song)
    
    # 方案 A：直接測試 lrclib API (設定超時 5 秒，防止卡死沒反應)
    try:
        status_text.info("🔍 正在檢索公共音樂節點...")
        lrclib_url = f"https://lrclib.net/api/search?artist={encoded_artist}&track={encoded_track}"
        res = requests.get(lrclib_url, timeout=5)
        
        if res.status_code == 200 and res.json():
            track_data = res.json()[0]
            lyrics = track_data.get("plainLyrics") or track_data.get("syncedLyrics")
            if lyrics:
                status_text.success("✨ 成功找到完整歌詞！")
                st.text_area("歌詞結果", value=lyrics, height=400)
                st.stop()
    except Exception:
        pass # 如果方案 A 超時或出錯，直接安靜地跳到方案 B

    # 方案 B：使用 DuckDuckGo 快取潔淨文字流 (設定超時 5 秒)
    try:
        status_text.info("🌐 公共節點未命中，正在全網搜刮文字快取...")
        search_url = f"https://html.duckduckgo.com/html/?q={encoded_artist}+{encoded_track}+%E6%AD%8C%E8%A9%9E"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        
        search_res = requests.get(search_url, headers=headers, timeout=5)
        if search_res.status_code == 200:
            soup = BeautifulSoup(search_res.text, "html.parser")
            snippets = soup.find_all("a", class_="result__snippet")
            
            if snippets:
                status_text.success("✨ 成功搜刮到歌詞主體片段！")
                combined_lyrics = ""
                for snip in snippets[:3]:
                    combined_lyrics += f"{snip.get_text().strip()}\n"
                
                cleaned_lyrics = combined_lyrics.replace("...", "\n")
                st.text_area("歌詞快取結果", value=cleaned_lyrics, height=400)
                st.stop()
        
        status_text.error("❌ 全網搜尋結束：該歌曲受到版權防火牆高強度保護，自動化程式遭封鎖。")
        
    except Exception as e:
        status_text.error(f"💥 運行時發生錯誤: {e}")
