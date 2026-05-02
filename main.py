# 1. Importing streamlit 
import streamlit as st

st.sidebar.title('Welcome')

# 2. Creating app pages
calories_page = st.Page(
    page='pages/calories_calculator.py',
    title='Calories Calculator',
    icon='🔥'
)

exercises_page = st.Page(
    page='pages/exercises_creator.py',
    title='Exercises Maker',
    icon='💪'
)

gym_page = st.Page(
    page='pages/gym_finder.py',
    title='Gym Finder',
    icon='🏋️'
)

inbody_page = st.Page(
    page='pages/inbody.py',
    title='InBody Analysis',
    icon='📊'
)

leftover_page = st.Page(
    page='pages/leftover_chef.py',
    title='Leftover Chef',
    icon='🍳'
)

signup_page = st.Page(
    page='pages/sign_up.py',
    title='Sign Up',
    icon='👤'
)

signin_page = st.Page(
    page='pages/sign_in.py',
    title='Sign In',
    icon='🔐'
)

chatbot_page = st.Page(
    page='pages/nutrition_chatbot.py',
    title='Nutrition Chatbot',
    icon='🤖'
)

planner_page = st.Page(
    page='pages/nutrition_planner.py',
    title='Nutrition Planner',
    icon='🥗'
)
about_us = st.Page(
page='pages/about_us.py',
title='About Us',
icon='🧑‍🤝‍🧑'
)
contact_us = st.Page(
    page='pages/contact_us.py',
    title='Contact Us',
    icon='📞'
)
meal_comparison = st.Page(
    page='pages/meal_comparison.py',
    title='Meal Comparison',
    icon='🥗'
)

# 3. Creating the navbar
all_pages = st.navigation(
    pages={
        '👤 Login': [signup_page, signin_page],
        '🏋️‍♀️ Fitness': [exercises_page, gym_page, inbody_page,],
        '🍽️ Eat Smarter': [calories_page, meal_comparison, leftover_page],
        '✨ Chat with AI': [chatbot_page, planner_page],
        '🧑‍🤝‍🧑 About Us': [about_us, contact_us]
    },
    position='top'
)

all_pages.run()