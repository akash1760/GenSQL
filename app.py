from dotenv import load_dotenv

load_dotenv()

import streamlit as st
import os
import sqlite3
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(question, prompt):
    model= genai.GenerativeModel('gemini-pro')
    response = model.generate_content([prompt[0], question])
    return response.text


def read_sql_query(sql, db):
    conn= sqlite3.connect(db)
    cur=conn.cursor()
    cur.execute(sql)
    rows= cur.fetchall()
    conn.commit()
    conn.close()

    for row in rows:
        print(row)
    return rows



prompt=[""""
        You are an expert in converting English questions to SQL query!
    The SQL database has the name STUDENT and has the following columns - NAME, CLASS, 
    SECTION \n\nFor example,\nExample 1 - How many entries of records are present?, 
    the SQL command will be something like this SELECT COUNT(*) FROM STUDENT ;
    \nExample 2 - Tell me all the students studying in Data Science class?, 
    the SQL command will be something like this SELECT * FROM STUDENT 
    where CLASS="Data Science"; 
    also the sql code should not have ``` in beginning or end and sql word in output
        """]




st.set_page_config(page_title= "I can retrieve Any SQL query")

st.markdown("""
    <style>
        body {
            background-color: #f7f7f7;
            font-family: 'Arial', sans-serif;
        }
        .main {
            width: 80%;
            margin: 0 auto;
            padding: 20px;
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            padding: 12px 20px;
            font-size: 16px;
            border-radius: 5px;
            cursor: pointer;
        }
        .stButton>button:hover {
            background-color: #45a049;
        }
    </style>
""", unsafe_allow_html=True)

with st.container():
    st.header("Gemini app to retrieve SQL data")
    question= st.text_input("Enter your question", key="input")
    submit=st.button("Ask the question")


# if submit:
#     response= get_gemini_response(question, prompt)
#     print(response)
#     data= read_sql_query(response, 'student.db')
#     st.subheader("The response is")
#     for row in data:
#         print(row)
#         st.header(row)
if submit:
    with st.spinner('Generating SQL query...'):
        response = get_gemini_response(question, prompt)
        data = read_sql_query(response, 'student.db')

    st.subheader("SQL Query:")
    st.markdown(f"```sql\n{response}\n```")

    st.subheader("SQL Query Results:")
    for row in data:
        if len(row) >= 3:
            st.write(f"**{row[0]}** - {row[1]} - {row[2]}")
        else:
            st.write(f"Row does not have enough columns: {row}")
