import os
import streamlit as st
import requests
import json
from PIL import Image
from io import BytesIO

# Set page configuration
st.set_page_config(page_title="Tamil to English Translation & Story Generation", layout="wide")

# Load tokens from environment variables
HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN")
GROQ_TOKEN = os.getenv("GROQ_TOKEN")

# Hugging Face API URLs
TRANSLATE_API_URL = "https://api-inference.huggingface.co/models/facebook/mbart-large-50-many-to-one-mmt"
IMAGE_API_URL = "https://api-inference.huggingface.co/models/CompVis/stable-diffusion-v1-4"
headers = {"Authorization": f"Bearer {HUGGINGFACE_TOKEN}"}

# Function to translate Tamil to English
def translate_tamil_to_english(text):
    payload = {"inputs": text}
    response = requests.post(TRANSLATE_API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        result = response.json()
        return result[0]['generated_text']
    else:
        return f"Error {response.status_code}: {response.text}"

# Function to generate an image from a prompt
def generate_image(prompt):
    data = {"inputs": prompt}
    response = requests.post(IMAGE_API_URL, headers=headers, json=data)
    if response.status_code == 200:
        image = Image.open(BytesIO(response.content))
        return image
    else:
        return f"Error {response.status_code}: {response.text}"

# Function to generate text using Groq
def generate_text(prompt, max_tokens, temperature):
    messages = [{"role": "user", "content": prompt}]
    payload = {
        "model": "mixtral-8x7b-32768",
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": temperature,
    }
    response = requests.post("https://api.groq.com/openai/v1/chat/completions", 
                              headers={"Authorization": f"Bearer {GROQ_TOKEN}"}, 
                              json=payload)
    if response.status_code == 200:
        result = response.json()
        return result["choices"][0]["message"]["content"]
    else:
        return f"Error {response.status_code}: {response.text}"

# Process input data
def process_input(tamil_text, max_tokens, temperature):
    with st.spinner("Translating and generating content..."):
        english_text = translate_tamil_to_english(tamil_text)
        image = generate_image(english_text)
        generated_story = generate_text(english_text, max_tokens, temperature)
    return english_text, image, generated_story

# Style for title with animated gradient
st.markdown(""" 
    <style>
    @keyframes gradient {
        0% {background-position: 0% 50%;}
        50% {background-position: 100% 50%;}
        100% {background-position: 0% 50%;}
    }
    .title {
        font-size: 60px;
        color: white;
        text-align: center;
        background: linear-gradient(-45deg, #ff9966, #ff5e62, #ff9966, #ff5e62);
        background-size: 400% 400%;
        animation: gradient 10s ease infinite;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.3);
        margin-bottom: 20px;  /* Space below the title */
    }
    </style>
    """, unsafe_allow_html=True)

# Main Title
st.markdown("<h1 class='title'>Tamil to English Translation & Story Generation</h1>", unsafe_allow_html=True)

# Sidebar Styling
st.markdown("""
    <style>
    .sidebar .sidebar-content {
        background-color: #2c3e50;
        color: white;
        text-align: center;  /* Center text in sidebar */
    }
    .sidebar .stTextArea, .sidebar .stSlider {
        width: 100%;  /* Full width for sidebar elements */
    }
    .sidebar .stButton > button {
        display: block;  /* Center buttons */
        margin: 0 auto;  /* Center buttons */
    }
    </style>
    """, unsafe_allow_html=True)

st.sidebar.header("Settings")

# Sidebar input elements
tamil_text_input = st.sidebar.text_area("Enter Tamil Text", help="Paste or type the Tamil text to translate and generate a story.")
max_tokens_input = st.sidebar.slider("Max Tokens", min_value=50, max_value=200, value=100, step=10, help="Controls the length of the generated story.")
temperature_input = st.sidebar.slider("Temperature", min_value=0.0, max_value=1.0, value=0.7, step=0.1, help="Controls the randomness of the generated story.")

# Initialize the session state for instructions
if "show_instructions" not in st.session_state:
    st.session_state.show_instructions = False

# How to Use Button
if st.sidebar.button("How to Use"):
    st.session_state.show_instructions = not st.session_state.show_instructions

# Show instructions if toggled on
if st.session_state.show_instructions:
    st.sidebar.info(
        """
        **Instructions:**
        1. Enter the Tamil text you want to translate in the text area.
        2. Adjust the **Max Tokens** slider to set the desired length of the generated story.
        3. Use the **Temperature** slider to control the creativity of the generated output.
        4. Click the **Submit** button to get the translated text and generated story along with an image.
        5. Review the outputs displayed in the main area.
        """
    )

# Display progress bar
progress_bar = st.sidebar.progress(0)

# Submit Button
if st.sidebar.button("Submit"):
    progress_bar.progress(20)  # Start progress
    english_text, image, generated_story = process_input(tamil_text_input, max_tokens_input, temperature_input)
    progress_bar.progress(100)  # Complete progress

    # Notify the user that the process was successful
    st.sidebar.success("Translation and generation complete!")

    # Layout with 2 columns
    col1, col2 = st.columns([1, 2])

    # Column 1: Translated and Generated Text
    with col1:
        st.markdown(f"""
        <div style="border: 2px solid #ff9966; padding: 15px; border-radius: 10px; background-color: #ffffff;">
        <h3 style="color: #ff5e62;">Translated English Text</h3>
        <p style="padding: 10px; background-color: #f9f9f9; border-radius: 10px;">{english_text}</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style="border: 2px solid #ff9966; padding: 15px; margin-top: 20px; border-radius: 10px; background-color: #ffffff;">
        <h3 style="color: #ff5e62;">Generated Story</h3>
        <p style="padding: 10px; background-color: #f9f9f9; border-radius: 10px;">{generated_story}</p>
        </div>
        """, unsafe_allow_html=True)

    # Column 2: Generated Image
    with col2:
        st.subheader("Generated Image")
        if isinstance(image, Image.Image):
            st.image(image, caption="Generated from your prompt", use_column_width=True, output_format="JPEG")
        else:
            st.error(image)

# Sidebar Tips
st.sidebar.markdown("### Tips for Best Results:")
st.sidebar.markdown("""
    - Keep **Max Tokens** between 50-150 for concise stories.
    - Use **Temperature** around 0.7 for creative but coherent outputs.
    - Longer text inputs generate more detailed stories.
""")

# Footer Section
st.markdown("""
    <style>
    .footer {
        position: fixed;
        bottom: 0;
        width: 100%;
        background-color: #2c3e50;
        color: white;
        text-align: center;
        padding: 10px;
        border-top: 2px solid #ff5e62;
    }
    </style>
    <div class="footer">
        Made with ❤️ by YASH | Contact: yashwantmanish@gmail.com
    </div>
    """, unsafe_allow_html=True)

# Add animation to buttons
st.markdown("""
    <style>
    .stButton > button:hover {
        background-color: #ff5e62;
        color: white;
        transition: background-color 0.3s ease, color 0.3s ease;
    }
    </style>
""", unsafe_allow_html=True)
