import streamlit as st
import mysql.connector
import pandas as pd
from datetime import datetime

# Function to establish a MySQL connection
def connect_to_mysql():
    return mysql.connector.connect(
        host="192.168.82.27",
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

def create_cws_table():
    connection=connect_to_mysql()
    cursor=connection.cursor()

    create_cws_table_query="""
            CREATE TABLE IF NOT EXISTS cws_table(
            cws_id INT AUTO_INCREMENT PRIMARY KEY,
            cws_name VARCHAR(255),
            cws_code VARCHAR(100)
        );
        """
    cursor.execute(create_cws_table_query)
    connection.commit()

    cursor.close()
    connection.close()

def create_farmers_table():
    connection= connect_to_mysql()
    cursor=connection.cursor()

    create_farmers_table_query="""
            CREATE TABLE IF NOT EXISTS farmer_details(
            cws_name VARCHAR(255),
            farmer_code VARCHAR(100) PRIMARY KEY,
            farmer_names VARCHAR(255),
            gender VARCHAR(255),
            age INT,
            phone_number VARCHAR(15),
            address VARCHAR(255),
            national_id VARCHAR(255),
            village VARCHAR(255),
            location VARCHAR(255)
        );
        """
    
    cursor.execute(create_farmers_table_query)
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

def get_farmers_list():
    connection= connect_to_mysql()
    cursor=connection.cursor()

    select_farmers_query="SELECT * FROM farmer_details;"
    cursor.execute(select_farmers_query)
    farmers=cursor.fetchall()

    cursor.close()
    connection.close()
    return farmers

def get_farmer_list():
    connection = connect_to_mysql()
    cursor = connection.cursor()

    select_farmers_query = "SELECT * FROM farmer_details;"
    cursor.execute(select_farmers_query)
    farmers_data = cursor.fetchall()

    # Get column names
    column_names = [desc[0] for desc in cursor.description]

    cursor.close()
    connection.close()

    # Convert the list of tuples to a list of dictionaries
    farmers = [dict(zip(column_names, row)) for row in farmers_data]

    return farmers
def get_farmers_list():
    connection= connect_to_mysql()
    cursor=connection.cursor()

    select_farmers_query="SELECT * FROM farmer_details;"
    cursor.execute(select_farmers_query)
    farmers=cursor.fetchall()

    cursor.close()
    connection.close()
    return farmers

def get_cws_list():
    connection = connect_to_mysql()
    cursor = connection.cursor()

    select_cws_query = "SELECT * FROM cws_table;"
    cursor.execute(select_cws_query)
    cws_data = cursor.fetchall()

    # Get column names
    column_names = [desc[0] for desc in cursor.description]

    cursor.close()
    connection.close()

    # Convert the list of tuples to a list of dictionaries
    cws = [dict(zip(column_names, row)) for row in cws_data]

    return cws

# Function to show the list of users
def show_user_list(users):
    st.title("User List")
    if not users:
        st.write("No users found.")
    else:
        # Display the list of users in a DataFrame
        user_df = pd.DataFrame(users)
        st.dataframe(user_df)


def show_farmers_list(farmers):
    st.title("Farmers List")
    if not farmers:
        st.write("No Farmers found.")
    else:
        # Display the list of farmers in a table with headers
        pd.DataFrame(farmers)


# Function to upload farmers data to MySQL
def upload_farmers_data():
    uploaded_file = st.file_uploader('Upload a file (CSV or Excel) with these columns ["CWS_Name","Farmer_Code", "Farmer_Name", "Gender", "Age", "Mobile_Number", "Address", "National_ID", "Village", "Location"]', type=["csv", "xlsx", "xls"])

    if uploaded_file is not None:
        if uploaded_file.type == "application/vnd.ms-excel" or uploaded_file.type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
            farmer_data = pd.read_excel(uploaded_file)
        elif uploaded_file.type == "text/csv":
            farmer_data = pd.read_csv(uploaded_file)
        else:
            st.error("Unsupported file type. Please upload a CSV or Excel file.")
            return

        # Check if required columns are present in the uploaded file
        required_columns = ["CWS_Name", "Farmer_Code", "Farmer_Name", "Gender", "Age", "Mobile_Number", "Address", "National_ID", "Village", "Location"]
        if not set(required_columns).issubset(farmer_data.columns):
            st.error(f"Required columns {required_columns} not found in the uploaded file.")
            return

        # Insert data into the MySQL table
        connection = connect_to_mysql()
        cursor = connection.cursor()

        for index, row in farmer_data.iterrows():
            # Check for NaN values and skip insertion for those rows
            if row.isnull().values.any():
                # st.warning(f"Skipping row {index + 2} due to NaN values.")
                continue

            insert_query = f"""
                INSERT INTO farmer_details (cws_name, farmer_code, farmer_names, gender, age, phone_number, address, national_id, village, location)
                VALUES ('{row['CWS_Name']}', '{row['Farmer_Code']}', '{row['Farmer_Name']}', '{row['Gender']}', {row['Age']}, '{row['Mobile_Number']}', '{row['Address']}', '{row['National_ID']}', '{row['Village']}', '{row['Location']}');
            """
            cursor.execute(insert_query)

        connection.commit()

        cursor.close()
        connection.close()
        st.success("Data uploaded successfully!")


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


def upload_cws_data():
    st.write("Ooops!!")
    uploaded_file = st.file_uploader("Upload file (CSV or Excel)", type=["csv", "xlsx", "xls"])
    if uploaded_file is not None:
        # Read the file into a DataFrame based on file type
        if uploaded_file.type == "application/vnd.ms-excel" or uploaded_file.type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
            cws_data = pd.read_excel(uploaded_file)
        elif uploaded_file.type == "text/csv":
            cws_data = pd.read_csv(uploaded_file)
        else:
            st.error("Unsupported file format. Please upload a CSV or Excel file.")
            return

        # Ensure the required columns are present
        required_columns = ["cws_code", "cws_name"]
        if not set(required_columns).issubset(cws_data.columns):
            st.error(f"Required columns {required_columns} not found in the uploaded file.")
            return

        for index, row in cws_data.iterrows():
            # Check for NaN values and skip insertion for those rows
            if row.isnull().values.any():
                # st.warning(f"Skipping row {index + 2} due to NaN values.")
                continue

            connection = connect_to_mysql()
            cursor = connection.cursor()

            insert_query = f"""
                INSERT INTO cws_table (cws_name, cws_code)
                VALUES ('{row['cws_name']}', '{row['cws_code']}');
            """

            cursor.execute(insert_query)
            connection.commit()

            cursor.close()
            connection.close()

        st.success(f"Successfully uploaded user data from the file.")

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
create_farmers_table()
create_cws_table()

# Navigation
nav_option = st.sidebar.radio("Navigation", ["Home", "User Details", "User List","Farmers List", "Upload Users", "Upload Farmers","Upload CWS","Transactions"])

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
    # export_to_csv(users)
elif nav_option == "Upload Users":
    upload_user_data()

elif nav_option=="Upload Farmers":
    upload_farmers_data()

elif nav_option=="Upload CWS":
    upload_cws_data()

elif nav_option == "User List":
    users = get_user_list()
    show_user_list(users)
    # export_to_csv(users)

elif nav_option == "Farmers List":
    farmers = get_farmer_list()
    show_farmers_list(farmers)

elif nav_option == "Transactions":
    # Show transactions form
    st.title("Transactions")
    st.write("Please fill in transaction details:")

    cws=get_cws_list()
    cws= [f" {cws_['cws_code']} ({cws_['cws_name']})" for cws_ in cws]
    selected_cws= st.selectbox("Select CWS",cws)
    selected_cws_code = selected_cws.split(' (')[0]
    st.write(selected_cws_code)
   
    farmers = get_farmer_list()
    farmer_names = [f" {farmer['farmer_names']} ({farmer['farmer_code']})" for farmer in farmers]
    selected_user = st.selectbox("Select Farmer", farmer_names)

    selected_farmer_name = selected_user.split(' (')[0]
    selected_farmer_code = selected_user.split(')')[0].split('(')[1]

    st.write(selected_farmer_name)
    st.write(selected_farmer_code)



    # user_id = int(selected_user.split(" ")[0])
    user_id =10

    date=st.date_input("Date")
    # formatted_year = date.strftime('%Y')
    last_two_digits_of_year = date.strftime('%y')
    formatted_month = date.strftime('%m')
    formatted_day = date.strftime('%d')

    quantity = st.number_input("Quantity", min_value=0, value=0)
    unit_price = st.number_input("Unit Price", min_value=0, value=0)
    transport = st.number_input("Transport", min_value=0, value=0)
    total_price = quantity * unit_price + transport
    coffee_category = st.text_input("Coffee Category")

    # Concatenate strings without spaces
    concatenated_string = str(date.strftime('%y'))+str(selected_cws_code.strip()) + str(formatted_month) + str(formatted_day) + str(coffee_category)
    batch = st.text_input(concatenated_string)

    submit_transaction_button = st.button("Submit Transaction")

    if submit_transaction_button:
        insert_transaction_details(user_id, quantity, unit_price, transport, total_price, coffee_category)
        st.success("Transaction Details Submitted!")

    # Show the list of transactions
    transactions = get_transactions_list()
    show_transactions_list(transactions)
