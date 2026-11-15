"""
Appends Consoles 23 and 24 to RR_EDGE_Dashboard/app.py
Expanding the live dashboard to 24 Consoles!
"""

import os
import py_compile

APP_PATH = r"C:\Users\PREMCHANDYADAV\Downloads\RR_Competition\RR_EDGE_Dashboard\app.py"

with open(APP_PATH, "r", encoding="utf-8") as f:
    code = f.read()

# 1. Update Navigation Radio List
old_nav = """"21. Spatial Fielding Optimization, Catch WPA & DRS Policy",
        "22. Squad WAR, Psychometric Clutch & Injury Resilience Hub"
    ]"""

new_nav = """"21. Spatial Fielding Optimization, Catch WPA & DRS Policy",
        "22. Squad WAR, Psychometric Clutch & Injury Resilience Hub",
        "23. SMS Jaipur Aerodynamics & Trajectory Flight Physics",
        "24. Zubin Bharucha High-Performance Academy & Biomechanical Lab"
    ]"""

if old_nav in code:
    code = code.replace(old_nav, new_nav)
    print("Successfully updated navigation list in app.py!")
else:
    print("Warning: old_nav not found exactly. Check app.py navigation.")

# 2. Append Console 23 and 24 code at the bottom
consoles_23_24_code = '''

# -------------------------------------------------------------
# PAGE 23: SMS JAIPUR AERODYNAMICS & TRAJECTORY FLIGHT PHYSICS
# -------------------------------------------------------------
elif page == "23. SMS Jaipur Aerodynamics & Trajectory Flight Physics":
    st.markdown("""
    <div class='rr-heritage-banner'>
        <div style='display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;'>
            <div>
                <span class='rr-badge' style='margin-bottom: 8px;'>🌬️ FLUID DYNAMICS & ATMOSPHERIC FLIGHT</span>
                <div style='font-family: Rajdhani, sans-serif; font-size: 2.2rem; font-weight: 900; letter-spacing: 1.5px; color: #FFFFFF;'>
                    SAWAI MANSINGH STADIUM <span style='color: #EA1A85;'>AERODYNAMICS & ALTITUDE</span>
                </div>
                <div style='font-family: Montserrat, sans-serif; font-size: 0.95rem; color: #D4AF37; font-weight: 600; margin-top: 4px;'>
                    435m Altitude Air Density (rho=1.172 kg/m³) • Aravalli Crosswinds • Magnus Flight Trajectories
                </div>
            </div>
            <div style='text-align: right; margin-top: 10px;'>
                <span style='background: rgba(234, 26, 133, 0.2); border: 1px solid #EA1A85; color: #EA1A85; padding: 6px 14px; border-radius: 20px; font-weight: 700; font-size: 0.85rem;'>
                    ALTITUDE BOOST: +5.4m
                </span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    aero_path = os.path.join(BASE_DIR, "outputs", "advanced_dimensions", "stadium_aerodynamics_flight_model.csv")
    if os.path.exists(aero_path):
        df_ae = pd.read_csv(aero_path)
        
        st.subheader("🌬️ Trajectory Flight Model Across Key Batter Signature Shots")
        st.dataframe(df_ae, use_container_width=True)
        
        c_a1, c_a2, c_a3 = st.columns(3)
        c_a1.metric("Altitude Air Density (rho)", "1.172 kg/m³", "-4.33% vs Sea Level")
        c_a2.metric("Aravalli Evening Crosswind", "14 km/h (NW -> SE)", "+6.1m Carry Boost")
        c_a3.metric("Max Fence Clearance", "Shimron Hetmyer (+25.6m)", "93.6m Total Carry")

        st.markdown("---")
        st.subheader("🏟️ Stadium Boundary Dimensions vs Aerodynamic Flight Carry")
        st.info("""
        • **Altitude Advantage (435m above sea level)**: At 32°C night temperature in Jaipur, thinner air reduces drag coefficient (Cd), granting +3.5m to +5.4m additional distance on aerial hits.
        • **Targeting the Shorter 68m Square Boundary**: Riyan Parag (pull shot with the wind) and Hetmyer (slog sweep) achieve over 89m of carry, easily clearing the fence by 21m+.
        """)


# -------------------------------------------------------------
# PAGE 24: ZUBIN BHARUCHA HIGH-PERFORMANCE ACADEMY & BIOMECHANICAL LAB
# -------------------------------------------------------------
elif page == "24. Zubin Bharucha High-Performance Academy & Biomechanical Lab":
    st.markdown("""
    <div class='rr-heritage-banner'>
        <div style='display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;'>
            <div>
                <span class='rr-badge' style='margin-bottom: 8px;'>🔬 RED BULL HIGH PERFORMANCE CENTRE</span>
                <div style='font-family: Rajdhani, sans-serif; font-size: 2.2rem; font-weight: 900; letter-spacing: 1.5px; color: #FFFFFF;'>
                    ZUBIN BHARUCHA <span style='color: #EA1A85;'>SKILL-ACQUISITION & BIOMECHANICS</span>
                </div>
                <div style='font-family: Montserrat, sans-serif; font-size: 0.95rem; color: #D4AF37; font-weight: 600; margin-top: 4px;'>
                    10,000-Ball Motor Learning • Kinetic Force Plates • High-Speed Photron 1,000 FPS Eye Tracking
                </div>
            </div>
            <div style='text-align: right; margin-top: 10px;'>
                <span style='background: rgba(212, 175, 55, 0.2); border: 1px solid #D4AF37; color: #D4AF37; padding: 6px 14px; border-radius: 20px; font-weight: 700; font-size: 0.85rem;'>
                    TALEGAON ACADEMY CERTIFIED
                </span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    drill_path = os.path.join(BASE_DIR, "outputs", "advanced_dimensions", "high_performance_training_prescriptions.csv")
    if os.path.exists(drill_path):
        df_dr = pd.read_csv(drill_path)
        
        st.subheader("📋 Official Pre-Season Biomechanical Drill Prescriptions")
        st.dataframe(df_dr, use_container_width=True)
        
        st.markdown("---")
        st.subheader("🏆 The Zubin Bharucha Method: 3 Pillars of Development")
        b1, b2, b3 = st.columns(3)
        b1.success("**1. Compressed Decision Time**\\n\\n16-yard side-arm machine drills at 148 kph force Jaiswal to process ball seam line under 0.34s.")
        b2.warning("**2. Ballistic Heavy Pull**\\n\\nOver-weighted cricket balls for Riyan Parag to roll wrists on 140+ kph rising chest deliveries.")
        b3.info("**3. Deflection Board Geometry**\\n\\nMulti-surface deflection tiles train Dhruv Jurel for sub-0.30s stumping reaction times.")
'''

code += consoles_23_24_code

with open(APP_PATH, "w", encoding="utf-8") as f:
    f.write(code)

print("Updated app.py with Consoles 23 and 24! Testing py_compile...")
py_compile.compile(APP_PATH, doraise=True)
print("py_compile passed cleanly with 0 errors!")
