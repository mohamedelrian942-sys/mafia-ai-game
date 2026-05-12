import streamlit as st
import random

# إعدادات واجهة الهاتف
st.set_page_config(page_title="مافيا عدنان - النسخة الإلكترونية", page_icon="🕵️")

# --- قاعدة بيانات الجرائم (يمكنك إضافة مئات القصص هنا) ---
CRIME_STORIES = [
    {
        "العنوان": "سرقة الموناليزا 🖼️",
        "المكان": "متحف اللوفر - ممر الفنون",
        "الأداة": "قاطع ليزر احترافي",
        "الشخصيات": ["حارس ليلي", "خبير ترميم", "سائح متخفي", "مديرة المتحف", "منظف كمرات"]
    },
    {
        "العنوان": "جريمة قطار الشرق 🚂",
        "المكان": "عربة الدرجة الأولى - الكابينة 4",
        "الأداة": "سم في فنجان القهوة",
        "الشخصيات": ["باشا غني", "طبيب القطار", "مضيفة غامضة", "عسكري متقاعد", "طباخ عربة الطعام"]
    },
    {
        "العنوان": "خيانة في معسكر المنتخب ⚽",
        "المكان": "غرفة تبديل الملابس - ملعب لوسيل",
        "الأداة": "تسريب خطة المباراة للمنافس",
        "الشخصيات": ["المدرب الفني", "حارس المرمى", "محلل الأداء", "رئيس الاتحاد", "صحفي متسلل"]
    }
]

# --- منطق التطبيق ---
st.title("🕵️ مافيا محمد عدنان x مافيوسو")
st.info("تطبيق الإدارة الذكي للعبة المافيا")

# 1. إعداد اللاعبين
st.subheader("1️⃣ تجهيز القائمة")
names_input = st.text_area("أدخل أسماء اللاعبين (اسم في كل سطر):", placeholder="محمد\nأحمد\nسارة...", height=150)
players = [n.strip() for n in names_input.split('\n') if n.strip()]

# 2. إعدادات اللعبة (ستايل مافيوسو)
st.sidebar.header("🛠️ إعدادات الجيم")
if st.sidebar.button("🔄 اختيار قصة عشوائية"):
    st.session_state.current_story = random.choice(CRIME_STORIES)

if "current_story" not in st.session_state:
    st.session_state.current_story = CRIME_STORIES[0]

story = st.session_state.current_story
st.sidebar.write(f"**القصة الحالية:** {story['العنوان']}")

# اختيار عدد المافيا (الذين لا يعرفون تفاصيل الجريمة)
mafia_count = st.sidebar.number_input("عدد المافيا", 1, 3, 1)

# 3. توزيع الأدوار (الدمج بين عدنان ومافيوسو)
if st.button("🚀 توزيع الأدوار والقصص"):
    if len(players) < 3:
        st.error("اللعبة تحتاج 3 لاعبين على الأقل!")
    else:
        # اختيار المافيا (برا السالفة)
        mafias = random.sample(players, mafia_count)
        # اختيار المحقق والطبيب (أدوار عدنان)
        others = [p for p in players if p not in mafias]
        detective = random.choice(others) if len(others) > 0 else None
        doctor = random.choice([p for p in others if p != detective]) if len(others) > 1 else None

        game_data = {}
        shuffled_roles = list(story['الشخصيات'])
        random.shuffle(shuffled_roles)

        for i, p in enumerate(players):
            role_type = "مواطن"
            if p in mafias: role_type = "مافيا (برا السالفة)"
            elif p == detective: role_type = "محقق (قناص)"
            elif p == doctor: role_type = "دكتور (إسعاف)"

            game_data[p] = {
                "نوع_الدور": role_type,
                "الشخصية": shuffled_roles[i % len(shuffled_roles)],
                "المكان": story['المكان'] if p not in mafias else "؟؟؟ (مجهول)",
                "الأداة": story['الأداة'] if p not in mafias else "؟؟؟ (مجهول)"
            }
        
        st.session_state.active_game = game_data
        st.success("تم التوزيع بنجاح! مرر الهاتف.")

# 4. مرحلة كشف الكروت السرية
if "active_game" in st.session_state:
    st.divider()
    current_p = st.selectbox("من أنت؟", ["اختر اسمك..."] + players)
    
    if current_p != "اختر اسمك...":
        with st.expander("انقر هنا لرؤية هويتك السرية 👁️"):
            data = st.session_state.active_game[current_p]
            st.warning(f"أنت تلعب بدور: **{data['الشخصية']}**")
            st.info(f"نوعك: **{data['نوع_الدور']}**")
            st.write(f"📍 مكان الجريمة: {data['المكان']}")
            st.write(f"🔪 أداة الجريمة: {data['الأداة']}")
            
            if "مافيا" in data['نوع_الدور']:
                st.error("تنبيه: أنت برا السالفة! حاول التمويه وادعاء معرفة المكان والأداة.")
            st.caption("أغلق المربع قبل تمرير الهاتف لللاعب التالي.")

# 5. لوحة تحكم المدير (محمد عدنان)
st.sidebar.divider()
if st.sidebar.checkbox("👀 كشف كل الأدوار (للمدير)"):
    if "active_game" in st.session_state:
        st.sidebar.json(st.session_state.active_game)
