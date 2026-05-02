import streamlit as st
import psycopg
import datetime as dt
# database connection
db_password = st.secrets['db_password']
connection_str = st.secrets['connection_str']
try:
    connection = psycopg.connect(connection_str, sslmode="require")
    cur = connection.cursor()
    st.success('connected to database successfully')
except:
    st.error('failed to connect to the database')

# Insert data into users table
def insert_data(name, date_of_birth, email, password):
    cur.execute(
    """INSERT INTO users (name, date_of_birth, email, password)
    VALUES (%s, %s, %s, %s)""",
    (name, date_of_birth, email, password)  
    )

    connection.commit()

# sign up form
with st.form('sign up'):
    name = st.text_input('Enter your name:')

    min_date = dt.date(1980,1,1)
    max_date = dt.date.today()
    date_of_birth = st.date_input('Enter birthdate:',
            min_value=min_date,
             max_value=max_date )
    email = st.text_input('Enter your email:')
    password = st.text_input('Enter your password', type='password')

    submit = st.form_submit_button('Create account',
                                   use_container_width=True, type='primary')

    if submit:
        insert_data(name, date_of_birth, email, password)
        st.success('Account created Successfully!')
        st.switch_page("pages/sign_in.py")
        init_user(name)