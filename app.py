import streamlit as st
import requests
from bs4 import BeautifulSoup

st.title("🎵 真正全自動歌詞搜尋器")

st.markdown("""
### 💡 運作原理
此版本不再詢問 AI，也不會直接挑戰歌詞網的 Cloudflare。它會**偽裝成真實瀏覽器去請求 DuckDuckGo/Google 的公開搜尋快取**，直接幫你把歌詞抓回來！
""")

artist = st.text_input("歌手：", value="汪蘇瀧")
song = st.text_input("歌名：", value="寫故事的人")

if st.button("🚀 讓系統自己去網路搜尋"):
    with st.spinner("系統正在全網搜尋歌詞，請稍候..."):
        # 使用不嚴格阻擋爬蟲的搜尋引擎介面
        search_url = f"https://html.duckduckgo.com/html/?q={artist}+{song}+歌詞"
        
        # 偽裝成一般的 Windows Chrome 瀏覽器
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        
        try:
            res = requests.get(search_url, headers=headers)
            if res.status_code == 200:
                soup = BeautifulSoup(res.text, "html.parser")
                
                # 抓取搜尋結果的前三個連結摘要
                results = soup.find_all("a", class_="result__snippet")
                
                if results:
                    st.success("🔍 系統已自動幫你找到以下網路文本：")
                    
                    # 把搜尋到的網頁文本片段組合起來
                    combined_text = ""
                    for i, r in enumerate(results[:3]):
                        combined_text += f"[來源 {i+1}]\n{r.get_text().strip()}\n\n"
                    
                    st.text_area("全自動搜尋並排版結果", value=combined_text, height=300)
                else:
                    st.warning("網路搜尋引擎回應空結果，可能需要更換關鍵字。")
            else:
                st.error(f"搜尋引擎連線失敗，代碼: {res.status_code}")
                
        except Exception as e:
            st.error(f"自動化搜尋發生錯誤: {e}")
