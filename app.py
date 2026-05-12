import streamlit as st
import google.generativeai as genai

# 1. إعدادات الصفحة
st.set_page_config(page_title="مافيا محمد عدنان", page_icon="🕵️", layout="centered")

# 2. ضع مفتاح الـ API الخاص بك هنا بين العلامتين
API_KEY = "AIzaSyB5k4agOUL57Qtm6MDz8UB4SSbcxFeQWc4" 

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash') # أو الموديل الذي اخترته

# 3. تهيئة الجلسة (ذاكرة اللعبة)
if "chat" not in st.session_state:
    # هنا نضع التعليمات البرمجية لـ "عادل" ليعرف دوره من أول لحظة
    system_instruction = (
        "أنت 'عادل'، مدير لعبة المافيا بأسلوب محمد عدنان. "
        "مهمتك إدارة اللعبة، توزيع الأدوار، وكتابة قصص جرائم مشوقة. "
        "ابدأ دائماً بالترحيب باللاعبين واسأل عن عددهم وأسمائهم."
    )
    st.session_state.chat = model.start_chat(history=[])
    # إرسال التعليمات في خلفية التطبيق
    st.session_state.chat.send_message(system_instruction)
    st.session_state.messages = []

# 4. واجهة المستخدم
st.title("🕵️ مافيا: الجريمة والذكاء")
st.markdown("---")

# عرض المحادثة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# إدخال المدير
if prompt := st.chat_input("اكتب هنا (مثلاً: نحن 6 لاعبين)..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = st.session_state.chat.send_message(prompt)
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})

# زر المسح
if st.sidebar.button("لعبة جديدة 🔄"):
    st.session_state.messages = []
    st.session_state.chat = model.start_chat(history=[])
    st.rerun()
