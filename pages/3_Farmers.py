import streamlit as st
import pandas as pd
import mysql.connector

# Function to establish a MySQL connection
def connect_to_mysql():
    return mysql.connector.connect(
        host="192.168.82.27",
        user="root",
        password="",
        database="mydb"
    )

# Function to get the list of users from the user table
def get_user_list():
    connection = connect_to_mysql()
    cursor = connection.cursor(dictionary=True)

    # SQL statement to select all users
    select_query = "SELECT * FROM user;"

    cursor.execute(select_query)
    users = cursor.fetchall()

    cursor.close()
    connection.close()

    return users

# Function to show the list of users
def show_user_list(users):
    st.title("Farmers List")
    if not users:
        st.write("No users found.")
    else:
        # Display the list of users in a DataFrame
        user_df = pd.DataFrame(users)
        st.dataframe(user_df)

users=get_user_list()
show_user_list(users)
