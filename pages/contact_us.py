import streamlit as st

# Extra styling
st.markdown("""
<style>
    div[data-testid="stForm"] {
        border: 1px solid #ddd;
        padding: 20px;
        border-radius: 15px;
        background-color: #f9f9f9;
    }
</style>
""", unsafe_allow_html=True)

st.title("📞 Contact Us")
st.write("If you face any issues or have questions, please feel free to reach out to us and we will get back to you as soon as possible!")

# Team contact information

st.subheader("👥 Our Team")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("Mohamed Abdelhamid")
    st.write("Co-Founder")
    st.write("📧 mohamedabdelhamidelkady@gmail.com")
    st.write("📞 +20 109 480 3101")

with col2:
    st.markdown("Mahmoud Mohamed")
    st.write("CEO")
    st.write("📧 mehrammahmoud156@gmail.com")
    st.write("📞 +20 111 749 0400")

with col3:
    st.markdown("Yassin Hassan")
    st.write("CTO")
    st.write("📧 yassinhassan657@gmail.com")
    st.write("📞 +20 107 081 6942")

# Send us a message if urgent

import streamlit as st
import psycopg

# Your existing database connection string

connection_str = "postgresql://postgres.xszpfapfnctuztlqmbdi:dbGXo0tbOXKsP9cx@aws-0-eu-west-1.pooler.supabase.com:5432/postgres"

# Function to save message to database

def save_message(name, email, message):
    conn = psycopg.connect(connection_str, sslmode="require")
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO contact_messages (name, email, message)
        VALUES (%s, %s, %s)
        """,
        (name, email, message)
    )

    conn.commit()
    cur.close()
    conn.close()


# User Interface

st.title("Contact Us")

st.write("Send us a message and we will get back to you.")

name = st.text_input("Your Name")
email = st.text_input("Your Email")
message = st.text_area("Your Message")

if st.button("Send Message"):
    if name and email and message:
        try:
            save_message(name, email, message)
            st.success("✅ Your message has been sent successfully!")
        except Exception as e:
            st.error(f"❌ Something went wrong: {e}")
