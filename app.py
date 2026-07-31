import streamlit as st
from google import genai
from PIL import Image

# 1. Page Configuration for Wide View (Zero Scrolling)
st.set_page_config(page_title="Pro AI Analyzer", layout="wide", initial_sidebar_state="expanded")

# Custom CSS for UI styling and Popup look
st.markdown("""
    <style>
    .report-box { padding: 15px; border-radius: 10px; background-color: #1E1E1E; margin-bottom: 10px; border-left: 5px solid #00FFCC; }
    .verdict-box { padding: 20px; border-radius: 10px; background-color: #2D1A1A; border: 2px solid #FF4B4B; text-align: center; }
    </style>
""", unsafe_allow_index=True)

st.title("🎯 Institutional Multi-Timeframe AI Analyzer")

# Sidebar Setup
api_key = st.sidebar.text_input("Google Gemini API Key:", type="password")
st.sidebar.markdown("---")
st.sidebar.info("💡 Pro-Tip: Multi-timeframe analysis se accuracy badh jaati hai.")

# State Management for hiding image after analysis
if 'analyzed' not in st.session_state:
    st.session_state.analyzed = False
if 'report_text' not in st.session_state:
    st.session_state.report_text = ""

# 2. Multi-Timeframe File Uploaders
col_files1, col_files2 = st.columns(2)
with col_files1:
    htf_file = st.file_uploader("1. Higher Timeframe Chart (e.g., 1H / 4H)", type=["jpg", "png", "jpeg"])
with col_files2:
    ltf_file = st.file_uploader("2. Lower Timeframe Chart (e.g., 5M / 15M)", type=["jpg", "png", "jpeg"])

# Show images ONLY IF analysis hasn't started yet (Hiding System)
if (htf_file or ltf_file) and not st.session_state.analyzed:
    st.subheader("📸 Uploaded Charts Preview")
    col_img1, col_img2 = st.columns(2)
    if htf_file:
        with col_img1: st.image(Image.open(htf_file), caption="Higher Timeframe", use_container_width=True)
    if ltf_file:
        with col_img2: st.image(Image.open(ltf_file), caption="Lower Timeframe", use_container_width=True)

# 3. Execution Trigger
if htf_file and ltf_file:
    if st.button("🚀 Run Deep Combo Analysis", use_container_width=True):
        if not api_key:
            st.error("Please enter Gemini API Key in the sidebar!")
        else:
            with st.spinner("AI analyzing both timeframes..."):
                try:
                    client = genai.Client(api_key=api_key)
                    img1 = Image.open(htf_file)
                    img2 = Image.open(ltf_file)
                    
                    prompt = """
                    Aap ek Institutional Multi-Timeframe Analyst hain. In dono charts (HTF aur LTF) ka milakar analysis karein.
                    Report ko bilkul short aur direct banayein. Khaas taur par short headings use karein.
                    Format exactly text me bhejye jo niche diye gaye 4 hisson me divide ho:
                    [PART1] Market Trend & Structure from HTF.
                    [PART2] Exact Trade Entry, Stop-Loss, and Target levels based on LTF alignment.
                    [PART3] Top 2 Retail Trader Mistakes to avoid on this current setup.
                    [PART4] Final Verdict (HIGH PROBABILITY or NO TRADE) with Risk-to-Reward.
                    """
                    
                    response = client.models.generate_content(
                        model='gemini-3.6-flash',
                        contents=[img1, img2, prompt]
                    )
                    
                    # Store in session and hide image
                    st.session_state.report_text = response.text
                    st.session_state.analyzed = True
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {str(e)}")

# 4. Display Result in clean, No-Scroll Dashboard Columns
if st.session_state.analyzed:
    st.success("✅ Analysis Complete! (Charts hidden for clean dashboard view)")
    
    # Reset Button to upload new charts
    if st.button("🔄 Analyze New Charts"):
        st.session_state.analyzed = False
        st.session_state.report_text = ""
        st.rerun()
        
    raw_text = st.session_state.report_text
    
    # Displaying clean layout using Columns to prevent vertical scrolling
    col_res1, col_res2 = st.columns(2)
    
    with col_res1:
        st.markdown("<div class='report-box'><h3>🔍 Market Structure (HTF)</h3>" + raw_text + "</div>", unsafe_allow_index=True)
        
    with col_res2:
        # Streamlit Popup/Dialog simulation for the execution blueprint
        @st.dialog("🎯 INSTANT TRADE BLUEPRINT")
        def show_popup(text):
            st.write("Professional Execution Plan:")
            st.markdown(text)
            if st.button("Close"): st.rerun()
            
        if st.button("🔥 Open Instant Popup Blueprint", use_container_width=True):
            show_popup(raw_text)
            
        st.markdown("<div class='verdict-box'><h3>🚦 AI Action Plan</h3>Review the layout or click the popup button above for exact trade signals.</div>", unsafe_allow_index=True)
