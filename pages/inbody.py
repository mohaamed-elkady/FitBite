import streamlit as st

st.title("💪 AI Fitness & Health Planner")

# USER INPUT

st.header("Enter Your Details")

age = st.number_input("Age", step=1.0, min_value=10.0, max_value=80.0)
weight = st.number_input("Weight (kg)", step=0.5, min_value=35.0)
height = st.number_input("Height (cm)", step=0.5, min_value=100.0, max_value=250.0)
gender = st.selectbox("Gender", ["Male", "Female"])
goal = st.selectbox("Goal", ["Lose Weight", "Gain Muscle", "Maintain"])
activity = st.selectbox("Exercise Frequency", ["None", "1-2 times/week", "3-4 times/week", "5+ times/week"])

# CALCULATIONS

if st.button("Calculate My Plan", type="primary"):

    # BMI
    height_m = height / 100
    bmi = weight / (height_m ** 2)

    # Body Fat %
    gender_value = 1 if gender == "Male" else 0
    body_fat = (1.2 * bmi) + (0.23 * age) - (10.8 * gender_value) - 5.4

    # Lean Mass
    lean_mass = weight * (1 - body_fat / 100)

    # Water Intake
    water = weight * 35  # ml

    # Adjust water
    if activity != "None":
        water += 500

    # Fitness Level
    if activity == "None":
        level = "Beginner"
    elif activity == "1-2 times/week":
        level = "Beginner"
    elif activity == "3-4 times/week":
        level = "Intermediate"
    else:
        level = "Advanced"


    # OUTPUT PART 3
   
    st.subheader("📊 Your Body Stats")

    st.write(f"**BMI:** {bmi:.2f}")
    st.write(f"**Body Fat %:** {body_fat:.2f}%")
    st.write(f"**Lean Mass:** {lean_mass:.2f} kg")
    st.write(f"**Water Intake:** {water:.0f} ml/day")
    st.write(f"**Fitness Level:** {level}")
