📦 Courier Management System








A modern, user-friendly desktop application for managing courier services, built with Python, CustomTkinter, and MySQL.
This system provides a complete solution with role-based access for administrators, employees, and clients — all within a single, seamless interface.

📑 Table of Contents

✨ Key Features

🛠 Technologies Used

🖼 Screenshots

📋 Prerequisites

⚙️ Setup and Installation

🖱 How to Use

🔑 Default Login Credentials

📂 Project Structure

✨ Key Features

Modern & Intuitive GUI – Built with CustomTkinter for a clean, elegant interface

Unified Single-Window Interface – Smooth navigation across all pages

Role-Based Access Control

👑 Admin Dashboard: Manage users (CRUD), view courier records

👷 Employee Dashboard: View/update assigned couriers' status

👤 Client Dashboard: Book shipments & track them

Secure User Authentication – Login/Registration for each role

Complete Courier Management – Full CRUD functionality

MySQL-Powered Backend – Stores users, couriers, and tracking history

Dark/Light Theme Support – Consistent, professional look

🛠 Technologies Used
Layer	Technology
Backend	Python
Database	MySQL
GUI Framework	CustomTkinter
Connector	mysql-connector-python
🖼 Screenshots
Admin Dashboard	Client Dashboard
(Add Screenshot Here)	(Add Screenshot Here)

💡 Tip: Add screenshots in the assets/ folder and reference them here with ![Alt Text](assets/screenshot.png).

📋 Prerequisites

Python 3.7+

MySQL Server 8.0+

⚙️ Setup and Installation
1️⃣ Clone the Repository
git clone <your-repository-url>
cd CourierManagementSystem

2️⃣ Install Required Python Libraries
pip install customtkinter mysql-connector-python


(On some systems use: py -m pip install ...)

3️⃣ Set Up the MySQL Database
mysql -u root -p
# Enter your MySQL password
mysql> SOURCE /path/to/your/project/folder/setup.sql;


This will:
✅ Create courier_db database
✅ Create users, couriers, and tracking_history tables
✅ Insert default users for each role

4️⃣ Configure Database Connection

Edit database.py:

connection = mysql.connector.connect(
    host='localhost',       # MySQL host (default: localhost)
    database='courier_db',
    user='root',            # Your MySQL username
    password='your_password'  # Change this to your MySQL password
)

5️⃣ Run the Application
python main.py

🖱 How to Use

Run main.py

Login/Register

Use default credentials
 OR

Register as a new client/employee

Explore Dashboards (Admin/Employee/Client based on role)

Logout securely via the sidebar

🔑 Default Login Credentials
Role	Username	Password
Admin	admin	admin123
Employee	employee1	emp123
Client	client1	client123
📂 Project Structure
CourierManagementSystem/
├── main.py               # Main application controller
├── database.py           # Handles all MySQL database operations
├── login_view.py         # Login & Registration frames
├── admin_view.py         # Admin dashboard
├── employee_view.py      # Employee dashboard
├── client_view.py        # Client dashboard
├── setup.sql             # Database initialization script
└── README.md             # Project documentation
