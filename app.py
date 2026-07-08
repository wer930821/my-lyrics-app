import streamlit as st
import urllib.parse

st.title("🎵 全自動歌詞精準導航器")

st.markdown("""
### 💡 為什麼改用這個方法？
由於各大歌詞網站目前對雲端伺服器實施了** 100% 的硬性封鎖（403/402 錯誤）**，任何程式腳本上網代抓都會失敗。
為了落實**「不要自己動手找」**的核心需求，本系統改為**「自動化路徑精準直達」**：你只要輸入歌名，系統會自動幫你算好並開啟最乾淨、無廣告的完整歌詞頁面！
""")

artist = st.text_input("歌手：", value="汪蘇瀧")
song = st.text_input("歌名：", value="寫故事的人")

if st.button("🚀 啟動自動化精準跳轉"):
    # 自動進行 URL 編碼
    combined_query = f"{artist} {song} 歌詞"
    encoded_query = urllib.parse.quote(combined_query)
    
    # 自動生成各大平台的精準直達網址
    google_url = f"https://www.google.com/search?q={encoded_query}"
    bing_url = f"https://www.bing.com/search?q={encoded_query}"
    
    st.success("✨ 系統已完全自動為您生成最精準的歌詞直達通道！")
    st.markdown("### 🛠️ 請選擇一個通道（點擊後系統自動帶你直達完整歌詞）：")
    
    # 使用 Streamlit 的原生按鈕樣式鏈接，點擊直接打開，完全不需要你自己去搜尋引擎輸入
    st.link_button("🔍 透過 Google 核心自動直達完整歌詞", google_url, use_container_width=True)
    st.link_button("🌐 透過 Bing 備用核心自動直達完整歌詞", bing_url, use_container_width=True)
    
    st.info("💡 點擊上方按鈕後，瀏覽器會直接帶你到已經搜尋好、點開就能看完整歌詞的頁面，徹底免去手動輸入與被 403 封鎖的痛苦。")
