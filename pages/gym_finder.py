import streamlit as st
import google.generativeai as genai
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

# Configure Gemini API

genai.configure(api_key=st.secrets['gemini_api_key'])
model = genai.GenerativeModel("gemini-3.1-flash-lite-preview")

# Functions

def parse_gyms(text):
    if not text:
        return []

    gyms = text.split("---")
    gym_list = []

    for gym in gyms:
        details = {}
        lines = gym.strip().split("\n")

        for line in lines:
            if ":" in line:
                key, value = line.split(":", 1)
                details[key.strip()] = value.strip()

        if details:
            gym_list.append(details)

    return gym_list

# Session State

if "result" not in st.session_state:
    st.session_state.result = None

st.title("🏋️ AI Gym Finder")

col1, col2 = st.columns(2)
with col1:
    location = st.text_input("Enter your area (e.g. Maadi, Nasr City)")
    goal = st.selectbox("Your goal", ["Weight Loss", "Muscle Gain", "General Fitness"])
with col2:
    number_of_gyms = st.segmented_control('How many gyms do you want recommended?',
            [1, 2, 3, 4, 5])
    price = st.selectbox('What is your budget?',
            ['Budget Friendly', 'Moderate', 'Premium' ])

if st.button("Find Gyms", type="primary"):
    if location:

        with st.spinner("🔍 Finding the best gyms for you... Please wait"):

            prompt = f"""
            Give {number_of_gyms} gyms in {location}, Egypt.
            Gym Name:
            Area:
            Rating:
            Description:
            Best For:
            Use "---" between gyms
            Do NOT skip any fields
            """

# ✅ Save Results

    response = model.generate_content(prompt)
    st.session_state.result = response.text  

else:
    st.warning("⚠️ Please enter a location first!")
gyms = parse_gyms(st.session_state.result)

if st.session_state.result:

    st.success("✅ Results ready!")
    st.subheader("📍 Recommended Gyms")

    gyms = parse_gyms(st.session_state.result)

    # 🔥 Show cards
    for gym in gyms:
        with st.container():
            st.markdown(f"### 🏋️ {gym.get('Gym Name', 'Unknown')}")
            st.markdown(f"📍 **Area:** {gym.get('Area', '-')}")
            st.markdown(f"⭐ **Rating:** {gym.get('Rating', '-')}")
            st.markdown(f"📝 **Description:** {gym.get('Description', '-')}")
            st.markdown(f"🎯 **Best For:** {gym.get('Best For', '-')}")
            st.markdown("---")

# PDF Maker

buffer = BytesIO()
doc = SimpleDocTemplate(buffer)
styles = getSampleStyleSheet()

content = []

content.append(Paragraph("Your Recommended Gyms Report", styles["Title"]))
content.append(Spacer(1, 20))

# Loop for all gyms

for gym in gyms:
    content.append(Paragraph(f"<b>Gym Name:</b> {gym.get('Gym Name', '-')}", styles["Normal"]))
    content.append(Paragraph(f"<b>Area:</b> {gym.get('Area', '-')}", styles["Normal"]))
    content.append(Paragraph(f"<b>Rating:</b> {gym.get('Rating', '-')}/5", styles["Normal"]))
    content.append(Paragraph(f"<b>Description:</b> {gym.get('Description', '-')}", styles["Normal"]))
    content.append(Paragraph(f"<b>Best For:</b> {gym.get('Best For', '-')}", styles["Normal"]))

# Spacing between recommended gyms

    content.append(Spacer(1, 15))
    content.append(Paragraph("--------------------------------------------------", styles["Normal"]))
    content.append(Spacer(1, 15))

# Do it only once

doc.build(content)
buffer.seek(0)

st.download_button(
    label="📄 Download PDF",
    data=buffer,
    file_name="gym_report.pdf",
    mime="application/pdf",
    key="gym_pdf_download_v1"
)