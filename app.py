import streamlit as st
from groq import Groq

# 1. Page Configuration
st.set_page_config(page_title="AI Tweet Generator", layout="wide")

# 2. Enhanced CSS
st.markdown("""
    <style>
    /* Main Gradient Background */
    .stApp { background: linear-gradient(135deg, #4A00E0, #FF0080); }
    
    /* Title Styling */
    .main-title { text-align: center; color: white !important; padding: 20px 0; }
    
    /* Sidebar Styling - Forces color to show */
    [data-testid="stSidebar"] {
        background-color: rgba(0, 0, 0, 0.3) !important;
    }
    [data-testid="stSidebar"] label, [data-testid="stSidebar"] h2 {
        color: white !important;
        font-weight: bold !important;
    }
    
    /* Output Card Styling (White cards, Black text) */
    .card {
        background-color: rgba(255, 255, 255, 0.95) !important;
        color: #000000 !important;
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Title at the top
st.markdown('<h1 class="main-title">🐦 AI Brand Voice & Tweet Generator</h1>', unsafe_allow_html=True)

# 4. Sidebar Inputs
with st.sidebar:
    st.markdown("## ⚙️ Brand Information")
    brand = st.text_input("Brand Name")
    industry = st.text_input("Industry")
    product = st.text_input("Product")
    audience = st.text_input("Target Audience")
    goal = st.text_input("Content Goal")
    num_tweets = st.slider("Number of Tweets", 5, 20, 10)
    generate = st.button("🚀 Generate Content", use_container_width=True)

# 5. Logic & Display
if generate:
    # IMPORTANT: Ensure your Groq API key is valid here
    client = Groq(api_key="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") 
    
    with st.spinner("Analyzing and Generating..."):
        prompt_voice = f"Analyze brand voice for {brand}. Return ONLY 4 bullet points: Tone, Audience, Themes, Style."
        voice = client.chat.completions.create(model="llama-3.1-8b-instant", messages=[{"role": "user", "content": prompt_voice}])
        voice_output = voice.choices[0].message.content

        prompt_tweets = f"Voice: {voice_output}. Generate {num_tweets} tweets for {brand}."
        tweets = client.chat.completions.create(model="llama-3.1-8b-instant", messages=[{"role": "user", "content": prompt_tweets}])
        tweet_output = tweets.choices[0].message.content

        # Dashboard layout using the custom 'card' class
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Brand Voice Summary")
            st.markdown(f'<div class="card">{voice_output.replace("•", "<br>•")}</div>', unsafe_allow_html=True)
        with col2:
            st.subheader("Generated Tweets")
            for line in tweet_output.split("\n"):
                if line.strip():
                    st.markdown(f'<div class="card">{line}</div>', unsafe_allow_html=True)