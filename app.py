import streamlit as st
import requests
from urllib.parse import quote

st.title("🎵 真正全自動完整歌詞獲取器 (無阻擋 API 版)")

artist = st.text_input("歌手：", value="汪蘇瀧")
song = st.text_input("歌名：", value="寫故事的人")

if st.button("🚀 讓系統自己去搜尋完整歌詞"):
    with st.spinner("系統正在向公共音樂數據庫檢索完整歌詞..."):
        
        # 1. 第一步：先用歌曲和歌手名稱搜尋歌曲的 ID
        search_query = quote(f"{artist} {song}")
        search_url = f"https://neteasecloudmusicapi.vercel.app/search?keywords={search_query}"
        
        try:
            # 發送搜尋請求
            search_res = requests.get(search_url, timeout=10)
            
            if search_res.status_code == 200:
                search_data = search_res.json()
                songs_list = search_data.get("result", {}).get("songs", [])
                
                if songs_list:
                    # 取得第一筆匹配成功的歌曲 ID
                    song_id = songs_list[0].get("id")
                    
                    # 2. 第二步：用歌曲 ID 直接調取「完整歌詞」的 JSON 數據 (100% 避開 403 網頁封鎖)
                    lyric_url = f"https://neteasecloudmusicapi.vercel.app/lyric?id={song_id}"
                    lyric_res = requests.get(lyric_url, timeout=10)
                    
                    if lyric_res.status_code == 200:
                        lyric_data = lyric_res.json()
                        
                        # 提取純文字歌詞（lrc格式）
                        raw_lyrics = lyric_data.get("lrc", {}).get("lyric", "")
                        
                        if raw_lyrics.strip():
                            st.success(f"✨ 系統已成功自動獲取《{song}》的完整歌詞！")
                            
                            # 簡單用正則表達式把時間軸 [00:12.34] 濾掉，只留下乾淨的歌詞文字
                            import re
                            clean_lyrics = re.sub(r"\[.*\]", "", raw_lyrics).strip()
                            
                            st.text_area("完整歌詞內文", value=clean_lyrics, height=500)
                        else:
                            st.warning("系統找到了這首歌，但該平台尚未錄入此歌曲的歌詞文字。")
                    else:
                        st.error("擷取歌詞文本失敗，伺服器未回應。")
                else:
                    st.warning("公共數據庫中未找到與該歌手/歌名匹配的歌曲 ID。")
            else:
                st.error(f"搜尋服務連線失敗，代碼: {search_res.status_code}")
                
        except Exception as e:
            st.error(f"自動化程序發生錯誤: {e}")
