📦 Courier Management System

A modern, user-friendly desktop application for managing courier services, built with Python, CustomTkinter, and MySQL.
This system provides a complete solution with role-based access for administrators, employees, and clients — all within a single, seamless interface.

📑 Table of Contents

Key Features

Technologies Used

Screenshots

Prerequisites

Setup and Installation

How to Use

Default Login Credentials

Project Structure

🚀 Key Features

✅ Modern & Intuitive GUI – Visually appealing interface built with CustomTkinter
✅ Unified Single-Window Interface – Seamless navigation between pages
✅ Role-Based Access Control

Admin Dashboard – Manage users (CRUD) & view all courier records

Employee Dashboard – View & update status of assigned couriers

Client Dashboard – Book shipments & track existing ones
✅ Secure User Authentication – Separate login & registration for each role
✅ Complete Courier Management – Full CRUD operations on courier data
✅ Persistent Data Storage – MySQL backend to store user data & tracking history
✅ Styled & Themed Interface – Light/Dark theme support with consistent widget styling

🛠 Technologies Used

Backend: Python

Database: MySQL

GUI Framework: CustomTkinter

Connector: mysql-connector-python


📋 Prerequisites

Before you begin, make sure you have:

Python 3.7+

MySQL Server 8.0+

⚙️ Setup and Installation
1️⃣ Clone the Repository
git clone <your-repository-url>
cd CourierManagementSystem

2️⃣ Install Required Python Libraries
pip install customtkinter
pip install mysql-connector-python


(You can also use: py -m pip install ... if needed)

3️⃣ Set Up the MySQL Database

Start MySQL Server

Log in to MySQL client (CLI or MySQL Workbench)

Run the provided setup.sql script:

mysql -u root -p
# Enter your password
mysql> SOURCE /path/to/your/project/folder/setup.sql;


This will:
✅ Create courier_db database
✅ Create users, couriers, and tracking_history tables
✅ Insert default users for each role

4️⃣ Configure Database Connection

Edit database.py and update your MySQL credentials:

# Inside database.py
connection = mysql.connector.connect(
    host='localhost',       # Your MySQL host (usually 'localhost')
    database='courier_db',
    user='root',            # Your MySQL username
    password='your_password'  # Change to your MySQL password
)

5️⃣ Run the Application
python main.py


You should now see the Login Window.

🖱 How to Use

Run main.py to launch the app

Login or Register

Use default credentials (see below) OR

Click "Register Here" to create a new client/employee account

Navigate Dashboard based on your role

Logout securely using the sidebar logout button

🔑 Default Login Credentials
Role	Username	Password
Admin	admin	admin123
Employee	employee1	emp123
Client	client1	client123
📂 Project Structure
CourierManagementSystem/
├── main.py               # Main application controller, manages frames
├── database.py           # Handles all MySQL database connections and queries
├── login_view.py         # Contains the Login and Registration frames
├── admin_view.py         # The dashboard frame for the Admin role
├── employee_view.py      # The dashboard frame for the Employee role
├── client_view.py        # The dashboard frame for the Client role
├── setup.sql             # SQL script to initialize the database and tables
└── README.md             # This file
