# =============================================================================
# file: logicc.py
# =============================================================================

from experta import *

class Room(Fact):
    pass
class Building(Fact):
    pass

class EnergyManager(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.actions = []
    def reset(self):
        super().reset()
        self.actions = []

    # =========================================================================
    # دسته ۱: قوانین حیاتی و امنیتی (۵ قانون)
    # =========================================================================
    @Rule(Building(security_mode='armed'), Room(presence=True), salience=100)
    def rule_01_security_breach(self):
        self.actions.append("🛡️ !!! هشدار امنیتی: حضور فرد در حالت مسلح شناسایی شد !!!")

    @Rule(Building(smoke_detector=True), salience=99)
    def rule_02_smoke_alert(self):
        self.actions.append("🔥 !!! خطر آتش‌سوزی: دود شناسایی شد! سیستم تهویه خاموش و اطلاع‌رسانی انجام شد !!!")

    @Rule(Room(name=MATCH.name, window_open=True), Building(security_mode='armed'), salience=95)
    def rule_03_window_security_alert(self, name):
        self.actions.append(f"🛡️ هشدار امنیتی: پنجره اتاق '{name}' در حالت مسلح باز است.")
        
    @Rule(Building(time_period='late_night'), NOT(Room(presence=True)), salience=10)
    def rule_04_auto_security_arm(self):
        self.actions.append("🌙 اتوماسیون کلی: ساختمان خالی و زمان آخر شب است. حالت امنیتی به صورت خودکار فعال شد.")

    @Rule(Building(user_mode='vacation'), salience=98)
    def rule_05_vacation_security(self):
        self.actions.append("🛡️ حالت مسافرت: امنیت در بالاترین سطح قرار گرفت و هشدارهای حساس فعال شدند.")
        
    # =========================================================================
    # دسته ۲: قوانین صرفه‌جویی حداکثری در انرژی (۱۰ قانون)
    # =========================================================================
    @Rule(Room(name=MATCH.name, window_open=True, temp=MATCH.t), salience=80)
    def rule_06_hvac_window_conflict(self, name, t):
        if t > 26 or t < 20:
            self.actions.append(f"💸 اتلاف انرژی در '{name}': پنجره باز است در حالی که سرمایش/گرمایش فعال است!")
    
    @Rule(AS.building<<Building(desired_temp_max=MATCH.max_t, outside_temp=MATCH.out_t), AS.room<<Room(presence=True, temp=MATCH.t, window_open=False),
           TEST(lambda t, max_t, out_t: t > max_t and out_t < max_t - 2), salience=71)
    def rule_07_free_cooling(self, room):
        self.actions.append(f"🌬️ صرفه‌جویی در '{room['name']}': اتاق گرم و هوای بیرون خنک است. پنجره برای تهویه طبیعی باز شود.")

    @Rule(Building(peak_hours=True), Room(name=MATCH.name, presence=False), salience=75)
    def rule_08_peak_hours_empty_room_shutdown(self, name):
        self.actions.append(f"⚡ اوج مصرف در اتاق خالی '{name}': تمام سیستم‌های غیرضروری خاموش شدند.")

    @Rule(AS.building << Building(is_sunny=True, desired_temp_min=MATCH.min_t), AS.room << Room(blinds_status='closed', temp=MATCH.t), TEST(lambda t, min_t: t < min_t), salience=70)
    def rule_09_solar_gain_heating(self, room):
        self.actions.append(f"☀️ صرفه‌جویی در '{room['name']}': اتاق سرد و بیرون آفتابی است. پرده‌ها برای گرمایش طبیعی باز شدند.")

    @Rule(AS.building << Building(is_sunny=True, desired_temp_max=MATCH.max_t), AS.room << Room(blinds_status='open', temp=MATCH.t), TEST(lambda t, max_t: t > max_t), salience=70)
    def rule_10_solar_gain_cooling(self, room):
        self.actions.append(f"☀️ صرفه‌جویی در '{room['name']}': اتاق گرم و بیرون آفتابی است. پرده‌ها برای جلوگیری از گرمای اضافه بسته شدند.")

    @Rule(Building(peak_hours=True, appliance_running='dishwasher'), salience=76)
    def rule_11_peak_hours_dishwasher(self):
        self.actions.append("⚡ صرفه‌جویی: ماشین ظرفشویی در ساعات اوج مصرف روشن است. پیشنهاد می‌شود به تعویق بیفتد.")
        
    @Rule(Building(user_mode='vacation'), salience=79)
    def rule_12_vacation_energy_saving(self):
        self.actions.append("💸 حالت مسافرت: ترموستات در حالت صرفه‌جویی حداکثری قرار گرفت و لوازم غیرضروری خاموش شدند.")

    @Rule(Room(name=MATCH.name, presence=False, light_on=True), salience=29)
    def rule_13_auto_lights_off(self, name):
        self.actions.append(f"💡 اتوماسیون در '{name}': کسی حضور ندارد، چراغ خاموش شد.")

    @Rule(Room(name=MATCH.name, presence=False, tv_on=True), salience=28)
    def rule_14_auto_tv_off(self, name):
        self.actions.append(f"📺 اتوماسیون در '{name}': کسی حضور ندارد، تلویزیون خاموش شد.")
        
    @Rule(Building(peak_hours=False, time_period='late_night'), salience=1)
    def rule_15_suggest_off_peak_appliance_use(self):
        self.actions.append("🔋 پیشنهاد: اکنون زمان مناسبی (خارج از اوج مصرف) برای استفاده از لوازم پرمصرف مانند ماشین لباسشویی است.")

    # =========================================================================
    # دسته ۳: قوانین سلامتی و کیفیت محیط (۱۰ قانون)
    # =========================================================================
    @Rule(Room(name=MATCH.name, presence=MATCH.p, humidity=MATCH.h), salience=55)
    def rule_16_high_humidity_alert(self, name, p, h):
        if p is True and h > 65:
            self.actions.append(f"💧 سلامتی در '{name}': رطوبت بالاست. حالت رطوبت‌زدایی فعال شد.")
    
    @Rule(Building(pollen_alert=True), salience=51)
    def rule_17_general_pollen_warning(self):
        self.actions.append("🌿 هشدار سلامتی: سطح گرده در هوای بیرون بالاست. توصیه می‌شود پنجره‌ها بسته بمانند.")

    @Rule(Building(pollen_alert=True), Room(window_open=True, name=MATCH.name), salience=50)
    def rule_18_pollen_window_conflict(self, name):
        self.actions.append(f"🌿 ریسک سلامتی در '{name}': با وجود هشدار گرده، پنجره باز است! پنجره بسته شود.")
        
    @Rule(Room(name=MATCH.name, presence=True, humidity__lt=30), Building(outside_temp__lt=10), salience=54)
    def rule_19_low_humidity_winter(self, name):
        self.actions.append(f"💧 سلامتی در '{name}': هوا خشک است. پیشنهاد می‌شود دستگاه بخور سرد روشن شود.")
        
    @Rule(Building(weather_forecast='rain'), Room(window_open=True, name=MATCH.name), salience=65)
    def rule_20_rain_forecast_close_window(self, name):
        self.actions.append(f"🌧️ هشدار هواشناسی در '{name}': پیش‌بینی بارندگی! پنجره‌ها بسته شوند.")

    @Rule(Building(weather_forecast='strong_wind'), Room(window_open=True, name=MATCH.name), salience=66)
    def rule_21_wind_forecast_blinds(self, name):
        self.actions.append(f"🌬️ هشدار هواشناسی در '{name}': پیش‌بینی باد شدید! پرده‌ها برای محافظت بسته شوند.")
        
    @Rule(Room(light_level__gt=800, blinds_status='open', name=MATCH.name), Building(time_period='day'), salience=15)
    def rule_22_glare_reduction(self, name):
        self.actions.append(f"🕶️ راحتی در '{name}': نور مستقیم خورشید شدید است. پرده‌ها برای کاهش درخشندگی کمی بسته شدند.")
        
    @Rule(Room(name=MATCH.name, temp=MATCH.t), TEST(lambda t: t > 35), salience=90)
    def rule_23_extreme_heat_alert(self, name):
        self.actions.append(f"🌡️ هشدار سلامتی در '{name}': دمای اتاق بسیار بالاست! وضعیت سیستم سرمایش بررسی شود.")
        
    @Rule(Room(name=MATCH.name, temp=MATCH.t), TEST(lambda t: t < 15), salience=90)
    def rule_24_extreme_cold_alert(self, name):
        self.actions.append(f"🌡️ هشدار سلامتی در '{name}': دمای اتاق بسیار پایین است! وضعیت سیستم گرمایش بررسی شود.")
        
    @Rule(Building(user_mode='guest'), Room(name='پذیرایی', temp=MATCH.t), TEST(lambda t: t < 22 or t > 24), salience=45)
    def rule_25_guest_mode_comfort(self, t):
        self.actions.append("👥 حالت مهمان: دمای پذیرایی برای راحتی حداکثری مهمانان در حال تنظیم است.")

    # =========================================================================
    # دسته ۴: قوانین راحتی و اتوماسیون (۲۵ قانون)
    # =========================================================================
    @Rule(Building(time_period='morning', day_type='weekday'), Room(name='خواب', presence=True, blinds_status='closed'), salience=40)
    def rule_26_weekday_morning_wakeup(self):
        self.actions.append("☀️ راحتی در اتاق خواب: صبح بخیر! پرده‌ها برای بیداری طبیعی باز شدند.")
        
    @Rule(Building(time_period='morning', day_type='weekend'), Room(name='خواب', presence=True, blinds_status='closed'), salience=40)
    def rule_27_weekend_morning_wakeup(self):
        self.actions.append("☀️ راحتی در اتاق خواب: آخر هفته خوبی داشته باشید! پرده‌ها کمی دیرتر باز می‌شوند.")

    @Rule(Building(time_period='night'), Room(name='پذیرایی', tv_on=True, light_on=True), salience=35)
    def rule_28_movie_mode_livingroom(self):
        self.actions.append("🎬 راحتی در پذیرایی: حالت تماشای فیلم فعال شد. چراغ‌ها کم‌نور شدند.")
    
    @Rule(Room(name=MATCH.name, presence=MATCH.p, light_level=MATCH.ll, light_on=MATCH.lo), salience=30)
    def rule_29_auto_lights_on(self, name, p, ll, lo):
        if p is True and ll < 300 and lo is False:
            self.actions.append(f"💡 اتوماسیون در '{name}': نور کم است، چراغ روشن شد.")
    
    @Rule(AS.building << Building(desired_temp_min=MATCH.min_t, outside_temp=MATCH.out_t), AS.room << Room(presence=True, temp=MATCH.t),
           TEST(lambda t, min_t, out_t: t < min_t and out_t < min_t + 5), salience=25)
    def rule_30_intelligent_heating(self, room):
        if room['window_open']:
             self.actions.append(f"🔥 اتوماسیون در '{room['name']}': هوا سرد است. ابتدا پنجره بسته و سپس گرمایش فعال شد.")
        else:
             self.actions.append(f"🔥 اتوماسیون در '{room['name']}': دما پایین است، گرمایش برای رسیدن به دمای مطلوب فعال شد.")

    @Rule(AS.building << Building(desired_temp_max=MATCH.max_t, outside_temp=MATCH.out_t), AS.room << Room(presence=True, temp=MATCH.t), 
          TEST(lambda t, max_t, out_t: t > max_t and out_t >= max_t - 2), salience=20)
    def rule_31_mechanical_cooling(self, room):
        self.actions.append(f"❄️ اتوماسیون در '{room['name']}': دما بالاست و بیرون گرم است. سرمایش (کولر) فعال شد.")
    
    @Rule(Room(name='آشپزخانه', presence=True), Building(time_period='morning'), salience=18)
    def rule_32_kitchen_morning_lights(self):
        self.actions.append("☕ اتوماسیون در آشپزخانه: چراغ‌های زیر کابینتی برای تهیه صبحانه روشن شدند.")
        
    @Rule(Room(name='خواب', presence=False), Building(time_period='day'), salience=17)
    def rule_33_bedroom_day_blinds(self):
        self.actions.append("☀️ اتوماسیون در اتاق خواب: پرده‌ها برای ورود نور در طول روز باز هستند.")
        
    @Rule(Building(time_period='evening'), Room(presence=True, name=MATCH.name), salience=16)
    def rule_34_evening_ambiance(self, name):
        self.actions.append(f"🌆 راحتی در '{name}': حالت نورپردازی عصرگاهی فعال شد.")
        
    @Rule(Room(name='کار', presence=True), salience=19)
    def rule_35_office_focus_mode(self):
        self.actions.append("🖥️ راحتی در اتاق کار: نورپردازی مناسب برای تمرکز فعال شد.")

    @Rule(Room(name=MATCH.name, presence=False, tv_on=False, light_on=False), salience=2)
    def rule_36_empty_room_stable(self, name):
        self.actions.append(f"✅ وضعیت در '{name}': اتاق خالی و سیستم‌ها در حالت آماده به کار هستند.")

    @Rule(Building(time_period='late_night'), Room(presence=True, name=MATCH.name), salience=15)
    def rule_37_late_night_light(self, name):
        self.actions.append(f"🌙 راحتی در '{name}': نور شب (حداقل روشنایی) فعال شد.")

    @Rule(Building(user_mode='party'), Room(name='پذیرایی'), salience=46)
    def rule_38_party_mode(self):
        self.actions.append("🎉 حالت مهمانی: سیستم تهویه مطبوع پذیرایی برای جمعیت بیشتر تقویت شد.")
        
    @Rule(Room(name='آشپزخانه', presence=False), salience=5)
    def rule_39_kitchen_empty_check(self):
        self.actions.append("🍳 بررسی آشپزخانه: اطمینان از خاموش بودن لوازم خانگی پس از خروج.")
        
    @Rule(Building(time_period='night'), Room(name='خواب', presence=True), salience=36)
    def rule_40_bedroom_night_mode(self):
        self.actions.append("😴 راحتی در اتاق خواب: حالت خواب فعال شد، دما کمی خنک‌تر تنظیم شد.")

    @Rule(Room(name='کار', presence=False), salience=4)
    def rule_41_office_empty_shutdown(self):
        self.actions.append("🖥️ اتوماسیون در اتاق کار: سیستم‌ها و مانیتورها خاموش شدند.")
        
    @Rule(Building(outside_temp__lt=0), salience=91)
    def rule_42_freeze_warning(self):
        self.actions.append("❄️ هشدار یخ‌زدگی: دمای بیرون زیر صفر است، وضعیت لوله‌ها بررسی شود.")
        
    @Rule(Room(name='پذیرایی', presence=True), salience=3)
    def rule_43_living_room_welcome(self):
        self.actions.append("🏡 خوش‌آمدگویی: حالت روشنایی ورودی برای پذیرایی فعال شد.")

    @Rule(Building(time_period='evening'), Room(blinds_status='open'), salience=14)
    def rule_44_evening_privacy(self):
        self.actions.append("🔒 راحتی: با غروب آفتاب، پرده‌ها برای حفظ حریم خصوصی بسته شدند.")
        
    @Rule(Building(user_mode='cleaning'), salience=47)
    def rule_45_cleaning_mode(self):
        self.actions.append("🧹 حالت نظافت: تمام چراغ‌ها روی حداکثر روشنایی و پرده‌ها کاملاً باز شدند.")
        
    @Rule(Room(name='خواب', light_level__lt=50, presence=True), Building(time_period='day'), salience=13)
    def rule_46_bedroom_dark_day(self):
        self.actions.append("💡 پیشنهاد در اتاق خواب: اتاق در طول روز تاریک است، پرده‌ها باز شوند؟")
        
    @Rule(Building(time_period__in=['evening', 'night']), Room(name='آشپزخانه', presence=True), salience=12)
    def rule_47_kitchen_evening_task_light(self):
        self.actions.append("💡 اتوماسیون در آشپزخانه: نورپردازی موضعی برای کار فعال شد.")
        
    @Rule(Room(name='پذیرایی', presence=False), Building(user_mode='away'), salience=78)
    def rule_48_away_mode_livingroom_temp(self):
        self.actions.append("🌡️ حالت بیرون از خانه: دمای پذیرایی در حالت اقتصادی تنظیم شد.")
        
    @Rule(Building(time_period='day', is_sunny=False), Room(name=MATCH.name, presence=True, light_level__lt=400), salience=11)
    def rule_49_cloudy_day_lights(self, name):
        self.actions.append(f"☁️ راحتی در '{name}': به دلیل ابری بودن هوا، نور مکمل فعال شد.")
        
    @Rule(Building(pollen_alert=False, outside_temp__gt=18, outside_temp__lt=25), Room(presence=True, name=MATCH.name), salience=6)
    def rule_50_suggest_fresh_air(self, name):
        self.actions.append(f"🍃 پیشنهاد در '{name}': هوای بیرون مطبوع است! برای تهویه طبیعی پنجره را باز کنید.")

    