import streamlit as st
import random

# --- إعدادات الصفحة ---
st.set_page_config(page_title="مافيا برو: الصناديق السرية", page_icon="🎁", layout="centered")

# --- تهيئة الحالة (Session State) ---
if "players_list" not in st.session_state:
    st.session_state.players_list = [""] 
if "step" not in st.session_state:
    st.session_state.step = 0

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

# --- تنسيق CSS للبطاقات والصناديق ---
st.markdown("""
    <style>
    .stButton>button { border-radius: 15px; font-weight: bold; }
    .player-box {
        background-color: #1E1E1E;
        padding: 20px;
        border-radius: 15px;
        border: 2px solid #3E3E3E;
        text-align: center;
        margin-bottom: 15px;
        color: white;
    }
    .role-reveal {
        background-color: #2D2D2D;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #FF4B4B;
        margin-top: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- المرحلة 0: إدخال اللاعبين ---
if st.session_state.step == 0:
    st.title("👥 تجهيز اللاعبين")
    for i in range(len(st.session_state.players_list)):
        col1, col2 = st.columns([4, 1])
        with col1:
            st.session_state.players_list[i] = st.text_input(f"اللاعب {i+1}", value=st.session_state.players_list[i], key=f"p_{i}")
        with col2:
            st.write(" ") 
            if st.button("❌", key=f"remove_{i}"):
                if len(st.session_state.players_list) > 1:
                    st.session_state.players_list.pop(i)
                    st.rerun()

    if st.button("➕ إضافة لاعب"):
        st.session_state.players_list.append("")
        st.rerun()

    st.divider()
    selected_key = st.selectbox("🎬 اختر السيناريو:", list(SCENARIOS.keys()))
    mafia_count = st.number_input("🤫 عدد المافيا:", 1, 3, 1)

    if st.button("🚀 توزيع الأدوار وبدء التحدي"):
        final_players = [name for name in st.session_state.players_list if name.strip()]
        if len(final_players) < 3:
            st.error("⚠️ نحتاج لـ 3 لاعبين على الأقل.")
        else:
            # منطق التوزيع (نفس المنطق السابق)
            mafias = random.sample(final_players, mafia_count)
            others = [p for p in final_players if p not in mafias]
            detective = random.choice(others) if others else None
            doctor = random.choice([p for p in others if p != detective]) if len(others) > 1 else None
            
            scenario = SCENARIOS[selected_key]
            shuffled_roles = list(scenario['roles'])
            random.shuffle(shuffled_roles)
            
            game_assignments = {}
            for i, p in enumerate(final_players):
                role_type = "مواطن صالِح"
                icon = "👤"
                if p in mafias: role_type, icon = "المافيا (برا السالفة)", "🤫"
                elif p == detective: role_type, icon = "المحقق (القناص)", "🔍"
                elif p == doctor: role_type, icon = "الطبيب (الإسعاف)", "🧪"
                
                game_assignments[p] = {
                    "role": role_type,
                    "icon": icon,
                    "character": shuffled_roles[i % len(shuffled_roles)],
                    "location": scenario['location'] if p not in mafias else "؟؟؟ (أنت برا السالفة)",
                    "weapon": scenario['weapon'] if p not in mafias else "؟؟؟"
                }
            
            st.session_state.game = game_assignments
            st.session_state.players_ready = final_players
            st.session_state.step = 1
            st.rerun()

# --- المرحلة 1: الصناديق السرية (كشف الهوية) ---
elif st.session_state.step == 1:
    st.title("🎁 الصناديق السرية")
    st.write("مرر الهاتف.. ليفتح كل لاعب صندوقه الخاص سراً!")
    
    for player in st.session_state.players_ready:
        with st.container():
            # تصميم الصندوق كبطاقة
            st.markdown(f'<div class="player-box"><h3>📦 صندوق: {player}</h3></div>', unsafe_allow_html=True)
            
            # زر الفتح تحت كل صندوق
            if st.checkbox(f"افتح صندوقك يا {player}", key=f"reveal_{player}"):
                data = st.session_state.game[player]
                st.markdown(f"""
                <div class="role-reveal">
                    <h4>{data['icon']} {data['role']}</h4>
                    <p>🎭 <b>الشخصية:</b> {data['character']}</p>
                    <p>📍 <b>المكان:</b> {data['location']}</p>
                    <p>🔪 <b>الأداة:</b> {data['weapon']}</p>
                </div>
                """, unsafe_allow_html=True)
                st.warning("⚠️ لا تنسَ إغلاق الصندوق (إلغاء الصح) قبل تمرير الهاتف!")
    
    st.divider()
    if st.button("الجميع عرف دوره؟ ابدأ الليل 🌙"):
        st.session_state.step = 2
        st.rerun()

# --- المرحلة 2: الليل (للمدير) ---
elif st.session_state.step == 2:
    st.title("🌙 مرحلة الليل")
    st.info("أنت الآن المدير.. اطلب من الجميع إغلاق أعينهم.")
    
    with st.expander("👁️ كشف الأدوار للمدير فقط"):
        for p, d in st.session_state.game.items():
            st.write(f"**{p}**: {d['role']} ({d['character']})")

    if st.button("حل الصباح ☀️"):
        st.session_state.step = 3
        st.rerun()

# --- المرحلة 3: الصباح ---
elif st.session_state.step == 3:
    st.title("☀️ شروق الشمس")
    st.error("حدثت جريمة! ابدأ النقاش والتحقيق.")
    if st.button("إنهاء الجولة والعودة للبداية 🔄"):
        st.session_state.step = 0
        st.rerun()
