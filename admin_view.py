import customtkinter as ctk
from tkinter import ttk, messagebox
import database as db

def style_treeview():
    """Styles the ttk.Treeview to match the CustomTkinter theme."""
    style = ttk.Style()
    # Get theme colors
    bg_color = ctk.ThemeManager.theme["CTkFrame"]["fg_color"][1]
    text_color = ctk.ThemeManager.theme["CTkLabel"]["text_color"][1]
    header_bg = ctk.ThemeManager.theme["CTkButton"]["fg_color"][1]
    
    style.theme_use("default")
    style.configure("Treeview", background=bg_color, foreground=text_color, fieldbackground=bg_color, borderwidth=0)
    style.configure("Treeview.Heading", background=header_bg, foreground="white", relief="flat")
    style.map("Treeview.Heading", background=[('active', ctk.ThemeManager.theme["CTkButton"]["hover_color"][1])])
    style.map("Treeview", background=[('selected', ctk.ThemeManager.theme["CTkButton"]["fg_color"][1])])

class AdminView(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.user = None

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- Sidebar ---
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsw")
        self.sidebar_frame.grid_rowconfigure(5, weight=1)

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="Admin Panel", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        self.welcome_label = ctk.CTkLabel(self.sidebar_frame, text="", anchor="w")
        self.welcome_label.grid(row=1, column=0, padx=20, pady=(10, 20))

        self.users_button = ctk.CTkButton(self.sidebar_frame, text="Manage Users", command=self.show_users_frame)
        self.users_button.grid(row=2, column=0, padx=20, pady=10)

        self.couriers_button = ctk.CTkButton(self.sidebar_frame, text="View All Couriers", command=self.show_couriers_frame)
        self.couriers_button.grid(row=3, column=0, padx=20, pady=10)

        self.logout_button = ctk.CTkButton(self.sidebar_frame, text="Logout", command=self.logout)
        self.logout_button.grid(row=6, column=0, padx=20, pady=(10, 20), sticky="s")

        # --- Main Content Area ---
        self.main_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        self.users_frame = self.create_users_frame()
        self.couriers_frame = self.create_couriers_frame()
        style_treeview()

    def on_show(self, user):
        self.user = user
        self.welcome_label.configure(text=f"Welcome, {self.user['username']}")
        self.show_users_frame()

    def logout(self):
        self.controller.logout()

    # ... (The rest of the methods like show_users_frame, create_users_frame, load_users, etc., remain the same)
    def show_users_frame(self):
        self.couriers_frame.pack_forget()
        self.users_frame.pack(fill="both", expand=True)
        self.load_users()

    def show_couriers_frame(self):
        self.users_frame.pack_forget()
        self.couriers_frame.pack(fill="both", expand=True)
        self.load_couriers()

    def create_users_frame(self):
        frame = ctk.CTkFrame(self.main_frame)
        label = ctk.CTkLabel(frame, text="User Management", font=ctk.CTkFont(size=20, weight="bold"))
        label.pack(pady=10, padx=10, anchor="w")
        tree_frame = ctk.CTkFrame(frame)
        tree_frame.pack(pady=10, padx=10, fill="both", expand=True)
        columns = ("id", "username", "full_name", "email", "role", "phone_number")
        self.users_tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
        for col in columns:
            self.users_tree.heading(col, text=col.replace("_", " ").title())
        self.users_tree.pack(fill="both", expand=True)
        delete_button = ctk.CTkButton(frame, text="Delete Selected User", command=self.delete_user)
        delete_button.pack(pady=10, padx=10, anchor="e")
        return frame

    def create_couriers_frame(self):
        frame = ctk.CTkFrame(self.main_frame)
        label = ctk.CTkLabel(frame, text="All Couriers", font=ctk.CTkFont(size=20, weight="bold"))
        label.pack(pady=10, padx=10, anchor="w")
        tree_frame = ctk.CTkFrame(frame)
        tree_frame.pack(pady=10, padx=10, fill="both", expand=True)
        columns = ("id", "tracking_number", "sender_name", "receiver_name", "status", "client_id", "created_at")
        self.couriers_tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
        for col in columns:
            self.couriers_tree.heading(col, text=col.replace("_", " ").title())
        self.couriers_tree.pack(fill="both", expand=True)
        return frame

    def load_users(self):
        for item in self.users_tree.get_children(): self.users_tree.delete(item)
        conn = db.create_connection()
        if conn:
            users = db.fetch_all(conn, "SELECT id, username, full_name, email, role, phone_number FROM users")
            conn.close()
            for user in users: self.users_tree.insert("", "end", values=list(user.values()))

    def delete_user(self):
        selected_item = self.users_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a user to delete.")
            return
        user_id = self.users_tree.item(selected_item, "values")[0]
        if int(user_id) == self.user['id']:
            messagebox.showerror("Error", "You cannot delete your own account.")
            return
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this user?"):
            conn = db.create_connection()
            if conn:
                db.execute_query(conn, "DELETE FROM users WHERE id = %s", (user_id,))
                conn.close()
                self.load_users()
                messagebox.showinfo("Success", "User deleted successfully.")

    def load_couriers(self):
        for item in self.couriers_tree.get_children(): self.couriers_tree.delete(item)
        conn = db.create_connection()
        if conn:
            couriers = db.fetch_all(conn, "SELECT id, tracking_number, sender_name, receiver_name, status, client_id, created_at FROM couriers")
            conn.close()
            for courier in couriers: self.couriers_tree.insert("", "end", values=list(courier.values()))