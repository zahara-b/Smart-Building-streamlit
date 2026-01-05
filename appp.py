# =============================================================================
# file: appp.py
# =============================================================================

import streamlit as st
from logicc import EnergyManager, Room, Building

# تنظیمات اولیه صفحه
st.set_page_config(
    page_title="سیستم خبره مدیریت ساختمان",
    page_icon="🏠",
    layout="wide"
)

# --- هدر اصلی ---
st.markdown("<h1 style='text-align: center; color: #4A90E2;'>🧠 سیستم خبره مدیریت هوشمند ساختمان (نسخه جامع)</h1>", unsafe_allow_html=True)
st.markdown("---")

# --- بخش تنظیمات کلی ساختمان در نوار کناری ---
with st.sidebar:
    st.image("https://www.gstatic.com/lamda/images/gemini_sparkle_v002_d4735339ff6186638136.gif", width=80)
    st.markdown("## 🌍 وضعیت کلی و محیط")
    
    # <<< بخش جدید: حالت‌های کاربری و پیش‌بینی‌ها >>>
    user_mode = st.selectbox("👤 حالت کاربری", ["normal", "guest", "party", "cleaning", "vacation", "away"])
    weather_forecast = st.selectbox("🌦️ پیش‌بینی آب و هوا", ["clear", "rain", "strong_wind"])
    day_type = st.radio("🗓️ نوع روز", ["weekday", "weekend"])

    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        is_peak_hours = st.checkbox("⚡️ اوج مصرف؟")
        is_sunny = st.checkbox("☀️ آفتابی؟")
    with col2:
        security_mode = st.radio("🛡️ امنیت", ["غیرفعال", "فعال"])

    time_period = st.select_slider("🕰️ بازه زمانی", ["morning", "day", "evening", "night", "late_night"])
    outside_temp = st.slider("🌡️ دمای بیرون (°C)", -10, 50, 18)
    
    with st.expander("🔬 تنظیمات پیشرفته دما و هشدارها"):
        desired_temp_range = st.slider("🎯 محدوده دمای مطلوب (°C)", 15.0, 30.0, (21.0, 25.0), 0.5)
        smoke_detector = st.checkbox("🔥 سنسور دود فعال؟")
        pollen_alert = st.checkbox("🌿 هشدار گرده؟")

# --- تعریف اتاق‌ها ---
rooms_config = [
    {"id": "living_room", "name": "🛋️ پذیرایی"}, {"id": "bedroom", "name": "🛏️ اتاق خواب"},
    {"id": "kitchen", "name": "🍳 آشپزخانه"}, {"id": "office", "name": "🖥️ اتاق کار"},
]
tabs = st.tabs([room["name"] for room in rooms_config])
room_inputs = {}

# --- ایجاد تب و ویجت‌ها برای هر اتاق ---
for i, room in enumerate(rooms_config):
    with tabs[i]:
        st.markdown(f"#### وضعیت سنسورهای اتاق **{room['name']}**")
        sub_col1, sub_col2, sub_col3 = st.columns(3)
        with sub_col1:
            presence = st.checkbox("👤 حضور", value=(room['id'] != 'office'), key=f"presence_{room['id']}")
            light_on = st.checkbox("💡 چراغ روشن", value=False, key=f"light_on_{room['id']}")
            tv_on = st.checkbox("📺 تلویزیون", key=f"tv_on_{room['id']}")
        with sub_col2:
            light_level = st.slider("☀️ شدت نور (lx)", 0, 1000, 450, key=f"light_level_{room['id']}")
            temp = st.slider("🌡️ دما (°C)", 10, 40, 24, key=f"temp_{room['id']}")
        with sub_col3:
            humidity = st.slider("💧 رطوبت (%)", 10, 90, 45, key=f"humidity_{room['id']}")
            blinds_status = st.select_slider("🖼️ پرده‌ها", ["closed", "half", "open"], value='half', key=f"blinds_{room['id']}")
            window_open = st.checkbox("🪟 پنجره باز", key=f"window_{room['id']}")
        
        clean_name = room['name'].split(" ")[1] if len(room['name'].split(" ")) > 1 else room['name']
        room_inputs[room['id']] = { "name": clean_name, "presence": presence, "light_level": light_level, "light_on": light_on, "temp": temp, "humidity": humidity, "tv_on": tv_on, "blinds_status": blinds_status, "window_open": window_open }

st.markdown("---")

if st.button("🚀 تحلیل کامل ساختمان و صدور فرمان", type="primary", key="analyze_button"):
    engine = EnergyManager()
    engine.reset()

    # ارسال تمام واقعیت‌های کلی به موتور خبره
    engine.declare(Building(
        peak_hours=is_peak_hours, time_period=time_period, is_sunny=is_sunny,
        security_mode="armed" if security_mode == "فعال" else "disarmed",
        smoke_detector=smoke_detector, pollen_alert=pollen_alert,
        desired_temp_min=desired_temp_range[0], desired_temp_max=desired_temp_range[1],
        outside_temp=outside_temp,
        user_mode=user_mode, weather_forecast=weather_forecast, day_type=day_type
    ))

    # ارسال واقعیت‌های هر اتاق
    for room_id, inputs in room_inputs.items():
        engine.declare(Room(**inputs))

    engine.run()

    with st.expander("📄 مشاهده نتایج تحلیل سیستم خبره", expanded=True):
        if engine.actions:
            st.success("فرمان‌های زیر (به ترتیب اولویت) برای مدیریت ساختمان صادر شد:")
            for action in engine.actions:
                st.markdown(f"- {action}")
        else:
            st.info("✅ وضعیت تمام اتاق‌ها پایدار است و نیازی به تغییر نیست.")