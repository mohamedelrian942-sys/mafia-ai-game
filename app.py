import streamlit as st
import random

# إعدادات الهاتف
st.set_page_config(page_title="مدير المافيا", page_icon="🃏")

st.title("🃏 لوحة إدارة المافيا")

# 1. إدخال الأسماء
names_input = st.text_area("أدخل أسماء اللاعبين (فصل بينهم بفاصلة أو سطر جديد):")
players = [name.strip() for name in names_input.split('\n') if name.strip()] or \
          [name.strip() for name in names_input.split(',') if name.strip()]

# 2. اختيار الأدوار
st.sidebar.header("إعدادات الأدوار")
roles_pool = []

# المافيا
mafia_count = st.sidebar.number_input("عدد المافيا", 1, 10, 2)
roles_pool.extend(["مافيا (شيخ)"] + ["مافيا"] * (mafia_count - 1))

# الأدوار الخاصة
if st.sidebar.checkbox("إسعاف", value=True): roles_pool.append("إسعاف")
if st.sidebar.checkbox("قناص", value=True): roles_pool.append("قناص")
if st.sidebar.checkbox("عمدة", value=True): roles_pool.append("عمدة")
if st.sidebar.checkbox("ولد صالح", value=True): roles_pool.append("ولد صالح")

# بقية اللاعبين مواطنين
remaining = len(players) - len(roles_pool)
if remaining > 0:
    roles_pool.extend(["مواطن صالح"] * remaining)

# 3. توزيع الأدوار
if st.button("توزيع الأدوار عشوائياً 🎲"):
    if len(players) < len(roles_pool):
        st.error(f"عدد الأدوار ({len(roles_pool)}) أكبر من عدد اللاعبين ({len(players)})!")
    else:
        shuffled_roles = roles_pool[:len(players)]
        random.shuffle(shuffled_roles)
        st.session_state.game_data = dict(zip(players, shuffled_roles))
        st.session_state.revealed = set()
        st.success("تم توزيع الأدوار! مرر الهاتف للاعبين.")

# 4. كشف الكروت (مرحلة التوزيع السرية)
if "game_data" in st.session_state:
    st.divider()
    player_to_see = st.selectbox("اختار اسمك لكشف كرتك:", ["اختر اسمك..."] + players)
    
    if player_to_see != "اختر اسمك...":
        if st.button(f"أنا {player_to_see}، اكشف كرتي 👁️"):
            role = st.session_state.game_data[player_to_see]
            st.info(f"دورك هو: **{role}**")
            st.warning("الرجاء إغلاق الكرت بعد رؤيته لضمان السرية!")
            
    if st.sidebar.button("كشف كل الأدوار (للمدير فقط) 🕵️"):
        st.sidebar.write(st.session_state.game_data)

# 5. سجل اللعبة (تتبع الموتى)
st.sidebar.divider()
st.sidebar.header("سجل الموتى")
for p in players:
    if st.sidebar.checkbox(f"إقصاء {p}"):
        st.sidebar.write(f"❌ {p} غادر اللعبة")
