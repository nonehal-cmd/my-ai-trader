import streamlit as st
from google import genai
from PIL import Image
import json
import base64
import requests
import io

# 1. Page Configuration & Wide Grid Layout Setup
st.set_page_config(page_title="Institutional AI Dashboard", layout="wide", initial_sidebar_state="expanded")

# Custom CSS aapke sketch/design ke mutabaq colorful boxes aur badges banane ke liye
st.markdown("""
    <style>
    .header-box { background-color: #1E1E1E; padding: 15px; border-radius: 8px; border: 1px solid #333; text-align: center; font-weight: bold; }
    .signal-buy { background-color: #155724; color: #d4edda; padding: 15px; border-radius: 8px; font-size: 22px; font-weight: bold; text-align: center; border: 2px solid #28a745; }
    .signal-sell { background-color: #721c24; color: #f8d7da; padding: 15px; border-radius: 8px; font-size: 22px; font-weight: bold; text-align: center; border: 2px solid #dc3545; }
    .conf-circle { background-color: #004085; color: #cce5ff; padding: 15px; border-radius: 50%; font-size: 22px; font-weight: bold; text-align: center; border: 2px solid #004085; width: 80px; height: 80px; display: flex; align-items: center; justify-content: center; margin: auto; }
    .content-card { background-color: #121212; padding: 20px; border-radius: 10px; border-top: 4px solid #00FFCC; min-height: 250px; margin-bottom: 15px; }
    .psych-card { background-color: #121212; padding: 20px; border-radius: 10px; border-top: 4px solid #FFCC00; min-height: 250px; margin-bottom: 15px; }
    </style>
""", unsafe_allow_html=True)

st.title("🛡️ Institutional Pro AI Dashboard")

# 🤖 SIDEBAR MULTI-API SYSTEM
st.sidebar.header("🛠️ AI Model Engine Settings")
api_provider = st.sidebar.selectbox("Choose AI Provider:", ["Google Gemini (FREE)", "Groq AI (Llama-3 FREE Backup)"])

api_key = st.sidebar.text_input(f"Enter {api_provider} API Key:", type="password")
st.sidebar.markdown("---")
st.sidebar.info("💡 Tip: Agar Gemini limit khatam ho jaye (Error 429), toh 'Groq AI' select karke chalaayein.")

# Session States Management
if 'analyzed' not in st.session_state: st.session_state.analyzed = False
if 'ai_data' not in st.session_state: st.session_state.ai_data = {}

# 2. File Uploaders
col_u1, col_u2 = st.columns(2)
with col_u1: htf_file = st.file_uploader("Upload Image 1 (Higher Timeframe / Main Chart)", type=["jpg", "png", "jpeg"])
with col_u2: ltf_file = st.file_uploader("Upload Image 2 (Lower Timeframe - Optional)", type=["jpg", "png", "jpeg"])

prompt = """
Aap ek top-tier institutional trader hain. Is chart screenshot ka code-level structure me data chahiye.
Mera response strict aur valid JSON format me hona chahiye bina kisi markdown block (```json) ke. 
Response is pattern me hona chahiye:
{
    "symbol": "Asset Name / Symbol (e.g. BTC, XAU/USD, RELIANCE)",
    "full_analysis": "Short 2-line global technical structure statement.",
    "signal": "BUY ya SELL ya NEUTRAL",
    "confirmation": "Confirmation percentage (e.g. 85%)",
    "retail_vs_pro": "Retailer kya sochta hai aur kyun wo galat hai, aur pro logic kya hai.",
    "liquidity_psychology": "Liquidity sweeps, Support/Resistance zones aur critical psychology points.",
    "other_news": "Expected macro events, target timeframes aur additional information."
}
"""

# Analysis Trigger Button
if htf_file or ltf_file:
    if not st.session_state.analyzed:
        if st.button("🚀 Shuru Karein Deep Live Analysis", use_container_width=True):
            if not api_key:
                st.error(f"Sidebar me {api_provider} Key darj karein!")
            else:
                with st.spinner(f"AI ({api_provider}) aapke layout ke mutabaq data process kar raha hai..."):
                    try:
                        clean_text = ""
                        
                        # 🟢 CONFIGURATION FOR GOOGLE GEMINI
                        if "Gemini" in api_provider:
                            client = genai.Client(api_key=api_key)
                            contents_list = []
                            if htf_file: contents_list.append(Image.open(htf_file))
                            if ltf_file: contents_list.append(Image.open(ltf_file))
                            contents_list.append(prompt)
                            
                            response = client.models.generate_content(
                                model='gemini-2.0-flash',
                                contents=contents_list
                            )
                            clean_text = response.text.strip()
                        
                        # 🔵 CONFIGURATION FOR GROQ FREE BACKUP (Llama-3 Vision)
                        elif "Groq" in api_provider:
                            # 🚨 FIXED: Convert RGBA to RGB to fix JPEG compression error
                            main_img = Image.open(htf_file if htf_file else ltf_file)
                            if main_img.mode in ("RGBA", "P"):
                                main_img = main_img.convert("RGB")
                                
                            buffered = io.BytesIO()
                            main_img.save(buffered, format="JPEG")
                            base64_image = base64.b64encode(buffered.getvalue()).decode('utf-8')
                            
                            headers = {
                                "Authorization": f"Bearer {api_key}",
                                "Content-Type": "application/json"
                            }
                            payload = {
                                "model": "llama-3.2-11b-vision-preview",
                                "messages": [
                                    {
                                        "role": "user",
                                        "content": [
                                            {"type": "text", "text": prompt},
                                            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                                        ]
                                    }
                                ],
                                "response_format": {"type": "json_object"}
                            }
                            res = requests.post("https://groq.com", headers=headers, json=payload)
                            clean_text = res.json()['choices']['message']['content'].strip()

                        # JSON clean up and parsing
                        if clean_text.startswith("```json"): clean_text = clean_text[7:]
                        if clean_text.endswith("```"): clean_text = clean_text[:-3]
                        
                        st.session_state.ai_data = json.loads(clean_text.strip())
                        st.session_state.analyzed = True
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"Error aaya: {str(e)}. Agar limit ka issue hai, toh doosra API provider select karein.")

# 3. Dynamic UI Generation - AAPKE WIREFRAME KE MUTABAQ
if st.session_state.analyzed:
    data = st.session_state.ai_data
    
    if st.button("🔄 Naya Chart Analyze Karein"):
        st.session_state.analyzed = False
        st.session_state.ai_data = {}
        st.rerun()

    st.markdown("---")
    
    # ROW 1: SYMBOL | ANALYSIS | SIGNAL | CONF
    row1_col1, row1_col2, row1_col3, row1_col4 = st.columns([1.5, 4, 2, 1.5])
    with row1_col1: st.markdown(f"<div class='header-box'><span style='color:#00FFCC;'>SYMBOL</span><br><span style='font-size:20px;'>{data.get('symbol', 'N/A')}</span></div>", unsafe_allow_html=True)
    with row1_col2: st.markdown(f"<div class='header-box' style='text-align:left;'><span style='color:#00FFCC;'>FULL CHART ANALYSIS</span><br><span style='font-weight:normal;'>{data.get('full_analysis', 'N/A')}</span></div>", unsafe_allow_html=True)
    with row1_col3:
        sig = data.get('signal', 'NEUTRAL').upper()
        bg_class = "signal-buy" if "BUY" in sig else ("signal-sell" if "SELL" in sig else "header-box")
        st.markdown(f"<div class='{bg_class}'>SIGNAL<br>{sig}</div>", unsafe_allow_html=True)
    with row1_col4: st.markdown(f"<div class='conf-circle'>{data.get('confirmation', '50%')}</div>", unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ROW 2: IMAGES & TEXT GRIDS
    main_col1, main_col2, main_col3 = st.columns([2.5, 4.5, 4])
    with main_col1:
        st.markdown("<p style='font-weight:bold; color:#777;'>📸 CHARTS PREVIEW</p>", unsafe_allow_html=True)
        if htf_file: st.image(Image.open(htf_file), caption="Main Image", use_container_width=True)
        if ltf_file: st.image(Image.open(ltf_file), caption="Secondary Image", use_container_width=True)
        
    with main_col2:
        st.markdown(f"<div class='content-card'><h4 style='color:#FF4B4B;'>🧠 Retail vs Pro Logic (Sabse Alag)</h4><p>{data.get('retail_vs_pro', 'N/A')}</p></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='psych-card'><h4 style='color:#00FFCC;'>📊 Liquidity, Levels & Psychology</h4><p>{data.get('liquidity_psychology', 'N/A')}</p></div>", unsafe_allow_html=True)
        
    with main_col3:
        st.markdown(f"<div class='content-card' style='border-top: 4px solid #9900FF; min-height:535px;'><h4 style='color:#9900FF;'>📰 Other, News & Macro Events</h4><p>{data.get('other_news', 'N/A')}</p></div>", unsafe_allow_html=True)
