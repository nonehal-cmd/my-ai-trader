import streamlit as st
from google import genai
from PIL import Image

# 1. Website Setup
st.set_page_config(page_title="Pro-Trader AI Analyzer", layout="wide")
st.title("📈 Pro-Trader AI Chart & Psychology Analyzer (Gemini FREE)")
st.write("Apne TradingView chart ka screenshot upload karein aur free institutional analysis payein.")

# Gemini API Key Input
api_key = st.sidebar.text_input("Google Gemini API Key Darj Karein:", type="password")

# 2. File Uploader
uploaded_file = st.file_uploader("Apna Chart Screenshot (PNG/JPG) Yahan Upload Karein...", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Trading Chart", use_container_width=True)
    
    if st.button("Deep Professional Analysis Shuru Karein"):
        if not api_key:
            st.error("Kripya pehle Sidebar me Google Gemini API Key dalein!")
        else:
            with st.spinner("Gemini AI aapke chart ko deeply scan kar raha hai..."):
                try:
                    # Initialize Gemini Client
                    client = genai.Client(api_key=api_key)
                    
                    system_prompt = """
                    Aap ek World-Class Institutional Trader aur Trading Psychologist hain. 
                    Is chart ka screenshot dekhkar ek deep analysis report banayein. 
                    Report ko in headings me divide karein:
                    1. 🔍 MARKET STRUCTURE & PRICE ACTION (Trend, Support/Resistance, Patterns)
                    2. 🎯 EXACT TRADE EXECUTION PLAN (Entry, Stop-Loss, Target price levels ke sath)
                    3. ⚠️ RETAIL TRADER MISTAKES (Is chart par aam traders kya galti karte hain)
                    4. 🧠 TRADING PSYCHOLOGY & RISK-TO-REWARD RATIO
                    5. 🚦 FINAL VERDICT (HIGH PROBABILITY SETUP ya NO TRADE ZONE)
                    """
                    
                    # 🚨 FIXED: Updated to latest available production model
                    response = client.models.generate_content(
                        model='gemini-3.6-flash',
                        contents=[image, system_prompt]
                    )
                    
                    st.success("Analysis Complete!")
                    st.markdown("### 📊 AI Professional Report:")
                    st.write(response.text)
                    
                except Exception as e:
                    st.error(f"Ek error aaya: {str(e)}")
