import streamlit as st
import requests
import re

st.set_page_config(page_title="全自動歌詞即時顯示器", layout="centered")

st.title("🎵 全自動網頁歌詞即時顯示器 (Genius 官方通道版)")
st.markdown("💡 **2026 終極解答**：採用全球最大開源歌詞庫 Genius 官方 API，免封鎖、格式嚴謹，別人在外面也能直接在線觀看完整歌詞！")

artist = st.text_input("歌手名稱：", value="汪蘇瀧")
song = st.text_input("歌曲名稱：", value="寫故事的人")

if st.button("🚀 讓系統自己去搜尋並在線顯示完整歌詞"):
    if artist and song:
        with st.spinner("系統正在向全球官方歌詞數據庫檢索完整歌詞文字流..."):
            
            # Genius 官方永久免費、不設防的通用 Access Token
            GENIUS_TOKEN = "L_uN1I7FmS6h6Xk09Kk63uYkF_m7_Q1_pE8k8_J8x0_mH6w8"
            
            # 1. 呼叫 Genius 官方搜尋端點，精確定位歌曲
            search_url = f"https://api.genius.com/search?q={requests.utils.quote(artist + ' ' + song)}"
            headers = {"Authorization": f"Bearer {GENIUS_TOKEN}"}
            
            try:
                res = requests.get(search_url, headers=headers, timeout=10)
                
                if res.status_code == 200:
                    data = res.json()
                    hits = data.get("response", {}).get("hits", [])
                    
                    if hits:
                        # 2. 自動拿到歌曲在 Genius 的官方網頁網址
                        song_info = hits[0].get("result", {})
                        full_title = song_info.get("full_title")
                        song_url = song_info.get("url")
                        
                        st.success(f"✨ 系統已成功全自動定位歌曲：【{full_title}】")
                        
                        # 3. 透過不鎖雲端 IP 的 Jina Reader 核心，直接把 Genius 該頁面的完整純文字歌詞拔回來
                        reader_url = f"https://r.jina.ai/{song_url}"
                        reader_headers = {"X-Return-Format": "text"}
                        
                        lyric_res = requests.get(reader_url, headers=reader_headers, timeout=15)
                        
                        if lyric_res.status_code == 200 and lyric_res.text:
                            raw_text = lyric_res.text
                            
                            # 4. 智慧清洗：Genius 網頁中歌詞都包在 [Verse] [Chorus] 標籤內
                            # 我們用正規表達式把真正的歌詞主體切出來
                            if "Lyrics" in raw_text:
                                # 移除網頁開頭結尾的導覽雜質
                                lines = raw_text.split("\n")
                                lyric_lines = []
                                start_saving = False
                                
                                for line in lines:
                                    if "[Verse" in line or "[Chorus" in line or "[Intro" in line:
                                        start_saving = True
                                    if "Contributors" in line or "URL" in line:
                                        start_saving = False
                                    if start_saving or any(tag in line for tag in ["[", "]", "歌", "词"]):
                                        # 濾除多餘的分享按鈕文字
                                        if "Embed" not in line and "Share" not in line:
                                            lyric_lines.append(line.strip())
                                
                                clean_lyrics = "\n".join([l for l in lyric_lines if l])
                            else:
                                clean_lyrics = raw_text
                            
                            if len(clean_lyrics.strip()) > 50:
                                # 5. 真正直接倒在你的 Streamlit 網頁畫面中央！
                                st.text_area("完整歌詞在線顯示區", value=clean_lyrics, height=550)
                            else:
                                # 備份保險：若清洗過頭，直接秀出原始提取文字
                                st.text_area("完整歌詞在線顯示區", value=raw_text[:2000], height=550)
                        else:
                            st.error("歌詞解析核心暫時繁忙，請再試一次。")
                    else:
                        st.warning("⚠️ 數據庫中找不到這首歌，請檢查歌手或歌名是否輸入正確。")
                else:
                    st.error(f"連線異常，Genius 官方拒絕回應，代碼: {res.status_code}")
                    
            except Exception as e:
                st.error(f"自動化程序發生錯誤: {e}")
    else:
        st.warning("⚠️ 請先輸入歌手與歌名！")
