import streamlit as st
import random

# --- إعدادات الصفحة الاحترافية ---
st.set_page_config(
    page_title="Mafia Pro | مافيا المحترفين",
    page_icon="🕵️",
    layout="centered"
)

# --- قاعدة بيانات السيناريوهات الاحترافية ---
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
    },
    "🎭 كواليس المسرح": {
        "location": "غرفة الماكياج - خلف الستار",
        "weapon": "سقوط ثريا / تبديل مسدس التمثيل",
        "roles": ["الممثل الرئيسي", "مخرجة العرض", "فني الإضاءة", "كاتب السيناريو", "عاملة الأزياء", "ملقن النصوص"]
    }
}

# --- تنسيق التصميم بـ CSS ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        background-color: #FF4B4B;
        color: white;
        font-weight: bold;
    }
    .player-card {
        padding: 20px;
        border-radius: 15px;
        background-color: #262730;
        border-left: 5px solid #FF4B4B;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- واجهة التطبيق ---
st.title("🕵️ مافيا المحترفين")
st.caption("الدمج المثالي بين نظام 'بيس كيك' وحماس 'محمد عدنان'")

# 1. قائمة اللاعبين
with st.expander("👥 إدارة اللاعبين", expanded=True):
    names_input = st.text_area("أدخل الأسماء (اسم في كل سطر):", height=120)
    players = [n.strip() for n in names_input.split('\n') if n.strip()]
    st.info(f"عدد اللاعبين الحالي: {len(players)}")

# 2. اختيار السيناريو
st.subheader("🎬 اختر السيناريو")
col1, col2 = st.columns([2, 1])
with col1:
    selected_key = st.selectbox("القصة:", list(SCENARIOS.keys()))
with col2:
    mafia_count = st.number_input("عدد المافيا:", 1, 3, 1)

# 3. توزيع الأدوار
if st.button("🚀 ابدأ الجولة الآن"):
    if len(players) < 3:
        st.error("⚠️ نحتاج لـ 3 لاعبين على الأقل.")
    else:
        # اختيار المافيا (برا السالفة)
        mafias = random.sample(players, mafia_count)
        others = [p for p in players if p not in mafias]
        
        # توزيع الأدوار الخاصة (عدنان)
        detective = random.choice(others) if others else None
        doctor = random.choice([p for p in others if p != detective]) if len(others) > 1 else None
        
        # تخصيص البيانات
        scenario = SCENARIOS[selected_key]
        shuffled_roles = list(scenario['roles'])
        random.shuffle(shuffled_roles)
        
        game_assignments = {}
        for i, p in enumerate(players):
            role_title = "مواطن صالِح"
            icon = "👤"
            if p in mafias:
                role_title, icon = "مافيا (برا السالفة)", "🤫"
            elif p == detective:
                role_title, icon = "المحقق (القناص)", "🔍"
            elif p == doctor:
                role_title, icon = "الطبيب (الإسعاف)", "🧪"
            
            game_assignments[p] = {
                "title": role_title,
                "icon": icon,
                "character": shuffled_roles[i % len(shuffled_roles)],
                "location": scenario['location'] if p not in mafias else "؟؟؟",
                "weapon": scenario['weapon'] if p not in mafias else "؟؟؟"
            }
        
        st.session_state.game = game_assignments
        st.session_state.game_on = True
        st.success("✅ تم التوزيع سرّياً! مرر الهاتف.")

# 4. كشف الهوية (UX محسن)
if "game" in st.session_state:
    st.divider()
    player_select = st.selectbox("من أنت؟", ["-- اختر اسمك --"] + players)
    
    if player_select != "-- اختر اسمك --":
        data = st.session_state.game[player_select]
        with st.expander(f"👁️ اضغط هنا يا {player_select}"):
            st.markdown(f"""
            <div class="player-card">
                <h3>{data['icon']} الدور: {data['title']}</h3>
                <p>🎭 <b>الشخصية:</b> {data['character']}</p>
                <hr>
                <p>📍 <b>المكان:</b> {data['location']}</p>
                <p>🔪 <b>الأداة:</b> {data['weapon']}</p>
            </div>
            """, unsafe_allow_html=True)
            if "مافيا" in data['title']:
                st.error("🔥 أنت برا السالفة! لا تنكشف.")
            st.caption("أغلق هذا المربع فوراً قبل تسليم الهاتف!")

# 5. لوحة تحكم القائد (المانيجر)
st.sidebar.title("🛠️ تحكم المانيجر")
if st.sidebar.checkbox("كشف قائمة الأدوار"):
    if "game" in st.session_state:
        for p, d in st.session_state.game.items():
            st.sidebar.write(f"{p}: {d['title']} ({d['character']})")

if st.sidebar.button("🗑️ إنهاء اللعبة"):
    st.session_state.clear()
    st.rerun()
