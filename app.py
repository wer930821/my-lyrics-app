import streamlit as st
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

st.title("🎵 全網通！全自動完整歌詞獲取器")
st.markdown("本系統採用商業級 ScraperAPI 真實住宅代理，100% 穿透各大音樂網防火牆，任何人隨時隨地皆可使用。")

# 1. 安全檢查：確保有填入 API Key
if "SCRAPER_API_KEY" in st.secrets:
    scraper_key = st.secrets["SCRAPER_API_KEY"]
else:
    st.error("⚠️ 請先在 Streamlit Cloud 的 Secrets 中設定 SCRAPER_API_KEY！")
    st.stop()

artist = st.text_input("歌手：", value="汪蘇瀧")
song = st.text_input("歌名：", value="寫故事的人")

if st.button("🚀 讓系統自己去搜尋並顯示歌詞"):
    with st.spinner("系統正在透過全球住宅代理網路，穿透封鎖提取完整歌詞..."):
        
        # 轉碼關鍵字
        keyword = quote(f"{artist} {song} 歌詞")
        search_url = f"https://html.duckduckgo.com/html/?q={keyword}"
        
        # 透過 ScraperAPI 去請求搜尋引擎，防止搜尋引擎阻擋雲端伺服器
        proxy_search_url = f"http://api.scraperapi.com?api_key={scraper_key}&url={search_url}"
        
        try:
            search_res = requests.get(proxy_search_url, timeout=30)
            
            if search_res.status_code == 200:
                soup = BeautifulSoup(search_res.text, "html.parser")
                links = soup.find_all("a", class_="result__url")
                
                if links:
                    # 拿到真正的歌詞網址（例如 KKBOX、Genius）
                    target_url = links[0]["href"].strip()
                    st.info(f"🔗 系統已自動尋獲最佳歌詞網頁，正在強力解鎖提取整頁內文...")
                    
                    # 核心突破：透過 ScraperAPI 點進 KKBOX，它會自動模擬真實人類、破解 Cloudflare 403 封鎖
                    proxy_lyric_url = f"http://api.scraperapi.com?api_key={scraper_key}&url={quote(target_url)}"
                    lyric_res = requests.get(proxy_lyric_url, timeout=30)
                    
                    if lyric_res.status_code == 200:
                        lyric_soup = BeautifulSoup(lyric_res.text, "html.parser")
                        
                        # 抓取網頁內所有的純文字
                        raw_text = lyric_soup.get_text()
                        
                        # 清洗多餘的空白，讓排版乾淨
                        clean_text = "\n".join([line.strip() for line in raw_text.split("\n") if line.strip()])
                        
                        st.success(f"✨ 系統已全自動穿透防禦，成功顯示《{song}》完整歌詞！")
                        st.text_area("完整網頁擷取結果（內含歌詞）", value=clean_text, height=500)
                    else:
                        st.error(f"代理伺服器嘗試破牆失敗，錯誤代碼: {lyric_res.status_code}")
                else:
                    st.warning("搜尋引擎未能定位到該歌曲的歌詞網站。")
            else:
                st.error("搜尋引擎代理連線超時，請再試一次。")
                
        except Exception as e:
            st.error(f"自動化程序發生錯誤: {e}")
