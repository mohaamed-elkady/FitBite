import streamlit as st
import google.generativeai as genai

genai.configure(api_key=st.secrets['gemini_api_key'])
model = genai.GenerativeModel('gemini-3.1-flash-lite-preview')

st.set_page_config(page_title="Smart Kitchen", page_icon="🍲", layout="wide")
st.markdown("# 🍲 Smart Kitchen Recipe Generator")
st.markdown("**Turn fridge leftovers into healthy meals**")

# Header
st.markdown("---")
col1, col2 = st.columns([1, 3])
with col1:
    st.markdown("### 📝 **Input**")
with col2:
    st.markdown("### 🎯 **Your Goals**")

# Inputs
col_a, col_b = st.columns(2)
with col_a:
    ingredients = st.text_area("",
                              placeholder=" Tell me your left overs: chicken, rice, broccoli, eggs...",
                              height=200,
                              label_visibility="collapsed")
with col_b:
    goals = st.text_area("",
                        placeholder="high protein, low carb, 500 calories, keto...",
                        height=200,
                        label_visibility="collapsed")

# Generate
if st.button("**✨ Generate Recipe**", type="primary", use_container_width=True):
    if ingredients and goals:
        with st.spinner("Cooking up your recipe... 🍳"):
            prompt = f"""Create healthy recipe using ONLY these ingredients: {ingredients}
            Nutrition goals: {goals}

            Format exactly:
            # {chr(127866)} Recipe Title
            ## Ingredients
            - list

            ## Instructions (5 steps max)
            1. ...

            ## Nutrition (per serving)
            - Calories:
            - Protein: g
            - Carbs: g  
            - Fat: g

            ## Why Perfect For You 💚"""
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.download_button("📥 Save Recipe", response.text, "recipe.md")
    else:
        st.warning("Add ingredients + goals!")

st.markdown("---")
st.caption("Powered by Gemini AI")