import re
import sys
import py_compile

RR_CSS = """# Custom Styling (Rajasthan Royals Signature Palette: Royal Pink #EA1A85, Deep Navy #0B132B, Imperial Gold #D4AF37)
st.markdown(\"\"\"
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700;800;900&family=Montserrat:wght@400;500;600;700;800&family=Rajdhani:wght@600;700;800&display=swap');

    /* Global Rajasthan Royals Theme Variables */
    :root {
        --rr-pink: #EA1A85;
        --rr-pink-hover: #FF4D9E;
        --rr-pink-glow: rgba(234, 26, 133, 0.4);
        --rr-navy-deep: #0B132B;
        --rr-navy-card: #131E3D;
        --rr-navy-surface: #182447;
        --rr-gold: #D4AF37;
        --rr-gold-light: #FFD700;
        --rr-gold-glow: rgba(212, 175, 55, 0.4);
        --rr-text: #F8FAFC;
    }

    /* Background and Base */
    .stApp {
        background: radial-gradient(circle at 15% 15%, #182447 0%, #0B132B 60%, #060B18 100%) !important;
        color: #F8FAFC !important;
        font-family: 'Montserrat', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }

    /* Top Headings with Royal Pink & Imperial Gold Gradient */
    h1, .rr-title {
        font-family: 'Rajdhani', sans-serif !important;
        font-weight: 800 !important;
        text-transform: uppercase !important;
        letter-spacing: 1.5px !important;
        background: linear-gradient(135deg, #FFFFFF 15%, #EA1A85 65%, #D4AF37 100%) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        margin-top: 0.1rem !important;
        margin-bottom: 0.4rem !important;
        filter: drop-shadow(0 2px 10px rgba(234, 26, 133, 0.35));
    }

    h2, h3 {
        font-family: 'Rajdhani', sans-serif !important;
        font-weight: 700 !important;
        color: #D4AF37 !important;
        letter-spacing: 1px !important;
        text-transform: uppercase !important;
    }

    h4, h5 {
        font-family: 'Montserrat', sans-serif !important;
        color: #CBD5E1 !important;
        font-weight: 600 !important;
    }

    /* Rajasthan Royals Jaipur Heritage Hero Banner */
    .rr-heritage-banner {
        background: linear-gradient(135deg, rgba(234, 26, 133, 0.2) 0%, rgba(19, 30, 61, 0.95) 45%, rgba(212, 175, 55, 0.18) 100%);
        border: 1px solid rgba(212, 175, 55, 0.38);
        border-top: 4px solid #EA1A85;
        border-bottom: 2px solid #D4AF37;
        border-radius: 14px;
        padding: 22px 28px;
        margin-bottom: 24px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5), inset 0 0 35px rgba(234, 26, 133, 0.1);
        position: relative;
        overflow: hidden;
    }
    
    .rr-heritage-banner::after {
        content: "👑 HALLA BOL";
        position: absolute;
        right: 20px;
        bottom: 8px;
        font-family: 'Cinzel', serif;
        font-weight: 900;
        font-size: 2.8rem;
        color: rgba(212, 175, 55, 0.08);
        letter-spacing: 4px;
        pointer-events: none;
    }

    /* Metric Cards with Imperial Gold Border & Royal Pink Value */
    .metric-box {
        background: linear-gradient(145deg, #182447 0%, #0F172A 100%);
        border: 1px solid rgba(212, 175, 55, 0.35);
        border-top: 3px solid #EA1A85;
        border-radius: 14px;
        padding: 18px 12px;
        text-align: center;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(212, 175, 55, 0.3);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .metric-box:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 28px rgba(234, 26, 133, 0.3), inset 0 1px 0 rgba(212, 175, 55, 0.7);
        border-color: #EA1A85;
    }
    .metric-value {
        font-family: 'Rajdhani', sans-serif;
        font-size: 2.3rem;
        font-weight: 800;
        color: #EA1A85;
        text-shadow: 0 0 16px rgba(234, 26, 133, 0.4);
        line-height: 1.1;
    }
    .metric-label {
        font-family: 'Montserrat', sans-serif;
        font-size: 0.76rem;
        text-transform: uppercase;
        color: #D4AF37;
        font-weight: 700;
        letter-spacing: 1.5px;
        margin-top: 6px;
    }

    /* RR Cards with Jharokha Left Border Accent */
    .rr-card {
        background: linear-gradient(135deg, rgba(19, 30, 61, 0.9) 0%, rgba(11, 19, 43, 0.95) 100%);
        border: 1px solid rgba(212, 175, 55, 0.3);
        border-left: 6px solid #EA1A85;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.45);
        backdrop-filter: blur(10px);
    }

    /* RR Badges */
    .rr-badge {
        background: linear-gradient(135deg, rgba(234, 26, 133, 0.22) 0%, rgba(234, 26, 133, 0.08) 100%);
        color: #FF70A6;
        padding: 5px 12px;
        border-radius: 6px;
        font-size: 0.8rem;
        font-weight: 700;
        border: 1px solid rgba(234, 26, 133, 0.5);
        display: inline-block;
        letter-spacing: 0.5px;
    }
    .rr-badge-gold {
        background: linear-gradient(135deg, rgba(212, 175, 55, 0.22) 0%, rgba(212, 175, 55, 0.08) 100%);
        color: #FFD700;
        padding: 5px 12px;
        border-radius: 6px;
        font-size: 0.8rem;
        font-weight: 700;
        border: 1px solid rgba(212, 175, 55, 0.55);
        display: inline-block;
        letter-spacing: 0.5px;
    }
    .rr-badge-blue {
        background: linear-gradient(135deg, rgba(28, 37, 65, 0.8) 0%, rgba(11, 19, 43, 0.9) 100%);
        color: #38BDF8;
        padding: 5px 12px;
        border-radius: 6px;
        font-size: 0.8rem;
        font-weight: 700;
        border: 1px solid rgba(56, 189, 248, 0.4);
        display: inline-block;
        letter-spacing: 0.5px;
    }
    .rr-hallabol {
        background: linear-gradient(135deg, #EA1A85 0%, #C2136E 50%, #D4AF37 100%);
        color: #FFFFFF;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 0.82rem;
        font-weight: 800;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        display: inline-block;
        box-shadow: 0 4px 15px rgba(234, 26, 133, 0.4);
    }

    /* Sidebar Theme */
    section[data-testid="stSidebar"] {
        background-color: #070D1E !important;
        border-right: 1px solid rgba(212, 175, 55, 0.25) !important;
    }
    section[data-testid="stSidebar"] .stRadio label {
        color: #CBD5E1 !important;
        font-family: 'Montserrat', sans-serif !important;
        font-size: 0.9rem !important;
        padding: 6px 10px !important;
        border-radius: 6px !important;
        transition: all 0.2s ease !important;
    }
    section[data-testid="stSidebar"] .stRadio label:hover {
        background: rgba(234, 26, 133, 0.12) !important;
        color: #EA1A85 !important;
    }

    /* Custom Streamlit Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #EA1A85 0%, #C2136E 60%, #D4AF37 100%) !important;
        color: #FFFFFF !important;
        font-family: 'Montserrat', sans-serif !important;
        font-weight: 700 !important;
        font-size: 0.9rem !important;
        border: 1px solid rgba(212, 175, 55, 0.5) !important;
        border-radius: 8px !important;
        padding: 0.6rem 1.4rem !important;
        box-shadow: 0 4px 18px rgba(234, 26, 133, 0.35) !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        transition: all 0.25s ease !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 25px rgba(212, 175, 55, 0.55) !important;
        border-color: #FFD700 !important;
    }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #0E162B;
        padding: 6px;
        border-radius: 10px;
        border: 1px solid rgba(212, 175, 55, 0.25);
    }
    .stTabs [data-baseweb="tab"] {
        color: #94A3B8 !important;
        font-family: 'Montserrat', sans-serif !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
        padding: 8px 18px !important;
        border: none !important;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #EA1A85 0%, #1E293B 100%) !important;
        color: #FFFFFF !important;
        border: 1px solid #D4AF37 !important;
        box-shadow: 0 4px 15px rgba(234, 26, 133, 0.3) !important;
    }

    /* Dataframe and Table Polish */
    div[data-testid="stDataFrame"] {
        border: 1px solid rgba(212, 175, 55, 0.25) !important;
        border-radius: 10px !important;
        overflow: hidden !important;
    }

    /* Dividers with Gold-Pink Gradient */
    hr {
        border: 0;
        height: 1px;
        background-image: linear-gradient(to right, rgba(212, 175, 55, 0), rgba(234, 26, 133, 0.75), rgba(212, 175, 55, 0.9), rgba(212, 175, 55, 0)) !important;
        margin: 20px 0 !important;
    }

    /* Expanders */
    div[data-testid="stExpander"] {
        background: #111A33 !important;
        border: 1px solid rgba(212, 175, 55, 0.3) !important;
        border-radius: 10px !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3) !important;
    }
</style>
\"\"\", unsafe_allow_html=True)"""

SIDEBAR_BRANDING = """# Sidebar Navigation (Rajasthan Royals Official Brand Presentation)
st.sidebar.image("https://upload.wikimedia.org/wikipedia/en/thumb/5/5c/Rajasthan_Royals_Logo.svg/300px-Rajasthan_Royals_Logo.svg.png", width=120)
st.sidebar.markdown(\"\"\"
<div style='margin-top: -6px; margin-bottom: 12px;'>
    <div class='rr-hallabol'>🦁 HALLA BOL</div>
    <div style='font-family: Rajdhani, sans-serif; font-size: 1.45rem; font-weight: 800; color: #FFFFFF; letter-spacing: 1px; margin-top: 8px;'>PROJECT RR-EDGE</div>
    <div style='font-family: Montserrat, sans-serif; font-size: 0.78rem; font-weight: 600; color: #D4AF37;'>JAIPUR HERITAGE EDITION • IPL 2027</div>
</div>
\"\"\", unsafe_allow_html=True)
st.sidebar.markdown("---")"""

HERO_BANNER = """    st.markdown(\"\"\"
    <div class='rr-heritage-banner'>
        <div style='display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;'>
            <div>
                <span class='rr-badge' style='margin-bottom: 8px;'>👑 OFFICIAL FRANCHISE SUITE</span>
                <div style='font-family: Rajdhani, sans-serif; font-size: 2.2rem; font-weight: 900; letter-spacing: 1.5px; color: #FFFFFF;'>
                    RAJASTHAN ROYALS <span style='color: #EA1A85;'>DECISION INTELLIGENCE</span>
                </div>
                <div style='font-family: Montserrat, sans-serif; font-size: 0.95rem; color: #D4AF37; font-weight: 600; margin-top: 4px;'>
                    Sawai Mansingh Stadium Fortress • IPL 2027 Auction & Tactical Blueprint
                </div>
            </div>
            <div style='text-align: right; margin-top: 10px;'>
                <span class='rr-badge' style='margin-right: 6px;'>#RoyalPink</span>
                <span class='rr-badge-gold' style='margin-right: 6px;'>#ImperialGold</span>
                <span class='rr-badge-blue'>#JodhpurNavy</span>
            </div>
        </div>
    </div>
    \"\"\", unsafe_allow_html=True)
"""

def update_app(filepath):
    print(f"Updating {filepath}...")
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Replace old CSS block
    css_pattern = re.compile(r"# Custom Styling \(Rajasthan Royals Royal Blue & Vibrant Pink\)\s+st\.markdown\(\"\"\"[\s\S]*?\"\"\", unsafe_allow_html=True\)", re.MULTILINE)
    if css_pattern.search(content):
        content = css_pattern.sub(RR_CSS, content)
        print(" -> Replaced old CSS block successfully.")
    else:
        print(" -> Warning: CSS pattern not matched cleanly; searching alternate boundary.")

    # 2. Replace sidebar logo block
    sidebar_old = """# Sidebar Navigation
st.sidebar.image("https://upload.wikimedia.org/wikipedia/en/thumb/5/5c/Rajasthan_Royals_Logo.svg/300px-Rajasthan_Royals_Logo.svg.png", width=105)
st.sidebar.title("PROJECT RR-EDGE")
st.sidebar.markdown("**IPL 2027 Auction & Tactical Intelligence**")
st.sidebar.markdown("---")"""
    if sidebar_old in content:
        content = content.replace(sidebar_old, SIDEBAR_BRANDING)
        print(" -> Replaced sidebar header successfully.")

    # 3. Add hero banner to Page 1
    page1_target = 'if page == "1. Executive Overview":\n    st.markdown("<h1 style=\'color: #48CAE4;\'>👑 PROJECT RR-EDGE: EXECUTIVE DASHBOARD</h1>", unsafe_allow_html=True)'
    page1_replacement = 'if page == "1. Executive Overview":\n' + HERO_BANNER + '    st.markdown("<h1 class=\'rr-title\'>👑 PROJECT RR-EDGE: EXECUTIVE DASHBOARD</h1>", unsafe_allow_html=True)'
    if page1_target in content:
        content = content.replace(page1_target, page1_replacement)
        print(" -> Injected Hero banner to Page 1.")

    # 4. Global replacement of cyan and magenta headers with RR Royal class
    content = content.replace("style='color: #48CAE4;'", "class='rr-title'")
    content = content.replace("style='color: #FF007F;'", "class='rr-title'")
    content = content.replace('style="color: #48CAE4;"', "class='rr-title'")
    content = content.replace('style="color: #FF007F;"', "class='rr-title'")
    content = content.replace("color_continuous_scale=\"Tealgrn\"", "color_continuous_scale=[[0, '#0B132B'], [0.5, '#EA1A85'], [1.0, '#D4AF37']]")
    content = content.replace("color_continuous_scale=\"Purples\"", "color_continuous_scale=[[0, '#182447'], [0.5, '#EA1A85'], [1.0, '#D4AF37']]")

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    py_compile.compile(filepath, doraise=True)
    print(f" -> Successfully compiled {filepath} without errors!")

if __name__ == "__main__":
    update_app("RR_EDGE_Dashboard/app.py")
    update_app("RR_EDGE_V3_0/dashboard/app.py")
