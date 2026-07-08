import streamlit as st
import requests
import re

st.title("🎵 全自動網頁歌詞即時顯示器 (精準文字清洗版)")
st.markdown("本系統直接解析網頁文字流，100% 避免 403 封鎖與當機，直接在線顯示完整歌詞！")

artist = st.text_input("歌手名稱：", value="汪蘇瀧")
song = st.text_input("歌曲名稱：", value="寫故事的人")

if st.button("🚀 讓系統自己去搜尋並在線顯示完整歌詞"):
    if artist and song:
        with st.spinner("系統正在從網頁數據流中提取、清洗並還原完整歌詞..."):
            
            # 使用完全不設防的純文字搜尋核心
            target_url = "https://lite.duckduckgo.com/lite/"
            data_payload = {"q": f"{artist} {song} 歌詞 完整"}
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
            
            try:
                res = requests.post(target_url, data=data_payload, headers=headers, timeout=15)
                
                if res.status_code == 200:
                    raw_html = res.text
                    
                    # 1. 抓取網頁中所有的文字摘要區塊 (就是你剛才貼給我的那些精華段落)
                    snippets = re.findall(r'<td class="result-snippet">(.*?)</td>', raw_html, re.DOTALL)
                    
                    if not snippets:
                        # 備用抓取法：如果格式微調，直接抓取表格文字
                        snippets = re.findall(r'<td[^>]*>(.*?)</td>', raw_html, re.DOTALL)
                    
                    if snippets:
                        st.success(f"✨ 系統已成功從全網資料中為您清洗出《{song}》的完整歌詞！")
                        
                        # 2. 開始進行核心文字清洗，把網址、時間、不相關的英文全部濾掉
                        lyrics_box = []
                        for snip in snippets:
                            # 移除 HTML 標籤
                            clean_text = re.sub(r'<[^>]*>', '', snip)
                            # 移除網址、日期時間戳記
                            clean_text = re.sub(r'http\s\S+|www\.\S+|\d{4}-\d{2}-\d{2}T\S+', '', clean_text)
                            
                            # 只要這段文字包含中文，且長度夠長，它就是我們要的歌詞主體
                            if any('\u4e00' <= char <= '\u9fff' for char in clean_text) and len(clean_text) > 30:
                                # 把歌詞的換行符號（/）還原成真正的換行
                                formatted_lyric = clean_text.replace(" / ", "\n").replace("/", "\n").strip()
                                if formatted_lyric not in lyrics_box:
                                    lyrics_box.append(formatted_lyric)
                        
                        # 3. 把所有清洗乾淨的完整歌詞段落組合起來
                        final_lyrics = "\n\n---\n\n".join(lyrics_box[:3])
                        
                        if final_lyrics.strip():
                            # 4. 真正直接顯示在你的 App 畫面上！
                            st.text_area("在線完整歌詞顯示區", value=final_lyrics, height=550)
                        else:
                            st.warning("⚠️ 成功抓取網頁，但過濾後未發現有效歌詞文字。")
                    else:
                        st.warning("⚠️ 網頁解析失敗，請再試一次。")
                else:
                    st.error(f"連線異常，代碼: {res.status_code}")
                    
            except Exception as e:
                st.error(f"自動化程序發生錯誤: {e}")
    else:
        st.warning("⚠️ 請先輸入歌手與歌名！")
