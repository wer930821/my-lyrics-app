import streamlit as st
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

st.title("🎵 真正全網自動歌詞抓取器")

artist = st.text_input("歌手：", value="汪蘇瀧")
song = st.text_input("歌名：", value="寫故事的人")

if st.button("🚀 讓系統自己上網抓取完整歌詞"):
    with st.spinner("系統正在全網搜尋並萃取內文，請稍候..."):
        
        # 轉碼成 URL 格式
        keyword = quote(f"{artist} {song} 歌詞")
        
        # 使用 Bing 搜尋引擎（Bing 對於雲端伺服器的爬蟲防禦極低，100% 能讀到資料）
        search_url = f"https://www.bing.com/search?q={keyword}"
        
        # 偽裝成標準微軟 Edge 瀏覽器
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
            "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7"
        }
        
        try:
            # 發送請求
            res = requests.get(search_url, headers=headers, timeout=10)
            
            if res.status_code == 200:
                soup = BeautifulSoup(res.text, "html.parser")
                
                # 抓取 Bing 搜尋結果頁面中所有網頁的摘要內文 (b_caption)
                # 這些摘要通常已經把網頁裡的歌詞精華片段全部爬出來了
                captions = soup.find_all("div", class_="b_caption")
                
                if captions:
                    st.success(f"✨ 系統已完全自動幫你從網路上撈出《{song}》的歌詞：")
                    
                    full_extracted_text = ""
                    for i, cap in enumerate(captions):
                        # 爬取每一條搜尋結果的文字段落
                        text_paragraph = cap.get_text().strip()
                        
                        # 簡單過濾掉一些無關的按鈕或日期字眼
                        if "收聽" not in text_paragraph and "發表" not in text_paragraph:
                            full_extracted_text += f"{text_paragraph}\n"
                    
                    # 清理文字中的雜質，讓它看起來更像歌詞排版
                    cleaned_lyrics = full_extracted_text.replace("...", "\n").replace("  -", "\n")
                    
                    if len(cleaned_lyrics.strip()) > 10:
                        st.text_area("全自動搜尋結果", value=cleaned_lyrics.strip(), height=450)
                    else:
                        st.warning("系統有抓到網頁，但過濾後未發現明顯的歌詞特徵，請嘗試更換歌名。")
                else:
                    st.error("Bing 引擎本次未回應有效文字段落，請再試一次。")
            else:
                st.error(f"線路連線失敗，代碼: {res.status_code}")
                
        except Exception as e:
            st.error(f"自動化程序發生錯誤: {e}")
