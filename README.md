Courier Management System
A modern, user-friendly desktop application for managing courier services, built with Python, CustomTkinter, and MySQL. This system provides a complete solution with role-based access for administrators, employees, and clients, all within a single, seamless interface.
<!-- Placeholder: Replace with an actual screenshot of your login screen -->
Table of Contents
Key Features
Technologies Used
Screenshots
Prerequisites
Setup and Installation
How to Use
Default Login Credentials
Project Structure
Key Features
Modern & Intuitive GUI: A visually appealing and easy-to-navigate interface built with the CustomTkinter library.
Unified Single-Window Interface: All operations and pages are managed within a single main window for a seamless user experience.
Role-Based Access Control:
Admin Dashboard: Manage users (CRUD) and view all courier records.
Employee Dashboard: View and update the status of assigned couriers.
Client Dashboard: Book new courier shipments and track the status of existing ones.
Secure User Authentication: Secure login and registration system for all user roles.
Comprehensive Courier Management: Full CRUD (Create, Read, Update, Delete) functionality for courier data.
Persistent Data Storage: Robust backend using a MySQL database to store user data, courier details, and tracking history.
Styled and Themed Interface: Features a modern dark/light theme with consistently styled widgets for a professional look.
Technologies Used
Backend: Python
-- Database: MySQL
GUI Framework: CustomTkinter
MySQL Connector: mysql-connector-python
Screenshots
Admin Dashboard	Client Dashboard
<!-- Placeholders: Replace with actual screenshots -->
Prerequisites
Before you begin, ensure you have the following installed on your system:
Python 3.7+
MySQL Server 8.0+
Setup and Installation
Follow these steps to get the application up and running on your local machine.
1. Clone the Repository
First, clone this repository or download the project folder to your local machine.
code
Bash
git clone <your-repository-url>
cd CourierManagementSystem
2. Install Required Python Libraries
Open your terminal or command prompt and install the necessary Python packages using pip.
code
Bash
pip install customtkinter
pip install mysql-connector-python
A more robust command on some systems is py -m pip install ...
3. Set Up the MySQL Database
Start your MySQL Server.
Log in to your MySQL client (e.g., MySQL Command-Line Client or a GUI tool like MySQL Workbench).
Execute the entire setup.sql script provided in the project folder. This will:
Create the courier_db database.
Create the users, couriers, and tracking_history tables.
Insert default users for each role to get you started.
Example using command line:
code
Bash
mysql -u root -p
# Enter your password
mysql> SOURCE /path/to/your/project/folder/setup.sql;
4. Configure the Database Connection
Open the database.py file in your code editor.
Locate the create_connection function.
Update the host, user, and password to match your MySQL server configuration.
code
Python
# Inside database.py
connection = mysql.connector.connect(
    host='localhost',       # Your MySQL host (usually 'localhost')
    database='courier_db',
    user='root',            # Your MySQL username
    password='your_password'  # IMPORTANT: Change this to your MySQL password
)
5. Run the Application
Once the setup is complete, run the main application file from your terminal:
code
Bash
python main.py
The application's login window should now appear.
How to Use
Launch the application by running main.py.
Login or Register:
Use the default credentials below to log in as an admin, employee, or client.
Alternatively, click "Register Here" to create a new client or employee account.
Navigate the Dashboard: Based on your role, you will be directed to the appropriate dashboard with access to specific functionalities.
Logout: Use the "Logout" button in the sidebar to securely return to the login screen.
Default Login Credentials
You can use these credentials (created by setup.sql) to log in for the first time:
Admin:
Username: admin
Password: admin123
Employee:
Username: employee1
Password: emp123
Client:
Username: client1
Password: client123
Project Structure
The project is organized into several modules for clarity and maintainability:
code
Code
CourierManagementSystem/
├── main.py               # Main application controller, manages frames
├── database.py           # Handles all MySQL database connections and queries
├── login_view.py         # Contains the Login and Registration frames
├── admin_view.py         # The dashboard frame for the Admin role
├── employee_view.py      # The dashboard frame for the Employee role
├── client_view.py        # The dashboard frame for the Client role
├── setup.sql             # SQL script to initialize the database and tables
└── README.md             # This file