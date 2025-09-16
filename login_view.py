import customtkinter as ctk
from tkinter import messagebox
import database as db

class RegistrationView(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.form_frame = ctk.CTkFrame(self, corner_radius=15)
        self.form_frame.grid(row=0, column=0, padx=20, pady=20)

        self.label = ctk.CTkLabel(self.form_frame, text="Create an Account", font=ctk.CTkFont(size=24, weight="bold"))
        self.label.pack(pady=(20, 15), padx=30)

        self.username_entry = ctk.CTkEntry(self.form_frame, placeholder_text="Username", width=250)
        self.username_entry.pack(pady=12, padx=30)

        self.password_entry = ctk.CTkEntry(self.form_frame, placeholder_text="Password", show="*", width=250)
        self.password_entry.pack(pady=12, padx=30)
        
        self.fullname_entry = ctk.CTkEntry(self.form_frame, placeholder_text="Full Name", width=250)
        self.fullname_entry.pack(pady=12, padx=30)

        self.email_entry = ctk.CTkEntry(self.form_frame, placeholder_text="Email", width=250)
        self.email_entry.pack(pady=12, padx=30)

        self.phone_entry = ctk.CTkEntry(self.form_frame, placeholder_text="Phone Number", width=250)
        self.phone_entry.pack(pady=12, padx=30)

        self.address_entry = ctk.CTkEntry(self.form_frame, placeholder_text="Address", width=250)
        self.address_entry.pack(pady=12, padx=30)

        self.role_menu = ctk.CTkOptionMenu(self.form_frame, values=["client", "employee"], width=250)
        self.role_menu.set("client")
        self.role_menu.pack(pady=12, padx=30)

        self.register_button = ctk.CTkButton(self.form_frame, text="Register", command=self.register_user, width=250)
        self.register_button.pack(pady=12, padx=30)

        self.back_button = ctk.CTkButton(self.form_frame, text="Back to Login", command=self.go_to_login, fg_color="transparent", border_width=1)
        self.back_button.pack(pady=(10, 20), padx=30)

    def register_user(self):
        # ... (This method's logic is unchanged)
        username = self.username_entry.get()
        password = self.password_entry.get()
        full_name = self.fullname_entry.get()
        email = self.email_entry.get()
        phone = self.phone_entry.get()
        address = self.address_entry.get()
        role = self.role_menu.get()

        if not all([username, password, full_name, email, role]):
            messagebox.showerror("Error", "Please fill all required fields.")
            return

        conn = db.create_connection()
        if conn:
            query = "INSERT INTO users (username, password, full_name, email, phone_number, address, role) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            try:
                db.execute_query(conn, query, (username, password, full_name, email, phone, address, role))
                messagebox.showinfo("Success", "Registration successful! You can now log in.")
                self.go_to_login()
            except Exception as e:
                messagebox.showerror("Error", f"Registration failed. Username or email may already exist.\n{e}")
            finally:
                conn.close()
    
    def go_to_login(self):
        self.username_entry.delete(0, 'end')
        self.password_entry.delete(0, 'end')
        self.fullname_entry.delete(0, 'end')
        self.email_entry.delete(0, 'end')
        self.phone_entry.delete(0, 'end')
        self.address_entry.delete(0, 'end')
        self.controller.show_frame("LoginView")


class LoginView(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.form_frame = ctk.CTkFrame(self, corner_radius=15)
        self.form_frame.grid(row=0, column=0, padx=20, pady=20)

        self.label = ctk.CTkLabel(self.form_frame, text="User Login", font=ctk.CTkFont(size=24, weight="bold"))
        self.label.pack(pady=(20, 15), padx=30)

        self.username_entry = ctk.CTkEntry(self.form_frame, placeholder_text="Username", width=250)
        self.username_entry.pack(pady=12, padx=30)

        self.password_entry = ctk.CTkEntry(self.form_frame, placeholder_text="Password", show="*", width=250)
        self.password_entry.pack(pady=12, padx=30)

        self.login_button = ctk.CTkButton(self.form_frame, text="Login", command=self.login_user, width=250)
        self.login_button.pack(pady=12, padx=30)

        self.register_label = ctk.CTkLabel(self.form_frame, text="Don't have an account?")
        self.register_label.pack(pady=(20, 0), padx=30)

        self.register_button = ctk.CTkButton(self.form_frame, text="Register Here", command=self.open_registration_page, fg_color="transparent")
        self.register_button.pack(pady=(5, 20), padx=30)

    def login_user(self):
        # ... (This method's logic is unchanged)
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password.")
            return

        conn = db.create_connection()
        if conn:
            query = "SELECT * FROM users WHERE username = %s AND password = %s"
            user = db.fetch_one(conn, query, (username, password))
            conn.close()

            if user:
                self.controller.on_login_success(user)
            else:
                messagebox.showerror("Error", "Invalid username or password.")

    def open_registration_page(self):
        self.controller.show_frame("RegistrationView")