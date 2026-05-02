import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="AI Workout Planner", layout="centered")

st.title("🏋️ AI Workout Plan Maker")

API_KEY = st.secrets['gemini_api_key']

genai.configure(api_key=API_KEY)

# ====== USER INPUTS ======
st.header("Your Details")

col1, col2 = st.columns(2)

with col1:
    days_per_week = st.slider("How many days per week?", 1, 7, 3)
    time_per_session = st.slider("Minutes per session", 20, 120, 60)

with col2:
    fitness_level = st.selectbox("Fitness Level", ["Beginner", "Intermediate", "Advanced"])
    goal = st.selectbox("Fitness Goal", ["Build Muscle", "Lose Fat", "Stay Fit", "Increase Strength"])

injuries = st.text_area("Any injuries or limitations?")

photo = st.file_uploader("Upload your body photo (optional)", type=["jpg", "jpeg", "png"])


if st.button("Generate Workout Plan", type='primary'):
    if not API_KEY:
        st.error("Please enter your Gemini API key.")
    else:
        with st.spinner("Generating your plan..."):
            model = genai.GenerativeModel("gemini-3.1-flash-lite-preview")

            prompt = f"""
            Create a detailed weekly workout plan.

            User Info:
            - Days per week: {days_per_week}
            - Time per session: {time_per_session} minutes
            - Fitness level: {fitness_level}
            - Goal: {goal}
            - Injuries: {injuries}

            Requirements:
            - Split workouts per day
            - Include exercises, sets, reps
            - Include rest times
            - Keep it simple and clear
            - Adapt to injuries if mentioned
            """

            try:
                response = model.generate_content(prompt)
                plan = response.text

                st.subheader("Your AI Workout Plan")
                st.write(plan)

                if photo:
                    st.info("Photo uploaded. (Advanced body analysis can be added later)")

            except Exception as e:
                st.error(f"Error: {e}")