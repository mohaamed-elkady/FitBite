import streamlit as st
from PIL import Image, ImageDraw

# Styling ( extra touch )

st.markdown("""
<style>
    img {
        border-radius: 50%;
        border: 3px solid #4CAF50;
    }
    div[data-testid="stVerticalBlock"] > div {
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# How to make the photos in a circular way

def make_circle(img_path):
    img = Image.open(img_path).convert("RGB")
    size = min(img.size)
    
    mask = Image.new("L", (size, size), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, size, size), fill=255)

    img = img.resize((size, size))
    output = Image.new("RGB", (size, size))
    output.paste(img, (0, 0), mask)

    return output

st.title("👥 Meet the Minds Behind the App")
st.subheader('AI Nutrition Helper was built by a small but passionate team of students who share a strong interest in artificial intelligence, health, and real-world problem solving')

# Columns for every single teammate and a small description 

col1, col2, col3 = st.columns(3)

with col1:
    st.image(make_circle("images/Mohamed.png"), use_container_width=True)
    st.subheader("Co-Founder: Mohamed Abdelhamid")

with col2:
    st.image(make_circle("images/Mahmoud.png"), use_container_width=True)
    st.subheader("CEO: Mahmoud Mohamed")

with col3:
    st.image(make_circle("images/Yassin.png"), use_container_width=True)
    st.subheader("CTO: Yassin Hassan")

st.subheader('🚀 Our Mission')
st.write('To combine artificial intelligence with health science to help users make smarter nutrition and fitness decisions in a simple and interactive way')
st.subheader('🔭 Our Vision')
st.write('To become a leading AI-powered platform that supports healthier lifestyles through personalized recommendations and smart automation')