import streamlit as st
import google.generativeai as genai

# إعداد الصفحة لتناسب شاشة الهاتف
st.set_page_config(page_title="مافيا محمد عدنان", page_icon="🕵️", layout="centered")

# --- الإعدادات ---
API_KEY = "ضع_مفتاحك_هنا" # استبدله بالمفتاح الذي نسخته
genai.configure(api_key=API_KEY)

# اختر الموديل المتاح لديك (Flash أو Pro)
model = genai.GenerativeModel('gemini-1.5-flash') 

# --- تهيئة ذاكرة اللعبة ---
if "messages" not in st.session_state:
    st.session_state.messages = []
    # إرسال تعليمات النظام تلقائياً عند بدء التشغيل
    st.session_state.chat = model.start_chat(history=[])
    
# --- واجهة المستخدم ---
st.title("🕵️ مافيا: الجريمة والذكاء")
st.subheader("إدارة: عادل (المدير الذكي)")

# عرض الرسائل السابقة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# مدخلات اللاعب (المدير)
if prompt := st.chat_input("اكتب عدد اللاعبين أو أحداث الليلة..."):
    # عرض رسالتك
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # رد Gemini
    with st.chat_message("assistant"):
        with st.spinner("عادل يفكر في الجريمة القادمة..."):
            response = st.session_state.chat.send_message(prompt)
            full_response = response.text
            st.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})

# زر لإعادة ضبط اللعبة
if st.button("بدء لعبة جديدة"):
    st.session_state.messages = []
    st.rerun()
