import streamlit as st
import requests

# 1. 網頁門面設計
st.title("🎵 智慧全自動歌詞抓取 × AI 完美排版神器")
st.write("真正全自動！利用 Gemini 內建 Google 搜尋功能直接抓取歌詞，100% 成功、免申請搜尋 API！")

# 2. 🔑 你的專屬 Gemini API Key
GEMINI_API_KEY = "AQ.Ab8RN6IyGKuv5spXFgcgH_U436HoMhmzpYlHItZ5SN-Mdk90Kg"

# 3. 畫面輸入框
artist = st.text_input("請輸入歌手名稱：", value="汪蘇瀧")
song_name = st.text_input("請輸入歌曲名稱：", value="寫故事的人")

# 💡 函式：開啟 Gemini 的聯網搜尋功能，讓 AI 自己去 Google 抓歌詞
def ai_search_and_format(artist_name, song):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"
    headers = {"Content-Type": "application/json"}
    
    prompt_text = f"""
    請使用你內建的 Google 搜尋功能，去網路上搜尋歌手「{artist_name}」演唱的歌曲《{song}》的完整歌詞。
    
    找到歌詞後，請嚴格執行以下排版規則：
    1. 將歌詞內容全部轉換為【繁體中文】輸出。
    2. 徹底刪除所有「作詞、作曲、編曲、製作人、錄音室、企劃、出品人」等幕幕後工作人員名單。
    3. 刪除所有像 [00:12.34] 這樣的時間戳記與開頭的歌名歌手介紹。
    4. 歌詞必須整齊地「一句一行」，不要擠成一團。
    5. 直接輸出排版後的歌詞，絕對不要說任何一句解釋、前言或搜尋過程的廢話。
    6. 如果在網路上真的完全找不到這首歌的歌詞，請只回答「找不到歌詞」。
    """
    
    # 💡 修正後的官方標準聯網 API JSON 結構
    payload = {
        "contents": [{"parts": [{"text": prompt_text}]}],
        "tools": [{"googleSearch": {}}]
    }
    
    response = requests.post(url, headers=headers, json=payload, timeout=30)
    if response.status_code == 200:
        res_data = response.json()
        try:
            return res_data['candidates'][0]['content']['parts'][0]['text']
        except KeyError:
            raise Exception(f"收到未預期的回應結構：{res_data}")
    else:
        error_msg = response.text
        raise Exception(f"AI 連線失敗，錯誤資訊：{error_msg}")

# 4. 當按鈕被按下時
if st.button("🚀 啟動全自動抓取與 AI 排版", type="primary"):
    if not artist or not song_name:
        st.warning("請先輸入歌手和歌曲名稱！")
    else:
        with st.spinner("Gemini 正在啟動 Google 搜尋引擎，全自動抓取並排版中..."):
            try:
                formatted_lyric = ai_search_and_format(artist, song_name)
                
                if "找不到歌詞" in formatted_lyric:
                    st.error("❌ Gemini 聯網搜尋後未找到完整歌詞，請確認歌名是否正確。")
                else:
                    st.success("✨ 聯網自動抓取 ＋ AI 智慧排版完成！")
                    
                    # 逐行輸出，乾乾淨淨
                    for line in formatted_lyric.split('\n'):
                        if line.strip():
                            st.text(line.strip())
                            
            except Exception as e:
                st.error(f"處理時發生錯誤：{e}")import streamlit as st
import requests

# 1. 網頁門面設計與手機版畫面優化
st.set_page_config(page_title="AI 歌詞完美排版神器", page_icon="🎵", layout="centered")

st.title("🎵 智慧全自動歌詞抓取 × AI 完美排版")
st.write("真正全自動！利用 AI 聯網功能直接抓取歌詞，100% 成功、免申請搜尋 API！")

# 2. 🔑 你的專屬 Gemini API Key
GEMINI_API_KEY = "AQ.Ab8RN6IyGKuv5spXFgcgH_U436HoMhmzpYlHItZ5SN-Mdk90Kg"

# 3. 畫面輸入框
artist = st.text_input("請輸入歌手名稱：", value="汪蘇瀧")
song_name = st.text_input("請輸入歌曲名稱：", value="寫故事的人")

# 💡 函式：開啟 Gemini 的聯網搜尋功能，讓 AI 自己去 Google 抓歌詞
def ai_search_and_format(artist_name, song):
    # 統一使用穩定的 v1beta 接口與支援 googleSearch 的模型
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"
    headers = {"Content-Type": "application/json"}
    
    prompt_text = f"""
    請使用你內建的 Google 搜尋功能，去網路上搜尋歌手「{artist_name}」演唱的歌曲《{song}》的完整歌詞。
    
    找到歌詞後，請嚴格執行以下排版規則：
    1. 將歌詞內容全部轉換為【繁體中文】輸出。
    2. 徹底刪除所有「作詞、作曲、編曲、製作人、錄音室、企劃、出品人」等幕後工作人員名單。
    3. 刪除所有像 [00:12.34] 這樣的時間戳記與開頭的歌名歌手介紹。
    4. 歌詞必須整齊地「一句一行」，不要擠成一團。
    5. 直接輸出排版後的歌詞，絕對不要說任何一句解釋、前言或搜尋過程的廢話。
    6. 如果在網路上真的完全找不到這首歌的歌詞，請只回答「找不到歌詞」。
    """
    
    payload = {
        "contents": [{"parts": [{"text": prompt_text}]}],
        "tools": [{"googleSearch": {}}]
    }
    
    response = requests.post(url, headers=headers, json=payload, timeout=30)
    if response.status_code == 200:
        res_data = response.json()
        try:
            return res_data['candidates'][0]['content']['parts'][0]['text']
        except KeyError:
            raise Exception("回應結構解析失敗")
    else:
        raise Exception(f"AI 連線失敗，狀態碼：{response.status_code}")

# 4. 當按鈕被按下時
if st.button("🚀 啟動全自動抓取與 AI 排版", type="primary", use_container_width=True):
    if not artist or not song_name:
        st.warning("請先輸入歌手和歌曲名稱！")
    else:
        with st.spinner("AI 正在聯網搜尋並智慧排版中..."):
            try:
                formatted_lyric = ai_search_and_format(artist, song_name)
                
                if "找不到歌詞" in formatted_lyric:
                    st.error("❌ 聯網搜尋後未找到完整歌詞，請確認歌名是否正確。")
                else:
                    st.success("✨ 歌詞智慧排版完成！")
                    
                    # 用一個美觀的容器顯示歌詞，方便手機複製
                    lyric_box = ""
                    for line in formatted_lyric.split('\n'):
                        if line.strip():
                            lyric_box += line.strip() + "\n"
                    st.text_area("📋 排版結果（長按可全選複製）", value=lyric_box, height=400)
                            
            except Exception as e:
                st.error(f"處理時發生錯誤：{e}")