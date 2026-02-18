# ==========================================
# AutoSage AI - Vehicle Image Analyzer
# ==========================================

import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
from PIL import Image

# ---------------------------
# Load API Key
# ---------------------------
print("App is running/rerunning...")
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# ---------------------------
# Gemini Function
# ---------------------------
from google.api_core import exceptions, retry

def get_gemini_response(prompt, image_parts):
    model = genai.GenerativeModel("gemini-2.5-flash")
    try:
        response = model.generate_content(
            [prompt, image_parts[0]],
            request_options={'retry': retry.Retry(total=0), 'timeout': 30}
        )
        return response.text
    except exceptions.ResourceExhausted:
        return "Error: API Quota Exceeded. Please try again later or use a different API key."
    except Exception as e:
        return f"An error occurred: {str(e)}"

# ---------------------------
# Image Processing
# ---------------------------
def input_image_setup(uploaded_file):
    if uploaded_file is None:
        return None

    bytes_data = uploaded_file.getvalue()

    image_parts = [{
        "mime_type": uploaded_file.type,
        "data": bytes_data
    }]
    return image_parts

# ---------------------------
# Prompt
# ---------------------------
input_prompt = """
You are a professional automobile expert AI.

Analyze the uploaded vehicle image and give:

1. Brand
2. Model Name (guess if unsure)
3. Vehicle Type (Bike/Car/Scooter/SUV)
4. Engine Capacity (approx CC)
5. Mileage (approx km/l)
6. Price Range in India
7. Launch Year (approx)
8. Top 5 Key Features
9. Suitable For (city/highway/family/offroad)
10. Short Review

Give answer in clean bullet points.
"""

# ---------------------------
# Streamlit UI
# ---------------------------
st.set_page_config(page_title="AutoSage AI", page_icon="🚗")

st.title("🚗 AutoSage - Vehicle Expert AI")
st.write("Upload any vehicle image and get full vehicle information instantly!")

uploaded_file = st.file_uploader("Upload Vehicle Image", type=["jpg","jpeg","png"])

# Show uploaded image
if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

# Analyze button
if st.button("🔍 Analyze Vehicle"):
    print("Button clicked!")

    if uploaded_file is None:
        st.warning("Please upload an image first!")
    else:
        with st.spinner("AI is analyzing vehicle..."):
            print("Starting analysis...")
            image_data = input_image_setup(uploaded_file)
            print("Image processed.")
            response = get_gemini_response(input_prompt, image_data)
            print("Response received.")

        st.subheader("📊 Vehicle Details")
        st.write(response)
        st.success("Analysis Completed Successfully!")
