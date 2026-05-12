import streamlit as st
import random

# --- إعدادات الصفحة ---
st.set_page_config(page_title="مدير مافيا الاحترافي", page_icon="🎙️", layout="centered")

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
    }
}

# --- واجهة التطبيق ---
st.title("🎙️ مدير جولة المافيا")
st.caption("أنت القائد.. والتطبيق يعطيك الأوامر")

# 1. إدخال اللاعبين
names_input = st.sidebar.text_area("👤 أسماء اللاعبين (كل اسم في سطر):", height=150)
players = [n.strip() for n in names_input.split('\n') if n.strip()]

# 2. اختيار السيناريو وعدد المافيا
selected_key = st.sidebar.selectbox("🎬 اختر السيناريو:", list(SCENARIOS.keys()))
mafia_count = st.sidebar.number_input("🤫 عدد المافيا:", 1, 3, 1)

# 3. زر بدء الجولة
if st.sidebar.button("🚀 بدء جولة جديدة"):
    if len(players) < 4:
        st.error("⚠️ تحتاج 4 لاعبين على الأقل للعب بنظام الأوامر.")
    else:
        # التوزيع
        mafias = random.sample(players, mafia_count)
        others = [p for p in players if p not in mafias]
        detective = random.choice(others)
        doctor = random.choice([p for p in others if p != detective])
        
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
        st.session_state.step = 1 # نبدأ بالخطوة الأولى
        st.success("✅ تم التوزيع! اتبع الأوامر بالأسفل.")

# --- نظام إدارة الأوامر (بعد بدء اللعبة) ---
if "game" in st.session_state:
    st.divider()
    
    # بطاقات توزيع الأدوار (مرحلة الكشف)
    if st.session_state.step == 1:
        st.header("Step 1: كشف الأدوار 👁️")
        st.info("مرر الهاتف لكل لاعب ليفتح الصندوق الخاص به ويحفظ دوره سراً.")
        
        player_select = st.selectbox("من أنت؟", ["-- اختر --"] + list(st.session_state.game.keys()))
        if player_select != "-- اختر --":
            data = st.session_state.game[player_select]
            with st.expander("انقر لرؤية هويتك"):
                st.write(f"🎭 شخصيتك: **{data['character']}**")
                st.write(f"💼 دورك السري: **{data['role']}**")
                st.write(f"📍 السالفة: {data['location']}")
                st.caption("أغلق المربع فوراً!")
        
        if st.button("انتهى الجميع؟ انتقل لليل 🌙"):
            st.session_state.step = 2
            st.rerun()

    # مرحلة الليل
    elif st.session_state.step == 2:
        st.header("Step 2: مرحلة الليل 🌙")
        st.warning("أمر القائد: 'يا أهل المدينة.. ناموا جميعاً وأغلقوا أعينكم!'")
        
        with st.expander("1️⃣ استدعاء المافيا (اضغط هنا للمتابعة)"):
            st.write("أمر القائد: 'يا مافيا استيقظوا.. اختاروا ضحيتكم بصمت'.")
            st.write(f"المافيا هم: **{', '.join([p for p, d in st.session_state.game.items() if d['role'] == 'مافيا'])}**")
        
        with st.expander("2️⃣ استدعاء الطبيب"):
            st.write("أمر القائد: 'يا دكتور استيقظ.. اختر شخصاً لتعالجه'.")
            st.write(f"الطبيب هو: **{', '.join([p for p, d in st.session_state.game.items() if d['role'] == 'طبيب'])}**")

        with st.expander("3️⃣ استدعاء المحقق"):
            st.write("أمر القائد: 'يا محقق استيقظ.. اختر شخصاً لتكشف هويته'.")
            st.write(f"المحقق هو: **{', '.join([p for p, d in st.session_state.game.items() if d['role'] == 'محقق'])}**")

        if st.button("حل الصباح؟ ابدأ النقاش ☀️"):
            st.session_state.step = 3
            st.rerun()

    # مرحلة النهار والنقاش
    elif st.session_state.step == 3:
        st.header("Step 3: شروق الشمس والنقاش ☀️")
        st.error("أمر القائد: 'استيقظوا جميعاً.. حدثت جريمة!'")
        st.markdown(f"""
        **قواعد النقاش الآن:**
        1. كل شخص يتحدث بناءً على شخصيته (مثلاً الجراح يتحدث بأسلوب طبي).
        2. ابدأوا بسؤال بعضكم عن تفاصيل **{SCENARIOS[selected_key]['location']}**.
        3. المافيا سيحاولون التظاهر بأنهم يعرفون المكان!
        """)
        
        if st.button("بدء التصويت النهائي 🗳️"):
            st.session_state.step = 4
            st.rerun()

    # مرحلة التصويت
    elif st.session_state.step == 4:
        st.header("Step 4: المحاكمة والتصويت ⚖️")
        st.write("أمر القائد: 'حان وقت العدالة.. صوتوا على الشخص المشبوه فيه'.")
        st.info("إذا تم كشف المافيا فاز الصالحون، وإذا عرف المافيا 'السالفة' فاز المافيا!")
        
        if st.button("إنهاء الجولة والعودة للرئيسية 🔄"):
            st.session_state.clear()
            st.rerun()

# تخصيص المظهر
st.markdown("<style>button {border-radius: 20px !important;}</style>", unsafe_allow_html=True)
