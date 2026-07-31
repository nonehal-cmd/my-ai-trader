import streamlit as st
from google import genai
from PIL import Image

# 1. Page Configuration for Wide View
st.set_page_config(page_title="Pro AI Analyzer", layout="wide", initial_sidebar_state="expanded")

# Custom CSS for UI styling
st.markdown("""
    <style>
    .report-box { padding: 15px; border-radius: 10px; background-color: #1E1E1E; margin-bottom: 10px; border-left: 5px solid #00FFCC; }
    .verdict-box { padding: 20px; border-radius: 10px; background-color: #2D1A1A; border: 2px solid #FF4B4B; text-align: center; }
    </style>
""", unsafe_allow_html=True)

st.title("🎯 Pro AI Chart & Psychology Analyzer")

# Sidebar Setup
api_key = st.sidebar.text_input("Google Gemini API Key:", type="password")
st.sidebar.markdown("---")
st.sidebar.info("💡 Tip: Aap koi bhi ek chart ya fir dono charts ek saath upload kar sakte hain.")

# State Management for hiding image after analysis
if 'analyzed' not in st.session_state:
    st.session_state.analyzed = False
if 'report_text' not in st.session_state:
    st.session_state.report_text = ""

# 2. Multi-Timeframe File Uploaders
col_files1, col_files2 = st.columns(2)
with col_files1:
    htf_file = st.file_uploader("Chart 1 (Higher Timeframe - Optional)", type=["jpg", "png", "jpeg"])
with col_files2:
    ltf_file = st.file_uploader("Chart 2 (Lower Timeframe - Optional)", type=["jpg", "png", "jpeg"])

# Show images ONLY IF analysis hasn't started yet (Hiding System)
if (htf_file or ltf_file) and not st.session_state.analyzed:
    st.subheader("📸 Uploaded Charts Preview")
    col_img1, col_img2 = st.columns(2)
    if htf_file:
        with col_img1: st.image(Image.open(htf_file), caption="Chart 1", use_container_width=True)
    if ltf_file:
        with col_img2: st.image(Image.open(ltf_file), caption="Chart 2", use_container_width=True)

# 3. Execution Trigger (Chalu hoga agar KAM SE KAM EK file upload ho)
if htf_file or ltf_file:
    if st.button("🚀 Run Deep Analysis", use_container_width=True):
        if not api_key:
            st.error("Please enter Gemini API Key in the sidebar!")
        else:
            with st.spinner("AI aapke data ko deeply scan kar raha hai..."):
                client = genai.Client(api_key=api_key)
                
                # Check karna ki user ne kaun-kaun se charts diye hain
                contents_list = []
                if htf_file:
                    contents_list.append(Image.open(htf_file))
                if ltf_file:
                    contents_list.append(Image.open(ltf_file))
                
                # Prompt ko flexible banana
                prompt = """
                Aap ek World-Class Institutional Trader aur Trading Psychologist hain. 
                Diye gaye trading chart screenshot (ya dono screenshots) ko deeply analyze karein. 
                Agar do charts hain toh unhe multi-timeframe ke mutabaq align karein, agar ek hai toh usi par focus karein.
                Report ko in 4 headings me divide karein:
                1. 🔍 MARKET STRUCTURE & PRICE ACTION (Trend, Support/Resistance, Patterns)
                2. 🎯 EXACT TRADE EXECUTION PLAN (Entry, Stop-Loss, Target price levels ke sath)
                3. ⚠️ RETAIL TRADER MISTAKES (Is chart par aam traders kya galti karte hain)
                4. 🧠 TRADING PSYCHOLOGY & RISK-TO-REWARD RATIO
                5. 🚦 FINAL VERDICT (HIGH PROBABILITY SETUP ya NO TRADE ZONE)
                """
                contents_list.append(prompt)
                
                # Dual-Model Backup Execution
                try:
                    response = client.models.generate_content(
                        model='gemini-2.5-flash',  # Ultra-stable production model
                        contents=contents_list
                    )
                    st.session_state.report_text = response.text
                    st.session_state.analyzed = True
                    st.rerun()
                except Exception as primary_error:
                    try:
                        response = client.models.generate_content(
                            model='gemini-2.0-flash',
                            contents=contents_list
                    )
                        st.session_state.report_text = response.text
                        st.session_state.analyzed = True
                        st.rerun()
                    except Exception as backup_error:
                        st.error(f"Servers busy hain, please 5 seconds baad try karein. Detail: {str(backup_error)}")

# 4. Display Result in clean, No-Scroll Dashboard Columns
if st.session_state.analyzed:
    st.success("✅ Analysis Complete! (Charts hidden for clean dashboard view)")
    
    # Reset Button to upload new charts
    if st.button("🔄 Analyze New Charts"):
        st.session_state.analyzed = False
        st.session_state.report_text = ""
        st.rerun()
        
    raw_text = st.session_state.report_text
    
    col_res1, col_res2 = st.columns(2)
    
    with col_res1:
        st.markdown("<div class='report-box'><h3>📊 Chart Technical Report</h3>" + raw_text + "</div>", unsafe_allow_html=True)
        
    with col_res2:
        # Streamlit Popup/Dialog simulation
        @st.dialog("🎯 INSTANT TRADE BLUEPRINT")
        def show_popup(text):
            st.write("Professional Execution Plan:")
            st.markdown(text)
            if st.button("Close"): st.rerun()
            
        if st.button("🔥 Open Instant Popup Blueprint", use_container_width=True):
            show_popup(raw_text)
            
        st.markdown("<div class='verdict-box'><h3>🚦 AI Action Plan</h3>Review the layout or click the popup button above for exact trade signals.</div>", unsafe_allow_html=True)
