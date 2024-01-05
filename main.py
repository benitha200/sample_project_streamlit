import streamlit as st
import mysql.connector
import pandas as pd

# Function to establish a MySQL connection
def connect_to_mysql():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="mydb"
    )

# Function to create the user table if it doesn't exist
def create_user_table():
    connection = connect_to_mysql()
    cursor = connection.cursor()

    # SQL statement to create the user table
    create_table_query = """
    CREATE TABLE IF NOT EXISTS user (
        id INT AUTO_INCREMENT,
        first_name VARCHAR(255),
        last_name VARCHAR(255),
        age INT,
        email VARCHAR(255),
        PRIMARY KEY (id)
    );
    """

    cursor.execute(create_table_query)
    connection.commit()

    cursor.close()
    connection.close()

# Function to create the transactions table if it doesn't exist
def create_transactions_table():
    connection = connect_to_mysql()
    cursor = connection.cursor()

    # SQL statement to create the transactions table
    create_table_query = """
    CREATE TABLE IF NOT EXISTS transactions (
        id INT AUTO_INCREMENT,
        user_id INT,
        quantity INT,
        unit_price FLOAT,
        transport FLOAT,
        total_price FLOAT,
        coffee_category VARCHAR(255),
        PRIMARY KEY (id),
        FOREIGN KEY (user_id) REFERENCES user(id)
    );
    """

    cursor.execute(create_table_query)
    connection.commit()

    cursor.close()
    connection.close()

def show_user_details():
    st.title("User Details")
    st.write("Please fill in your details:")
    
    # Form to collect user details
    with st.form("user_details_form"):
        first_name = st.text_input("First Name")
        last_name = st.text_input("Last Name")
        age = st.number_input("Age", min_value=0, max_value=150)
        email = st.text_input("Email")
        
        submit_button = st.form_submit_button("Submit")
    if submit_button:
        insert_user_details(first_name, last_name, age, email)
        st.success("User Details Submitted!")

# Function to insert user details into the user table
def insert_user_details(first_name, last_name, age, email):
    connection = connect_to_mysql()
    cursor = connection.cursor()

    # SQL statement to insert user details
    insert_query = """
    INSERT INTO user (first_name, last_name, age, email)
    VALUES (%s, %s, %s, %s);
    """

    cursor.execute(insert_query, (first_name, last_name, age, email))
    connection.commit()

    cursor.close()
    connection.close()

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
    st.title("User List")
    if not users:
        st.write("No users found.")
    else:
        # Display the list of users in a DataFrame
        user_df = pd.DataFrame(users)
        st.dataframe(user_df)

# Function to export user details to a CSV file
def export_to_csv(users):
    if not users:
        st.warning("No users to export.")
        return

    # Convert user data to a DataFrame
    user_df = pd.DataFrame(users)

    # Create a download link for the CSV file
    csv_file = user_df.to_csv(index=False)
    st.download_button(
        label="Export to CSV",
        data=csv_file,
        file_name="user_list.csv",
        key="csv_export_button"
    )

# Function to upload user data from an Excel file
def upload_user_data():
    uploaded_file = st.file_uploader("Upload file (CSV or Excel)", type=["csv", "xlsx", "xls"])
    if uploaded_file is not None:
        # Read the file into a DataFrame based on file type
        if uploaded_file.type == "application/vnd.ms-excel" or uploaded_file.type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
            user_data = pd.read_excel(uploaded_file)
        elif uploaded_file.type == "text/csv":
            user_data = pd.read_csv(uploaded_file)
        else:
            st.error("Unsupported file format. Please upload a CSV or Excel file.")
            return

        # Ensure the required columns are present
        required_columns = ["first_name", "last_name", "age", "email"]
        if not set(required_columns).issubset(user_data.columns):
            st.error(f"Required columns {required_columns} not found in the uploaded file.")
            return

        # Skip entries where the ID already exists in the database
        user_data = user_data[~user_data["id"].isin(get_user_ids())]

        # Insert user data into the database
        for _, row in user_data.iterrows():
            insert_user_details(row["first_name"], row["last_name"], row["age"], row["email"])

        st.success(f"Successfully uploaded user data from the file.")

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
    select_query = "SELECT * FROM transactions;"

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

# Ensure the user and transactions tables exist
create_user_table()
create_transactions_table()

# Navigation
nav_option = st.sidebar.radio("Navigation", ["Home", "User Details", "User List", "Upload Users", "Transactions"])

# Display content based on navigation choice
if nav_option == "Home":
    st.title("Home Page")
    st.write("Welcome to the Streamlit App!")
    st.write("Use the navigation to explore different sections.")
elif nav_option == "User Details":
    show_user_details()
elif nav_option == "User List":
    users = get_user_list()
    show_user_list(users)
    export_to_csv(users)
elif nav_option == "Upload Users":
    upload_user_data()
elif nav_option == "Transactions":
    # Show transactions form
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
