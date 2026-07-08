import streamlit as st
import google.generativeai as genai

st.title("🎵 AI 模型偵錯器")

api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.error("請設定 API Key")
    st.stop()

genai.configure(api_key=api_key)

if st.button("🔍 檢查可用的模型"):
    try:
        # 列出所有可用的模型，看看你的帳號到底支援哪個
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_method_names]
        st.write("目前你的帳號支援的模型列表：", models)
    except Exception as e:
        st.error(f"偵錯失敗: {e}")
