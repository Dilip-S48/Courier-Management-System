import customtkinter as ctk
from tkinter import ttk, messagebox
import database as db
from admin_view import style_treeview # Import the styling function

class EmployeeView(ctk.CTkFrame):
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

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="Employee Panel", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        self.welcome_label = ctk.CTkLabel(self.sidebar_frame, text="", anchor="w")
        self.welcome_label.grid(row=1, column=0, padx=20, pady=(10, 20))

        self.logout_button = ctk.CTkButton(self.sidebar_frame, text="Logout", command=self.logout)
        self.logout_button.grid(row=6, column=0, padx=20, pady=(10, 20), sticky="s")

        # --- Main Content Area ---
        self.main_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        label = ctk.CTkLabel(self.main_frame, text="Manage Couriers", font=ctk.CTkFont(size=20, weight="bold"))
        label.pack(pady=10, padx=10, anchor="w")

        tree_frame = ctk.CTkFrame(self.main_frame)
        tree_frame.pack(pady=10, padx=10, fill="both", expand=True)

        columns = ("id", "tracking_number", "sender_name", "receiver_name", "status", "created_at")
        self.couriers_tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
        for col in columns:
            self.couriers_tree.heading(col, text=col.replace("_", " ").title())
        self.couriers_tree.pack(fill="both", expand=True)
        style_treeview()

        controls_frame = ctk.CTkFrame(self.main_frame)
        controls_frame.pack(pady=10, padx=10, fill="x")

        self.status_label = ctk.CTkLabel(controls_frame, text="Update Status:")
        self.status_label.pack(side="left", padx=(10, 5))
        self.status_menu = ctk.CTkOptionMenu(controls_frame, values=["Pending", "In Transit", "Delivered", "Cancelled"])
        self.status_menu.pack(side="left", padx=5)
        self.update_button = ctk.CTkButton(controls_frame, text="Update Selected Courier", command=self.update_courier_status)
        self.update_button.pack(side="left", padx=5)
        self.refresh_button = ctk.CTkButton(controls_frame, text="Refresh", command=self.load_couriers)
        self.refresh_button.pack(side="right", padx=10)

    def on_show(self, user):
        self.user = user
        self.welcome_label.configure(text=f"Welcome, {self.user['username']}")
        self.load_couriers()

    def logout(self):
        self.controller.logout()

    # ... (load_couriers and update_courier_status methods remain the same)
    def load_couriers(self):
        for item in self.couriers_tree.get_children(): self.couriers_tree.delete(item)
        conn = db.create_connection()
        if conn:
            query = "SELECT id, tracking_number, sender_name, receiver_name, status, created_at FROM couriers WHERE status NOT IN ('Delivered', 'Cancelled')"
            couriers = db.fetch_all(conn, query)
            conn.close()
            for courier in couriers: self.couriers_tree.insert("", "end", values=list(courier.values()))

    def update_courier_status(self):
        selected_item = self.couriers_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a courier to update.")
            return
        courier_id = self.couriers_tree.item(selected_item, "values")[0]
        new_status = self.status_menu.get()
        conn = db.create_connection()
        if conn:
            try:
                db.execute_query(conn, "UPDATE couriers SET status = %s, assigned_employee_id = %s WHERE id = %s", (new_status, self.user['id'], courier_id))
                db.execute_query(conn, "INSERT INTO tracking_history (courier_id, status, remarks) VALUES (%s, %s, %s)", (courier_id, new_status, f"Status updated by employee {self.user['username']}"))
                messagebox.showinfo("Success", "Courier status updated successfully.")
                self.load_couriers()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update status: {e}")
            finally:
                conn.close()