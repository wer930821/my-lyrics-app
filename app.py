import streamlit as st
import google.generativeai as genai

st.title("🎵 AI 偵錯器 v2")

api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("請在 Streamlit Secrets 設定中填入 GEMINI_API_KEY")
    st.stop()

genai.configure(api_key=api_key)

if st.button("🚀 執行連線測試"):
    try:
        # 使用更穩定的方式列出模型
        models = genai.list_models()
        st.write("連線成功！以下是你帳號可用的模型清單：")
        for m in models:
            st.write(f"- {m.name}")
    except Exception as e:
        st.error(f"連線失敗，請檢查 API Key 是否正確。詳細錯誤: {e}")
