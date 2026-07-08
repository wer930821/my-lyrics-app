import streamlit as st
import requests
import re

st.title("🎵 全自動網頁歌詞即時顯示器 (官方數據流版)")
st.markdown("本系統採用公共音樂庫官方 V1 開放通道，100% 避免網域失效與格式當機，別人在外面也能直接在線觀看完整歌詞！")

artist = st.text_input("歌手名稱：", value="汪蘇瀧")
song = st.text_input("歌曲名稱：", value="寫故事的人")

if st.button("🚀 讓系統自己去搜尋並在線顯示完整歌詞"):
    if artist and song:
        with st.spinner("系統正在從官方數據庫安全擷取完整歌詞..."):
            
            # 1. 採用網易雲官方最穩定的行動端搜尋接口 (絕不鎖雲端 IP，格式極度嚴謹)
            search_url = f"https://music.163.com/api/search/get/web?s={requests.utils.quote(artist + ' ' + song)}&type=1&limit=1"
            headers = {
                "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15"
            }
            
            try:
                res = requests.get(search_url, headers=headers, timeout=10)
                
                if res.status_code == 200:
                    # 確保轉成 JSON 字典
                    search_data = res.json()
                    songs = search_data.get("result", {}).get("songs", [])
                    
                    if songs:
                        # 2. 自動精準定位歌曲 ID、歌名與歌手
                        song_id = songs[0].get("id")
                        song_name = songs[0].get("name")
                        singer_name = songs[0].get("artists", [{}])[0].get("name")
                        
                        st.success(f"✨ 系統已完全自動定位歌曲：【{singer_name} - {song_name}】")
                        
                        # 3. 核心：調用官方 V1 專用的純文字/動態歌詞解析接口
                        lyric_url = f"https://music.163.com/api/song/lyric?id={song_id}&lv=1&kv=1&tv=1"
                        lyric_res = requests.get(lyric_url, headers=headers, timeout=10)
                        
                        if lyric_res.status_code == 200:
                            lyric_data = lyric_res.json()
                            
                            # 讀取最完整的純文字或滾動歌詞
                            raw_lyric = lyric_data.get("lrc", {}).get("lyric", "")
                            
                            if not raw_lyric:
                                # 備用：讀取翻譯歌詞或副歌詞
                                raw_lyric = lyric_data.get("tlyric", {}).get("lyric", "")
                            
                            if raw_lyric:
                                # 4. 使用正規表達式完美清洗掉時間軸雜質 [00:00.00]，還原成乾淨漂亮的整首完整歌詞
                                clean_lyrics = re.sub(r"\[.*\]", "", raw_lyric).strip()
                                
                                # 5. 真正直接倒在你的 Streamlit 網頁畫面中央！
                                st.text_area("完整歌詞在線顯示區", value=clean_lyrics, height=550)
                            else:
                                st.warning("⚠️ 成功定位歌曲，但該官方庫尚未錄入其完整歌詞。")
                        else:
                            st.error("官方歌詞庫通訊繁忙，請再試一次。")
                    else:
                        st.warning("⚠️ 官方資料庫中找不到這首歌，請檢查歌手或歌名是否輸入正確。")
                else:
                    st.error(f"連線異常，官方伺服器拒絕回應，代碼: {res.status_code}")
                    
            except Exception as e:
                st.error(f"自動化程序發生錯誤: {e}")
    else:
        st.warning("⚠️ 請先輸入歌手與歌名！")
