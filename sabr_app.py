# =========================================================
# مشروع سَبْر (Sabr)
# المنظومة الصوتية والزمنية لتحليل التفسير القرآني
# =========================================================
# للتشغيل:
#   pip install streamlit numpy matplotlib pandas plotly
#   streamlit run sabr_app.py
# =========================================================

import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import plotly.graph_objects as go

# ------------------------------------------------------------------
# إعدادات الصفحة العامة
# ------------------------------------------------------------------
st.set_page_config(
    page_title="مشروع سَبْر | Sabr Project",
    page_icon="📜",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ------------------------------------------------------------------
# الألوان والهوية البصرية
# ------------------------------------------------------------------
NAVY = "#0B1F3A"        # كحلي داكن
NAVY_LIGHT = "#152C4E"
OFFWHITE = "#F6F1E7"    # أوف وايت
GOLD = "#C9A227"        # ذهبي
GOLD_LIGHT = "#E4C874"
TEXT_DARK = "#1C1C1C"

matplotlib.rcParams["axes.unicode_minus"] = False

# ------------------------------------------------------------------
# CSS عام: دعم RTL + الخطوط + التصميم الفخم
# ------------------------------------------------------------------
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&family=Tajawal:wght@300;400;500;700;900&display=swap');

html, body, [class*="css"] {{
    direction: rtl;
    text-align: right;
    font-family: 'Tajawal', sans-serif;
}}

.stApp {{
    background: linear-gradient(180deg, {NAVY} 0%, {NAVY_LIGHT} 100%);
    color: {OFFWHITE};
}}

section[data-testid="stSidebar"] {{
    background-color: {NAVY};
    border-left: 2px solid {GOLD};
}}

h1, h2, h3, h4 {{
    font-family: 'Tajawal', sans-serif;
    color: {GOLD_LIGHT} !important;
}}

.main-title {{
    text-align: center;
    font-size: 46px;
    font-weight: 900;
    color: {GOLD};
    letter-spacing: 1px;
    margin-bottom: 0px;
}}

.sub-title {{
    text-align: center;
    font-size: 18px;
    color: {OFFWHITE};
    opacity: 0.85;
    margin-top: 4px;
    margin-bottom: 25px;
}}

.gold-line {{
    height: 3px;
    background: linear-gradient(90deg, transparent, {GOLD}, transparent);
    margin: 10px 0 30px 0;
    border: none;
}}

.card {{
    background-color: {OFFWHITE};
    color: {TEXT_DARK};
    border-radius: 18px;
    padding: 25px 30px;
    box-shadow: 0 6px 20px rgba(0,0,0,0.35);
    border-top: 5px solid {GOLD};
    margin-bottom: 20px;
}}

.verse-box {{
    background: linear-gradient(135deg, {NAVY_LIGHT}, {NAVY});
    border: 1.5px solid {GOLD};
    border-radius: 20px;
    padding: 35px;
    text-align: center;
    margin-bottom: 20px;
}}

.verse-text {{
    font-family: 'Amiri', serif;
    font-size: 42px;
    color: {GOLD_LIGHT};
    line-height: 2.2;
}}

.badge {{
    display: inline-block;
    background-color: {GOLD};
    color: {NAVY};
    padding: 5px 16px;
    border-radius: 30px;
    font-weight: 700;
    font-size: 13px;
    margin-bottom: 10px;
}}

.section-header {{
    border-right: 5px solid {GOLD};
    padding-right: 12px;
    margin-top: 10px;
    margin-bottom: 15px;
}}

.bullet-item {{
    background-color: rgba(201,162,39,0.08);
    border-right: 3px solid {GOLD};
    padding: 10px 15px;
    border-radius: 8px;
    margin-bottom: 8px;
    color: {OFFWHITE};
}}

div[data-baseweb="tab-list"] {{
    justify-content: center;
}}
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------
# قاعدة البيانات التجريبية (Dummy Data) — 3 آيات تعكس التدرج
# ------------------------------------------------------------------
AYAT_DB = {
    "ayah_1": {
        "id": "ayah_1",
        "order": 1,
        "marhala": "المرحلة المكية — مرحلة الدعوة وبناء الصبر",
        "surah": "سورة المُزَّمِّل",
        "ayah_no": "الآية 10",
        "year_hint": "السنة الأولى من البعثة تقريبًا",
        "theme": "الصبر",
        "text": "وَاصْبِرْ عَلَىٰ مَا يَقُولُونَ وَاهْجُرْهُمْ هَجْرًا جَمِيلًا",
        "tafsir_source": "خلاصة من تفسير ابن كثير والسعدي",
        "tafsir_text": (
            "توجيه نبوي مبكر للنبي ﷺ بالصبر الجميل على أذى المشركين في قلوبهم "
            "دون جزع أو رد فعل انفعالي، مع الإعراض عنهم بأسلوب راقٍ لا يحمل "
            "ضغينة، وهذا يتناسب مع طبيعة المرحلة المكية التي كانت تقوم على "
            "بناء الأساس النفسي والإيماني للدعوة قبل مرحلة التشريع."
        ),
        "bulaghi_points": [
            "الفعل «اصبر» جاء بصيغة الأمر المباشر للتثبيت النفسي المبكر للنبي ﷺ.",
            "وصف الهجر بـ«الجميل» بلاغة نادرة تجمع بين الحزم واللين في آنٍ واحد.",
            "تكرار حرف الصاد والباء في الآية يعكس جرسًا صوتيًا يوحي بالثبات والتماسك.",
            "السياق المكي يفسر غياب التشريعات التفصيلية واقتصار الخطاب على التزكية.",
        ],
        "phonetic": {"شدة الألفاظ": 3, "المدود": 6, "الفواصل القرآنية": 4, "الغنة": 2, "التفخيم": 5},
        "tone_desc": "نبرة هادئة، إيقاع متأنٍّ يوحي بالسكينة والثبات الداخلي.",
    },
    "ayah_2": {
        "id": "ayah_2",
        "order": 2,
        "marhala": "المرحلة المدنية — مرحلة التشريع وبناء المجتمع",
        "surah": "سورة البقرة",
        "ayah_no": "الآية 183",
        "year_hint": "السنة الثانية للهجرة تقريبًا",
        "theme": "التشريع (الصيام)",
        "text": "يَا أَيُّهَا الَّذِينَ آمَنُوا كُتِبَ عَلَيْكُمُ الصِّيَامُ كَمَا كُتِبَ عَلَى الَّذِينَ مِنْ قَبْلِكُمْ لَعَلَّكُمْ تَتَّقُونَ",
        "tafsir_source": "خلاصة من تفسير السعدي وابن كثير",
        "tafsir_text": (
            "خطاب تشريعي مباشر لأهل الإيمان بعد استقرار الدولة في المدينة، "
            "يفرض الصيام بصيغة الإلزام «كُتِبَ»، ويربط العبادة بغايتها الكبرى "
            "وهي تحقيق التقوى، مستحضرًا أن هذا التكليف ليس بدعًا بل امتداد "
            "لسنن الأمم السابقة، مما يعكس نضج الخطاب التشريعي في هذه المرحلة."
        ),
        "bulaghi_points": [
            "النداء بـ«يا أيها الذين آمنوا» أسلوب مدني متكرر يواكب مرحلة بناء التشريع.",
            "صيغة المبني للمجهول «كُتِبَ» تفيد الحتم والإلزام دون تحديد قائل.",
            "الربط بالأمم السابقة يمنح التشريع بعدًا تاريخيًا يهدئ من وطأة التكليف الجديد.",
            "ختم الآية بـ«لعلكم تتقون» يحول الحكم الفقهي إلى غاية تربوية سامية.",
        ],
        "phonetic": {"شدة الألفاظ": 6, "المدود": 4, "الفواصل القرآنية": 7, "الغنة": 5, "التفخيم": 4},
        "tone_desc": "نبرة خطابية واضحة، إيقاع منتظم يناسب طابع التشريع والإلزام.",
    },
    "ayah_3": {
        "id": "ayah_3",
        "order": 3,
        "marhala": "أواخر المرحلة المدنية — مرحلة اكتمال الدين والنصر",
        "surah": "سورة النصر",
        "ayah_no": "الآيات 1-3",
        "year_hint": "قبيل وفاة النبي ﷺ (حجة الوداع)",
        "theme": "النصر",
        "text": "إِذَا جَاءَ نَصْرُ اللَّهِ وَالْفَتْحُ ۝ وَرَأَيْتَ النَّاسَ يَدْخُلُونَ فِي دِينِ اللَّهِ أَفْوَاجًا ۝ فَسَبِّحْ بِحَمْدِ رَبِّكَ وَاسْتَغْفِرْهُ ۚ إِنَّهُ كَانَ تَوَّابًا",
        "tafsir_source": "خلاصة من تفسير ابن كثير والسعدي",
        "tafsir_text": (
            "بشارة ختامية بتحقق النصر ودخول الناس في الإسلام أفواجًا بعد سنوات "
            "من الصبر والتشريع، ثم يأتي التوجيه الأخير بالتسبيح والاستغفار عوضًا "
            "عن الاحتفال الدنيوي، في إشارة لطيفة إلى اقتراب أجل الرسالة، وهذا "
            "يمثل ذروة التدرج من التأسيس إلى التشريع إلى الإنجاز والاكتمال."
        ),
        "bulaghi_points": [
            "كلمة «أفواجًا» تصور جماعية الدخول في الدين بعد أن كان الإسلام فرديًا في مكة.",
            "الجمع بين «التسبيح» و«الاستغفار» عند النصر إشارة بلاغية إلى تواضع الظفر لا الفخر به.",
            "«إنه كان توابًا» ختام يوحي بدورة كاملة تبدأ بالصبر المكي وتنتهي بالتوبة والاكتمال.",
            "الإيقاع السريع للآيات الثلاث يحاكي تدفق الأحداث وسرعة تحقق الوعد الإلهي.",
        ],
        "phonetic": {"شدة الألفاظ": 8, "المدود": 5, "الفواصل القرآنية": 6, "الغنة": 6, "التفخيم": 7},
        "tone_desc": "نبرة احتفالية مهيبة، إيقاع متصاعد ثم ينحدر نحو السكينة عند الاستغفار.",
    },
}

ORDERED_IDS = ["ayah_1", "ayah_2", "ayah_3"]

# ------------------------------------------------------------------
# حالة الجلسة (Session State)
# ------------------------------------------------------------------
if "selected_ayah" not in st.session_state:
    st.session_state.selected_ayah = "ayah_1"

# ------------------------------------------------------------------
# الرأس الرئيسي
# ------------------------------------------------------------------
st.markdown('<div class="main-title">📜 مشروع سَبْر (Sabr)</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-title">المنظومة الصوتية والزمنية لتحليل التفسير القرآني — '
    'دمج الخط الزمني لتدرج النزول مع المحلل الصوتي والبلاغي للآيات</div>',
    unsafe_allow_html=True,
)
st.markdown('<hr class="gold-line">', unsafe_allow_html=True)

# ------------------------------------------------------------------
# المكون 1: الخط الزمني التفاعلي للنزول
# ------------------------------------------------------------------
st.markdown('<div class="section-header"><h3>🕰️ الخط الزمني لتدرج النزول</h3></div>', unsafe_allow_html=True)

# رسم خط زمني تفاعلي بواسطة Plotly
fig_timeline = go.Figure()

x_vals = [ayat["order"] for ayat in AYAT_DB.values()]
y_vals = [0 for _ in x_vals]
labels = [f'{AYAT_DB[i]["surah"]} — {AYAT_DB[i]["theme"]}' for i in ORDERED_IDS]
colors = [GOLD if i == st.session_state.selected_ayah else "#5A6B8C" for i in ORDERED_IDS]
sizes = [34 if i == st.session_state.selected_ayah else 22 for i in ORDERED_IDS]

fig_timeline.add_trace(go.Scatter(
    x=[AYAT_DB[i]["order"] for i in ORDERED_IDS],
    y=[0, 0, 0],
    mode="lines",
    line=dict(color="#5A6B8C", width=3),
    hoverinfo="skip",
    showlegend=False,
))

fig_timeline.add_trace(go.Scatter(
    x=[AYAT_DB[i]["order"] for i in ORDERED_IDS],
    y=[0, 0, 0],
    mode="markers+text",
    marker=dict(size=sizes, color=colors, line=dict(width=2, color=OFFWHITE)),
    text=labels,
    textposition="top center",
    textfont=dict(color=OFFWHITE, size=13),
    hovertext=[AYAT_DB[i]["marhala"] for i in ORDERED_IDS],
    hoverinfo="text",
    showlegend=False,
))

fig_timeline.update_layout(
    height=180,
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    margin=dict(l=20, r=20, t=40, b=10),
    xaxis=dict(visible=False),
    yaxis=dict(visible=False, range=[-1, 1.5]),
)

st.plotly_chart(fig_timeline, use_container_width=True)

# أزرار اختيار الآية
cols = st.columns(3)
for idx, ayah_id in enumerate(ORDERED_IDS):
    ayah = AYAT_DB[ayah_id]
    with cols[idx]:
        btn_label = f'{ayah["surah"]} | {ayah["theme"]}\n({ayah["marhala"].split("—")[0].strip()})'
        if st.button(btn_label, key=f"btn_{ayah_id}", use_container_width=True):
            st.session_state.selected_ayah = ayah_id

st.markdown('<hr class="gold-line">', unsafe_allow_html=True)

# ------------------------------------------------------------------
# الآية المختارة حاليًا
# ------------------------------------------------------------------
current = AYAT_DB[st.session_state.selected_ayah]

st.markdown(f"""
<div class="verse-box">
    <div class="badge">{current['marhala']}</div>
    <div class="verse-text">{current['text']}</div>
    <p style="color:{OFFWHITE}; opacity:0.85; margin-top:10px;">
        {current['surah']} — {current['ayah_no']} &nbsp;|&nbsp; {current['year_hint']}
    </p>
</div>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------
# المكون 2: المحلل الصوتي والبلاغي
# ------------------------------------------------------------------
st.markdown('<div class="section-header"><h3>🎙️ المحلل الصوتي والبلاغي</h3></div>', unsafe_allow_html=True)

col_audio, col_wave = st.columns([1, 2])

with col_audio:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("**رفع أو تشغيل تسجيل صوتي للآية**")
    uploaded_audio = st.file_uploader(
        "اختر ملف صوتي (mp3 / wav)", type=["mp3", "wav", "ogg"], key=f"upl_{current['id']}"
    )
    if uploaded_audio is not None:
        st.audio(uploaded_audio)
        st.success("تم تحميل التسجيل بنجاح — جاري التحليل الصوتي.")
    else:
        st.info("لم يتم رفع ملف بعد — سيتم عرض تحليل توضيحي (Demo) للموجة الصوتية.")
    st.markdown(f"**وصف النبرة العامة:**")
    st.write(current["tone_desc"])
    st.markdown('</div>', unsafe_allow_html=True)

with col_wave:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("**الموجة الصوتية المرئية (Visual Waveform)**")

    # توليد موجة صوتية تجريبية (Demo) تعتمد على خصائص الآية المختارة
    seed = current["order"] * 17
    rng = np.random.default_rng(seed)
    t = np.linspace(0, 4, 800)
    base_freq = 2 + current["order"]
    wave = (
        np.sin(2 * np.pi * base_freq * t)
        * np.exp(-0.15 * t)
        + 0.3 * rng.normal(size=t.shape[0]) * 0.2
    )
    envelope = 1 + 0.4 * np.sin(0.6 * t + current["order"])
    wave = wave * envelope

    fig_wave, ax = plt.subplots(figsize=(8, 3))
    fig_wave.patch.set_facecolor(NAVY)
    ax.set_facecolor(NAVY)
    ax.plot(t, wave, color=GOLD, linewidth=1.4)
    ax.fill_between(t, wave, color=GOLD, alpha=0.15)
    ax.set_xlabel("الزمن (ثانية)", color=OFFWHITE)
    ax.set_ylabel("السعة الصوتية", color=OFFWHITE)
    ax.tick_params(colors=OFFWHITE)
    for spine in ax.spines.values():
        spine.set_color("#5A6B8C")
    ax.set_title(f"تمثيل توضيحي لموجة تلاوة: {current['surah']}", color=GOLD_LIGHT, fontsize=12)
    st.pyplot(fig_wave)
    st.caption("* رسم توضيحي تجريبي (Demo) لأغراض العرض، وليس تسجيلًا صوتيًا حقيقيًا.")
    st.markdown('</div>', unsafe_allow_html=True)

# تحليل بصري ونقاط الخصائص الصوتية
st.markdown("### 📊 تحليل الخصائص الصوتية والبلاغية")
phon = current["phonetic"]
df_phon = pd.DataFrame({"الخاصية": list(phon.keys()), "الدرجة": list(phon.values())})

col_chart, col_points = st.columns([1.3, 1])

with col_chart:
    fig_bar, ax2 = plt.subplots(figsize=(6, 3.5))
    fig_bar.patch.set_facecolor(NAVY)
    ax2.set_facecolor(NAVY)
    bars = ax2.barh(df_phon["الخاصية"], df_phon["الدرجة"], color=GOLD)
    ax2.invert_yaxis()
    ax2.set_xlim(0, 10)
    ax2.tick_params(colors=OFFWHITE, labelsize=11)
    for spine in ax2.spines.values():
        spine.set_color("#5A6B8C")
    ax2.set_xlabel("الدرجة من 10", color=OFFWHITE)
    st.pyplot(fig_bar)

with col_points:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("**ملاحظات صوتية سريعة:**")
    top_feature = max(phon, key=phon.get)
    st.markdown(f"""
    <div class="bullet-item">🔹 أبرز خاصية صوتية في هذه الآية: <b>{top_feature}</b> (بدرجة {phon[top_feature]}/10)</div>
    <div class="bullet-item">🔹 عدد الفواصل القرآنية المقدّرة: {phon['الفواصل القرآنية']}</div>
    <div class="bullet-item">🔹 مستوى المدود: {phon['المدود']}/10</div>
    <div class="bullet-item">🔹 مستوى التفخيم الصوتي: {phon['التفخيم']}/10</div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<hr class="gold-line">', unsafe_allow_html=True)

# ------------------------------------------------------------------
# المكون 3: بطاقة التفسير والسر البلاغي
# ------------------------------------------------------------------
st.markdown('<div class="section-header"><h3>📖 بطاقة التفسير والسر البلاغي</h3></div>', unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📚 التفسير التحليلي", "✨ السر البلاغي والتاريخي"])

with tab1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(f"**المصدر:** {current['tafsir_source']}")
    st.write(current["tafsir_text"])
    st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(f"**كيف ترتبط النبرة الصوتية بالمرحلة الزمنية والتفسير؟**")
    for point in current["bulaghi_points"]:
        st.markdown(f'<div class="bullet-item">✨ {point}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ------------------------------------------------------------------
# تذييل الصفحة
# ------------------------------------------------------------------
st.markdown('<hr class="gold-line">', unsafe_allow_html=True)
st.markdown(f"""
<p style="text-align:center; color:{OFFWHITE}; opacity:0.6; font-size:13px;">
مشروع سَبْر (Sabr) — مشروع تقني في مادة التفسير | المرحلة الثانوية
</p>
""", unsafe_allow_html=True)