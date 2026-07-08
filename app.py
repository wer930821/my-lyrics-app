import streamlit as st
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import quote

st.title("🎵 真正全網自動完整歌詞提取器")

artist = st.text_input("歌手：", value="汪蘇瀧")
song = st.text_input("歌名：", value="寫故事的人")

if st.button("🚀 讓系統自己去抓取完整歌詞"):
    with st.spinner("系統正在全網點擊網頁、穿透封鎖提取完整歌詞中..."):
        
        # 1. 轉碼關鍵字，先透過不受阻擋的 DuckDuckGo 尋找真正的歌詞網址
        keyword = quote(f"{artist} {song} 歌詞")
        search_url = f"https://html.duckduckgo.com/html/?q={keyword}"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        
        try:
            search_res = requests.get(search_url, headers=headers, timeout=10)
            if search_res.status_code == 200:
                soup = BeautifulSoup(search_res.text, "html.parser")
                
                # 抓取搜尋結果的第一個實際網頁連結
                links = soup.find_all("a", class_="result__url")
                
                if links:
                    # 拿到目標歌詞網（例如 KKBOX 或 Genius）的真實網址
                    target_url = links[0]["href"].strip()
                    
                    # 2. 終極核心：透過 r.jina.ai 這個完全免費且專門對抗 Cloudflare 的網頁純文字轉換代理
                    # 它會代替我們的伺服器「點進去網頁」，把整頁的所有文字（包含完整歌詞）全部拔下來
                    proxy_reader_url = f"https://r.jina.ai/{target_url}"
                    
                    st.info(f"🔗 系統已自動尋獲歌詞網頁，正在深度提取整頁內文...")
                    lyric_res = requests.get(proxy_reader_url, timeout=15)
                    
                    if lyric_res.status_code == 200:
                        raw_markdown = lyric_res.text
                        
                        # 3. 清洗雜質：過濾掉網頁的頁首頁尾、廣告、隱私政策，只留下核心歌詞
                        lines = raw_markdown.split("\n")
                        cleaned_lines = []
                        for line in lines:
                            # 剔除明顯的網頁導覽標籤或廣告關鍵字
                            if any(x in line for x in ["Cookie", "隱私權", "登入", "訂閱", "App", "Copyright", "版權所有"]):
                                continue
                            cleaned_lines.append(line)
                        
                        final_lyrics = "\n".join(cleaned_lines).strip()
                        
                        st.success(f"✨ 系統已全自動穿透防禦，成功抓取《{song}》完整歌詞！")
                        st.text_area("完整歌詞內文結果", value=final_lyrics, height=500)
                    else:
                        st.error("❌ 嘗試點進網頁提取完整文字時失敗，代理伺服器遭拒絕。")
                else:
                    st.warning("❌ 搜尋引擎未能定位到該歌曲的任何歌詞網站。")
            else:
                st.error("❌ 線路連線失敗，無法發起自動搜尋。")
                
        except Exception as e:
            st.error(f"自動化程序發生錯誤: {e}")
