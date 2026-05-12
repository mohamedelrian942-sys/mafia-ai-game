import streamlit as st
import random

# --- إعدادات الصفحة ---
st.set_page_config(page_title="مدير مافيا الاحترافي", page_icon="🎙️", layout="centered")

# --- منع خطأ AttributeError بتعريف الحالة الابتدائية ---
if "step" not in st.session_state:
    st.session_state.step = 0  # 0 تعني مرحلة ما قبل البدء

# --- قاعدة بيانات السيناريوهات ---
SCENARIOS = {
    "💎 سرقة الموناليزا": {
        "location": "متحف اللوفر - القاعة الكبرى",
        "weapon": "ليزر حراري / مفتاح منسوخ",
        "roles": ["أمين المتحف", "سائح فضولي", "خبير كمرات", "منظف ليلي", "بروفيسور فنون", "صحفي متخفي"]
    },
    "🚂 جريمة قطار الشرق": {
        "location": "مقصورة الدرجة الأولى",
        "weapon": "سم في الشاي / خنجر أثري",
        "roles": ["قائد القطار", "طبيب جراح", "أرملة ثرية", "جندي سابق", "طباخ عربة الطعام", "مساعد شخصي"]
    },
    "⚽ معسكر المنتخب": {
        "location": "غرفة الملابس - ملعب لوسيل",
        "weapon": "تسريب الخطة / تسميم المشروب",
        "roles": ["المدرب الفني", "حارس المرمى", "محلل فيديو", "طبيب الفريق", "رئيس البعثة", "مدلك اللاعبين"]
    }
}

# --- واجهة التطبيق ---
st.title("🎙️ مدير جولة المافيا")

# 1. إدخال اللاعبين في القائمة الجانبية
st.sidebar.header("👥 إعدادات اللاعبين")
names_input = st.sidebar.text_area("أسماء اللاعبين (كل اسم في سطر):", height=150)
players = [n.strip() for n in names_input.split('\n') if n.strip()]

selected_key = st.sidebar.selectbox("🎬 اختر السيناريو:", list(SCENARIOS.keys()))
mafia_count = st.sidebar.number_input("🤫 عدد المافيا:", 1, 3, 1)

# 2. زر بدء الجولة
if st.sidebar.button("🚀 بدء جولة جديدة"):
    if len(players) < 3:
        st.error("⚠️ تحتاج 3 لاعبين على الأقل.")
    else:
        # منطق التوزيع
        mafias = random.sample(players, mafia_count)
        others = [p for p in players if p not in mafias]
        detective = random.choice(others) if others else None
        doctor = random.choice([p for p in others if p != detective]) if len(others) > 1 else None
        
        scenario = SCENARIOS[selected_key]
        shuffled_roles = list(scenario['roles'])
        random.shuffle(shuffled_roles)
        
        game_assignments = {}
        for i, p in enumerate(players):
            role_type = "مواطن"
            if p in mafias: role_type = "مافيا"
            elif p == detective: role_type = "محقق"
            elif p == doctor: role_type = "طبيب"
            
            game_assignments[p] = {
                "role": role_type,
                "character": shuffled_roles[i % len(shuffled_roles)],
                "location": scenario['location'] if p not in mafias else "؟؟؟",
                "weapon": scenario['weapon'] if p not in mafias else "؟؟؟"
            }
        
        st.session_state.game = game_assignments
        st.session_state.current_scenario_key = selected_key
        st.session_state.step = 1 # ننتقل لخطوة التوزيع
        st.rerun()

# --- نظام إدارة المراحل ---

# الحالة 0: شاشة الترحيب
if st.session_state.step == 0:
    st.info("قم بإدخال الأسماء في القائمة الجانبية ثم اضغط 'بدء جولة جديدة' للبدء.")

# الحالة 1: توزيع الأدوار
elif st.session_state.step == 1:
    st.header("Step 1: كشف الأدوار 👁️")
    st.write("مرر الهاتف لكل لاعب ليفتح الصندوق الخاص به سراً.")
    
    player_select = st.selectbox("من أنت؟", ["-- اختر اسمك --"] + list(st.session_state.game.keys()))
    if player_select != "-- اختر اسمك --":
        data = st.session_state.game[player_select]
        with st.expander("انقر لرؤية هويتك"):
            st.write(f"🎭 شخصيتك: **{data['character']}**")
            st.write(f"💼 دورك السري: **{data['role']}**")
            st.write(f"📍 السالفة: {data['location']}")
            if data['role'] == "مافيا":
                st.error("أنت برا السالفة! لا تنكشف.")
            st.caption("أغلق المربع فوراً!")
    
    if st.button("انتهى الجميع؟ انتقل لليل 🌙"):
        st.session_state.step = 2
        st.rerun()

# الحالة 2: مرحلة الليل
elif st.session_state.step == 2:
    st.header("Step 2: مرحلة الليل 🌙")
    st.warning("أمر القائد: 'ناموا جميعاً وأغلقوا أعينكم!'")
    
    with st.expander("1️⃣ استدعاء المافيا"):
        mafias_list = [p for p, d in st.session_state.game.items() if d['role'] == 'مافيا']
        st.write(f"المافيا هم: **{', '.join(mafias_list)}**")
    
    with st.expander("2️⃣ استدعاء الطبيب"):
        docs = [p for p, d in st.session_state.game.items() if d['role'] == 'طبيب']
        st.write(f"الطبيب: **{', '.join(docs) if docs else 'لا يوجد'}**")

    with st.expander("3️⃣ استدعاء المحقق"):
        dets = [p for p, d in st.session_state.game.items() if d['role'] == 'محقق']
        st.write(f"المحقق: **{', '.join(dets) if dets else 'لا يوجد'}**")

    if st.button("بدء النقاش (الصباح) ☀️"):
        st.session_state.step = 3
        st.rerun()

# الحالة 3: الصباح والنقاش
elif st.session_state.step == 3:
    st.header("Step 3: شروق الشمس ☀️")
    st.error("أمر القائد: 'استيقظوا جميعاً.. حدثت جريمة!'")
    st.info(f"المكان الحقيقي كان: {SCENARIOS[st.session_state.current_scenario_key]['location']}")
    
    if st.button("انهاء الجولة 🔄"):
        st.session_state.step = 0
        st.session_state.game = {}
        st.rerun()
