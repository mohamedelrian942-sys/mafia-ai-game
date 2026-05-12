import streamlit as st
import google.generativeai as genai

# 1. إعدادات Gemini
genai.configure(api_key="ضع_مفتاحك_هنا") # احصل عليه من AI Studio
model = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="مافيا محمد عدنان", page_icon="🕵️‍♂️")

st.title("🕵️‍♂️ مدير لعبة المافيا")
st.caption("إدارة اللعبة بأسلوب محمد عدنان وذكاء Gemini")

# إنشاء ذاكرة للعبة
if "messages" not in st.session_state:
    st.session_state.messages = []
    # رسالة البداية المخفية لضبط القواعد
    st.session_state.messages.append({"role": "user", "content": "ابدأ اللعبة الآن، رحب بالمدير واطلب منه إدخال أسماء الـ 14 لاعباً."})

# عرض المحادثة
for message in st.session_state.messages[1:]: # تخطي رسالة الإعداد
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# إدخال المدير للأوامر
if prompt := st.chat_input("ماذا حدث الآن؟ (مثلاً: المافيا قتلوا أحمد)"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = model.generate_content(str(st.session_state.messages))
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
