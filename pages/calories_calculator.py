# 1. Importing extensions
import streamlit as st
import google.generativeai as ai
from PIL import Image


# 2. Connecting to Gemini API
gemini_client = ai.configure(api_key=st.secrets['gemini_api_key'])
gemini_model = ai.GenerativeModel(model_name='gemini-3.1-flash-lite-preview')

# 4. Page title and description
st.title("Calorie Calculator 🔥")
st.write("Describe your food or upload a photo to get a rough calorie estimate!")
st.divider()

# 5. Creating two tabs for text and image input
text_tab, image_tab = st.tabs(["Enter Food as Text 📝", "Upload Food Image 📷"])

# 6. Text input tab using Groq
with text_tab:
    st.subheader("Describe Your Food")
    st.info("Type what you ate and roughly how much. The AI will give you a general estimate, not an exact count.")

    food_text = st.text_area(
        label="What did you eat?",
        placeholder="e.g. a plate of rice with grilled chicken and salad",
        height=120
    )

    portion_note = st.text_input(
        label="Any extra notes about the portion or cooking? (optional)",
        placeholder="e.g. large portion, fried in oil, restaurant serving"
    )

    text_button = st.button(label="Estimate Calories", type="primary")

    if text_button:
        if food_text == "":
            st.error("Please enter a food description first!")
        else:
            with st.spinner("Analyzing your food, please wait..."):

                # 7. Building the prompt for text input
                prompt = (
                    "You are a friendly nutrition helper. The user described this food: " + food_text + ". "
                    + ("Extra notes: " + portion_note + ". " if portion_note else "") +
                    "Give a rough general calorie estimate. "
                    "Use only round numbers, for example around 350 kcal not 347 kcal. "
                    "Provide: "
                    "1. Each food item with a rough rounded calorie estimate. "
                    "2. A total rounded calorie estimate for the full meal. "
                    "3. A very general idea of protein, carbs, and fats in round numbers. "
                    "4. One short friendly tip about the meal. "
                    "Keep it simple and remind the user these are rough estimates only, not precise values."
                )

                # 8. Sending prompt to Groq and showing response
                response = gemini_model.generate_content(prompt)

                st.divider()
                st.subheader("Calorie Estimate")
                st.write(response.text)
                st.success("Done! Remember these are rough estimates only.")

# 9. Image input tab using Gemini
with image_tab:
    st.subheader("Upload a Food Photo")
    st.info("Upload a clear photo of your meal. Gemini will look at it and give you a rough calorie estimate.")

    uploaded_image = st.file_uploader(
        label="Choose a food image",
        type=["jpg", "jpeg", "png"]
    )

    extra_context = st.text_input(
        label="Any extra context about the food? (optional)",
        placeholder="e.g. homemade, large portion, street food"
    )

    image_button = st.button(label="Estimate Calories from Image")

    if uploaded_image is not None:
        st.image(uploaded_image, caption="Your uploaded food photo")

    if image_button:
        if uploaded_image is None:
            st.error("Please upload a food image first!")
        else:
            with st.spinner("Analyzing your food image, please wait..."):

                # 10. Opening the image and building the prompt
                image = Image.open(uploaded_image)

                prompt = (
                    "You are a friendly nutrition helper. Look at this food image and give a rough calorie estimate. "
                    + ("Extra context from the user: " + extra_context + ". " if extra_context else "") +
                    "Use only round numbers, for example around 400 kcal not 392 kcal. "
                    "Provide: "
                    "1. A list of the food items you can see in the image. "
                    "2. A rough rounded calorie estimate for each item. "
                    "3. A total rounded calorie estimate for the full meal. "
                    "4. A very general macronutrient overview in round numbers. "
                    "5. One short friendly tip. "
                    "If the image is unclear, give your best guess and say so. "
                    "Remind the user these are rough visual estimates only."
                )

                # 11. Sending image and prompt to Gemini and showing response
                response = gemini_model.generate_content(
                    contents=[prompt, image]
                )

                st.divider()
                st.subheader("Calorie Estimate")
                st.write(response.text)
                st.success("Done!")