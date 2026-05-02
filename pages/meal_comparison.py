import streamlit as st
import google.generativeai as genai
from PIL import Image

# Set API key and gemini

genai.configure(api_key=st.secrets['gemini_api_key'])
model = genai.GenerativeModel("gemini-3.1-flash-lite-preview")

st.set_page_config(page_title="AI Meal Comparison", layout="wide")
st.title("🥗 AI Meal Comparison Tool")
st.caption("Compare meals using AI to make smarter and healthier choices 💡")

# Gemini prompt

def compare_meals_ai(meal1, meal2, goal, img1=None, img2=None):

    prompt = f"""
    You are a professional nutritionist AI.

    Compare the following two meals:

    Meal 1: {meal1}
    Meal 2: {meal2}

    User goal: {goal}

    Do the following:
    1. Estimate calories, protein, carbs, and fats for each meal
    2. Compare both meals clearly
    3. Decide which meal is better based on the goal
    4. Explain WHY in simple terms
    5. Give each meal a health score out of 10
    6. Give a short improvement tip for the LESS healthy meal

    Format EXACTLY like this:

    Meal 1:
    Calories:
    Protein:
    Carbs:
    Fat:
    Score(out of 10):

    Meal 2:
    Calories:
    Protein:
    Carbs:
    Fat:
    Score(out of 10):

    Final Verdict:
    (which meal is better and why)

    Improvement Tip:
    """

    inputs = [prompt]

    if img1:
        inputs.append(img1)
    if img2:
        inputs.append(img2)

    response = model.generate_content(inputs)
    return response.text

# Inputting meals

col1, col2 = st.columns(2)
with col1:
    st.subheader("🍽️ Meal 1")
    meal1 = st.text_input("Describe Meal 1")
    img1 = st.file_uploader("Upload Meal 1 Image", type=["jpg", "png"], key="img1")

    if img1:
        st.image(img1, caption="Meal 1 Preview", use_container_width=True)

with col2:
    st.subheader("🍽️ Meal 2")
    meal2 = st.text_input("Describe Meal 2")
    img2 = st.file_uploader("Upload Meal 2 Image", type=["jpg", "png"], key="img2")

    if img2:
        st.image(img2, caption="Meal 2 Preview", use_container_width=True)

st.divider()

goal = st.selectbox(
    "🎯 Your Goal",
    ["Weight Loss", "Muscle Gain", "Maintenance"]
)

compare_btn = st.button("🚀 Compare Meals", type="primary")

# -------------------------
# 🚀 PROCESS
# -------------------------
if compare_btn:

    if not meal1 and not img1:
        st.warning("⚠️ Please provide Meal 1 (text or image)")
    elif not meal2 and not img2:
        st.warning("⚠️ Please provide Meal 2 (text or image)")
    else:
        with st.spinner("🤖 AI is analyzing your meals..."):

            pil_img1 = Image.open(img1) if img1 else None
            pil_img2 = Image.open(img2) if img2 else None

            result = compare_meals_ai(meal1, meal2, goal, pil_img1, pil_img2)

        st.divider()
        st.markdown("## 📊 AI Nutrition Analysis")

        # Format text nicely
        formatted = result.replace("\n", "<br>")
        st.markdown(formatted, unsafe_allow_html=True)

        # Extract and highlight verdict
        if "Final Verdict:" in result:
            verdict = result.split("Final Verdict:")[-1].split("Improvement Tip:")[0]
            st.success(f"🏆 {verdict.strip()}")

        # Extract and highlight tip
        if "Improvement Tip:" in result:
            tip = result.split("Improvement Tip:")[-1]
            st.info(f"💡 {tip.strip()}")