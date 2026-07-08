import streamlit as st
import lyricsgenius

st.title("🎵 自動歌詞抓取器")

# 請在 Streamlit Secrets 設定 GENIUS_API_TOKEN
token = st.secrets.get("GENIUS_API_TOKEN")

if not token:
    st.error("請在 Secrets 設定中加入 GENIUS_API_TOKEN")
    st.stop()

genius = lyricsgenius.Genius(token)

artist_name = st.text_input("輸入歌手：", "")
song_name = st.text_input("輸入歌名：", "")

if st.button("🚀 開始自動抓取"):
    with st.spinner("正在從 Genius 資料庫搜尋歌詞..."):
        try:
            # 自動搜尋歌詞
            song = genius.search_song(song_name, artist_name)
            if song:
                st.subheader(f"{song.title} - {song.artist}")
                st.text_area("歌詞內容", value=song.lyrics, height=400)
            else:
                st.warning("找不到這首歌，請確認歌手或歌名是否正確。")
        except Exception as e:
            st.error(f"搜尋失敗: {e}")
