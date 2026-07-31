import streamlit as st
import openai
from PIL import Image
import io

# 1. Website ka Title aur Theme Setup
st.set_page_config(page_title="Pro-Trader AI Analyzer", layout="wide")
st.title("📈 Pro-Trader AI Chart & Psychology Analyzer")
st.write("Apne TradingView chart ka screenshot upload karein aur professional institutional analysis payein.")

# OpenAI API Key Input (Users apna key daal sakte hain ya aap apna embed kar sakte hain)
api_key = st.sidebar.text_input("OpenAI API Key Darj Karein:", type="password")

# 2. File Uploader Widget
uploaded_file = st.file_uploader("Apna Chart Screenshot (PNG/JPG) Yahan Upload Karein...", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    # Image ko screen par dikhana
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Trading Chart", use_container_width=True)
    
    # Analyze Button
    if st.button("Deep Professional Analysis Shuru Karein"):
        if not api_key:
            st.error("Kripya pehle Sidebar me OpenAI API Key dalein!")
        else:
            with st.spinner("AI aapke chart ko deeply scan kar raha hai aur kamiyan dhoond raha hai..."):
                try:
                    # Image ko bytes me convert karna API ke liye
                    img_byte_arr = io.BytesIO()
                    image.save(img_byte_arr, format='PNG')
                    img_bytes = img_byte_arr.getvalue()
                    
                    # 3. Institutional Trader Prompt (Jo aapki saari requirements poori karega)
                    system_prompt = """
                    Aap ek World-Class Institutional Trader, Risk Manager aur Trading Psychologist hain. 
                    Is chart ka screenshot dekhkar ek aisi deep analysis report banayein jo ek aam retail trader nahi dekh pata. 
                    Report ko in 5 headings me divide karein:

                    1. 🔍 MARKET STRUCTURE & PRICE ACTION:
                       - Major trend (Bullish/Bearish/Sideways), Support aur Resistance zones identify karein.
                       - Candlestick patterns aur Chart patterns (agar koi hain) ka breakdown dein.

                    2. 🎯 EXACT TRADE EXECUTION PLAN:
                       - Professional Entry Zone, Invalidation Level (Stop-Loss) aur Target (Take-Profit) exact price levels ke sath batayein.

                    3. ⚠️ RETAIL TRADER MISTAKES (Kamiyan aur Galtiyan):
                       - Is chart par aam taur par retail traders kya galti karte hain? (Jaise: FOMO me aakar galat jagah entry, Support ke bilkul upar sell karna, ya tight stop-loss rakhna).
                       - Kya abhi trade lena "Chasing the market" (bhaagti hui market ke piche bhagna) hai?

                    4. 🧠 TRADING PSYCHOLOGY & RISK WARNING:
                       - Is trading setup me greed (lalach) aur fear (darr) kahan par trigger ho sakta hai?
                       - Risk-to-Reward Ratio calculate karein (Kamyab hone ke liye minimum 1:2 hona chahiye).

                    5. 🚦 FINAL VERDICT:
                       - Saaf shabdon me batayein: HIGH PROBABILITY SETUP (Trade lene layak hai) ya NO TRADE ZONE (Wait karna behtar hai).
                    """
                    
                    # OpenAI API Call (Using gpt-4o for advanced visual analysis)
                    openai.api_key = api_key
                    # Note: API format standard OpenAI integration ke mutabaq hai
                    response = openai.chat.completions.create(
                        model="gpt-4o",
                        messages=[
                            {
                                "role": "user",
                                "content": [
                                    {"type": "text", "text": system_prompt},
                                    {
                                        "type": "image_url",
                                        "image_url": {
                                            "url": f"data:image/png;base64,{img_bytes.hex()}" # Simple representation
                                        }
                                    }
                                ]
                            }
                        ],
                        max_tokens=1500
                    )
                    
                    # Output ko Display karna
                    st.success("Analysis Complete!")
                    st.markdown("### 📊 AI Professional Report:")
                    st.write(response.choices[0].message.content)
                    
                except Exception as e:
                    st.error(f"Ek error aaya: {str(e)}")
