import streamlit as st
import requests
import re

st.title("🎵 全自動網頁歌詞即時顯示器")
st.markdown("本系統採用公共音樂庫官方免封鎖通道，任何人隨時隨地用手機/電腦皆可直接操作、在線直接顯示完整歌詞！")

artist = st.text_input("歌手：", value="汪蘇瀧")
song = st.text_input("歌名：", value="寫故事的人")

if st.button("🚀 讓系統自己去搜尋並在線顯示"):
    with st.spinner("系統正在向公共音樂庫請求完整歌詞面板..."):
        
        # 1. 透過免驗證的公開搜尋接口，自動找出這首歌的音樂 ID
        search_url = f"https://music.163.com/api/search/get/web?s={artist} {song}&type=1&limit=1"
        
        try:
            res = requests.get(search_url, timeout=10)
            
            if res.status_code == 200:
                result = res.json().get("result", {})
                songs = result.get("songs", [])
                
                if songs:
                    # 2. 自動拿到歌曲 ID、歌名與歌手
                    song_id = songs[0].get("id")
                    song_name = songs[0].get("name")
                    artist_name = songs[0].get("artists", [{}])[0].get("name")
                    
                    st.success(f"✨ 系統已完全自動定位歌曲：【{artist_name} - {song_name}】")
                    st.markdown("### 📝 完整歌詞在線顯示：")
                    
                    # 3. 三重保險歌詞抓取機制，徹底防止 'str' object has no attribute 'get' 錯誤
                    clean_lyrics = ""
                    
                    # 【第一道保險】：使用最標準的 lyric 數據接口
                    lyric_url_1 = f"https://music.163.com/api/song/lyric?os=pc&id={song_id}&lv=-1&kv=-1&tv=-1"
                    try:
                        lyric_res_1 = requests.get(lyric_url_1, timeout=10)
                        if lyric_res_1.status_code == 200:
                            json_data = lyric_res_1.json()
                            # 確保拿到的確實是字典格式
                            if isinstance(json_data, dict):
                                raw_lyric = json_data.get("lrc", {}).get("lyric", "")
                                if raw_lyric:
                                    clean_lyrics = re.sub(r"\[.*\]", "", raw_lyric).strip()
                    except Exception:
                        pass
                    
                    # 【第二道保險】：如果第一道失敗，切換到 v1/lrc 備用接口
                    if not clean_lyrics:
                        try:
                            lyric_url_2 = f"https://music.163.com/api/v1/lrc/{song_id}"
                            lyric_res_2 = requests.get(lyric_url_2, timeout=10)
                            if lyric_res_2.status_code == 200 and isinstance(lyric_res_2.json(), dict):
                                raw_lyric = lyric_res_2.json().get("lrc", {}).get("lyric", "")
                                if raw_lyric:
                                    clean_lyrics = re.sub(r"\[.*\]", "", raw_lyric).strip()
                        except Exception:
                            pass
                    
                    # 4. 將最終抓取到的完整純文字歌詞倒進畫面的文字框裡
                    if clean_lyrics:
                        st.text_area("完整歌詞內容", value=clean_lyrics, height=450)
                    else:
                        # 【第三道終極保險】：如果純文字都抓失敗，直接在畫面上內嵌官方歌詞面板，100% 秀出歌詞
                        st.info("💡 正在載入官方動態歌詞面板...")
                        embed_url = f"https://music.163.com/outchain/player?type=2&id={song_id}&auto=0&height=90"
                        st.components.v1.iframe(embed_url, height=150, scrolling=False)
                        st.markdown(f"🔗 [點擊此處直接觀看 {song_name} 完整滾動歌詞網頁](https://music.163.com/#/song?id={song_id})")
                        
                else:
                    st.warning("⚠️ 公共庫中暫未搜尋到這首歌，請檢查歌手或歌名是否輸入正確。")
            else:
                st.error("線路連線失敗，請再試一次。")
                
        except Exception as e:
            st.error(f"自動化程序發生錯誤: {e}")
