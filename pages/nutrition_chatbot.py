import streamlit as st
import google.generativeai as genai

genai.configure(api_key=st.secrets['gemini_api_key'])
model = genai.GenerativeModel('gemini-3.1-flash-lite-preview')

st.set_page_config(page_title="Nutritionist", page_icon="🥗", layout="wide")
st.markdown("# 🥗 Virtual AI Nutritionist")
st.markdown("**Your 24/7 nutrition coach**")

# Sidebar profile
with st.sidebar:
    st.markdown("### 👤 **Quick Profile**")
    goals = st.text_input("Goals:", placeholder="weight loss, muscle gain")
    diet = st.text_input("Diet:", placeholder="vegan, keto, balanced")
    allergies = st.text_input("Allergies:", placeholder="nuts, dairy")

    # Save properly
    st.session_state.goals = goals
    st.session_state.diet = diet
    st.session_state.allergies = allergies

    st.info(f"**Active:** Goals: {goals} | Diet: {diet} | Allergies: {allergies}")

# Initialize chat
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi! I'm your nutritionist. Tell me your goals or ask for meal ideas! 💪"}
    ]

# ✅ FIX: Convert to Gemini format
def convert_messages(messages):
    converted = []
    for msg in messages:
        role = "model" if msg["role"] == "assistant" else "user"
        converted.append({
            "role": role,
            "parts": [{"text": msg["content"]}]
        })
    return converted

# Display chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Profile context
profile = f"Goals: {st.session_state.get('goals', '')} | Diet: {st.session_state.get('diet', '')} | Allergies: {st.session_state.get('allergies', '')}"
system_prompt = f"Expert nutritionist. User: {profile}. Give precise macros, evidence-based advice, encouraging tone."

# Chat input
if prompt := st.chat_input("Ask about meals, plans, macros..."):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # ✅ FIX: use converted history
        chat = model.start_chat(history=convert_messages(st.session_state.messages[:-1]))

        response = chat.send_message(system_prompt + "\nUser: " + prompt)

        st.markdown(response.text)

        st.session_state.messages.append({
            "role": "assistant",
            "content": response.text
        })

# Footer
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🔄 New Chat", use_container_width=True):
        st.session_state.messages = [
            {"role": "assistant", "content": "New chat! What's your nutrition goal?"}
        ]
        st.rerun()

with col2:
    if st.button("📤 Export", use_container_width=True):
        chat_md = "\n\n".join(
            [f"**{m['role'].title()}:** {m['content']}" for m in st.session_state.messages]
        )
        st.download_button("Save", chat_md, "chat.md", use_container_width=True)

with col3:
    st.empty()

st.caption("✨ Gemini AI Nutritionist")