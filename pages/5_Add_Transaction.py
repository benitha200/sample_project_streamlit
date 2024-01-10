import streamlit as st
import mysql.connector
import pandas as pd

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

# Function to insert transaction details into the transactions table
def insert_transaction_details(user_id, quantity, unit_price, transport, total_price, coffee_category):
    connection = connect_to_mysql()
    cursor = connection.cursor()

    # SQL statement to insert transaction details
    insert_query = """
    INSERT INTO transactions (user_id, quantity, unit_price, transport, total_price, coffee_category)
    VALUES (%s, %s, %s, %s, %s, %s);
    """

    cursor.execute(insert_query, (user_id, quantity, unit_price, transport, total_price, coffee_category))
    connection.commit()

    cursor.close()
    connection.close()

# Function to show the list of transactions
def show_transactions_list(transactions):
    st.title("Transactions List")
    if not transactions:
        st.write("No transactions found.")
    else:
        # Display the list of transactions in a DataFrame
        transactions_df = pd.DataFrame(transactions)
        st.dataframe(transactions_df)

# Function to get the list of transactions from the transactions table
def get_transactions_list():
    connection = connect_to_mysql()
    cursor = connection.cursor(dictionary=True)

    # SQL statement to select all transactions
    select_query = "SELECT u.first_name,u.last_name,t.quantity, t.unit_price, t.transport, t.total_price, t.coffee_category FROM transactions t, user u where t.user_id=u.id;"

    cursor.execute(select_query)
    transactions = cursor.fetchall()

    cursor.close()
    connection.close()

    return transactions
# Function to get the list of user IDs from the user table
def get_user_ids():
    connection = connect_to_mysql()
    cursor = connection.cursor()

    # SQL statement to select all user IDs
    select_query = "SELECT id FROM user;"

    cursor.execute(select_query)
    user_ids = [row[0] for row in cursor.fetchall()]

    cursor.close()
    connection.close()

    return user_ids

st.title("Transactions")
st.write("Please fill in transaction details:")
    
    # Get the list of users for the combo box
users = get_user_list()
user_names = [f"{user['id']} - {user['first_name']} {user['last_name']}" for user in users]
selected_user = st.selectbox("Select Farmer", user_names)

    # Extract user_id from the selected user
user_id = int(selected_user.split(" ")[0])

quantity = st.number_input("Quantity", min_value=0, value=0)
unit_price = st.number_input("Unit Price", min_value=0, value=0)
transport = st.number_input("Transport", min_value=0, value=0)
total_price = quantity * unit_price + transport
coffee_category = st.text_input("Coffee Category")

submit_transaction_button = st.button("Submit Transaction")

if submit_transaction_button:
    insert_transaction_details(user_id, quantity, unit_price, transport, total_price, coffee_category)
    st.success("Transaction Details Submitted!")

    # Show the list of transactions
    transactions = get_transactions_list()
    show_transactions_list(transactions)
