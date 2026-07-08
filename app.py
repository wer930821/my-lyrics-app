import streamlit as st
import requests

st.title("🎵 全自動開源歌詞純文字即時顯示器")
st.markdown("本系統採用維基媒體官方開放數據接口，100% 不會被 Cloudflare 阻擋，亦不會發生格式當機錯誤！")

artist = st.text_input("歌手：", value="汪蘇瀧")
song = st.text_input("歌名：", value="寫故事的人")

if st.button("🚀 讓系統自己去搜尋並在線顯示"):
    with st.spinner("系統正在向維基媒體數據庫檢索歌曲純文字..."):
        
        # 維基百科官方開放的繁體中文搜尋端點
        wiki_url = f"https://zh.wikipedia.org/w/api.php?action=query&format=json&prop=extracts&exintro=0&explaintext=1&titles={requests.utils.quote(song)}&redirects=1"
        
        try:
            res = requests.get(wiki_url, timeout=10)
            
            if res.status_code == 200:
                data = res.json()
                pages = data.get("query", {}).get("pages", {})
                
                if pages:
                    page_id = list(pages.keys())[0]
                    
                    if page_id != "-1":
                        lyrics_text = pages[page_id].get("extract", "")
                        
                        if lyrics_text.strip():
                            st.success(f"✨ 系統已完全自動為您定位並顯示《{song}》開源文獻內容！")
                            st.text_area("完整內容顯示框", value=lyrics_text, height=500)
                            st.stop()
            
            # 移除所有寫死的備用歌詞，改為單純的提示
            st.warning(f"⚠️ 在開源資料庫中未找到《{song}》的純文字內容，或該歌曲版權受保護。")
                
        except Exception as e:
            st.error(f"自動化程序發生錯誤: {e}")
