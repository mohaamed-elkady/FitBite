# 1. Importing extensions
import streamlit as st
import google.generativeai as genai 

genai.configure(api_key=st.secrets['gemini_api_key'])
model = genai.GenerativeModel('gemini-3.1-flash-lite-preview')

# 3. Page title and description
st.title("Nutrition Plan Generator")
st.write("Fill in your details below and we will generate a nutrition plan for you!")
st.divider()

# 4. Taking user personal information
st.subheader("1️⃣ Your Personal Information")

col1, col2, col3 = st.columns(3)

with col1:
    age = st.number_input(
        label="Enter your age:",
        min_value=5,
        max_value=100,
        step=1,
        value=25
    )

with col2:
    weight = st.number_input(
        label="Enter your weight (kg):",
        min_value=20.0,
        max_value=300.0,
        step=0.5,
        value=70.0
    )

with col3:
    height = st.number_input(
        label="Enter your height (cm):",
        min_value=100.0,
        max_value=250.0,
        step=0.5,
        value=170.0
    )

gender = st.radio(
    label="Select your gender:",
    options=["Male", "Female"],
    horizontal=True
)

# 5. Taking user lifestyle information
st.divider()
st.subheader("2️⃣ Your Lifestyle")

activity_level = st.selectbox(
    label="Select your activity level:",
    options=[
        "little or no exercise",
        "Lightly active (1 to 3 days per week)",
        "Moderately active (3 to 5 days per week)",
        "Very active (6 to 7 days per week)",
        "Super active (physical job or twice daily training)"
    ]
)

goal = st.selectbox(
    label="What is your goal?",
    options=[
        "Lose weight",
        "Maintain weight",
        "Gain muscle",
        "Improve overall health",
        "Increase energy levels"
    ]
)

diet_type = st.selectbox(
    label="Do you follow a specific diet?",
    options=[
        "No preference",
        "Vegetarian",
        "Vegan",
        "Keto",
        "Gluten-free",
        "Dairy-free"
    ]
)

meals_per_day = st.slider(
    label="How many meals do you eat per day?",
    min_value=2,
    max_value=6,
    value=3
)

allergies = st.text_input(
    label="Any food allergies or restrictions? (optional)",
    placeholder="e.g. nuts, shellfish, lactose"
)

# 6. Generating the nutrition plan when button is clicked
st.divider()
generate_button = st.button(label="Generate now!", type="primary")

if generate_button:
    with st.spinner("Generating your personalized nutrition plan, please wait..."):

        # 7. Building the prompt from user inputs
        prompt = f"""
        You are a friendly nutritionist. Create a simple daily nutrition plan for this person.

        Age: {age} years  
        Gender: {gender}  
        Weight: {weight} kg  
        Height: {height} cm  
        Activity level: {activity_level}  
        Goal: {goal}  
        Diet preference: {diet_type}  
        Meals per day: {meals_per_day}  
        Allergies or restrictions: {allergies if allergies else "None"}  

        Provide:

        1. A rough estimated daily calorie range using round numbers only (no decimals).
        2. A general macronutrient guideline in grams, rounded to the nearest 10.

        Table columns are the meal name and 5 columns for the food options:
        Each column is named (Option 1, 2, etc.)
        and must contain the food item name, allowed quantity, calories in 3 different line 

        Meal plan requirements:
        - Include common meals (Breakfast, Lunch, Dinner, Snacks).
        - Each meal must include a variety of foods such as proteins, carbs, healthy fats, fruits, and vegetables.
        - Food options should be diverse (e.g., eggs, yogurt, oats, chicken, fish, rice, bread, legumes, fruits, nuts, etc.).
        - Keep calorie estimates simple and rounded (e.g., 100 kcal, 250 kcal).
        - Make the table clean, readable, and well-structured.

        4. Two or three simple, practical tips aligned with the user’s goal.

        Guidelines:
        - Keep all numbers rounded and easy to understand.
        - Be friendly, encouraging, and easy to read.
        - Add a short disclaimer at the end stating that these are general estimates and not medical advice.
        """

        # 8. Sending the prompt to Groq and displaying the response
        response = model.generate_content(prompt)

        st.divider()
        st.subheader("Your complete nutrition plan 📋")
        st.write(response.choices[0].message.content)
        st.success("Plan generated successfully!")