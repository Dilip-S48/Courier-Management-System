import customtkinter as ctk
from tkinter import ttk, messagebox
import database as db
import uuid
from admin_view import style_treeview # Import the styling function

class ClientView(ctk.CTkFrame):
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

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="Client Portal", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        self.welcome_label = ctk.CTkLabel(self.sidebar_frame, text="", anchor="w")
        self.welcome_label.grid(row=1, column=0, padx=20, pady=(10, 20))

        self.book_button = ctk.CTkButton(self.sidebar_frame, text="Book a Courier", command=self.show_booking_frame)
        self.book_button.grid(row=2, column=0, padx=20, pady=10)

        self.track_button = ctk.CTkButton(self.sidebar_frame, text="My Couriers", command=self.show_tracking_frame)
        self.track_button.grid(row=3, column=0, padx=20, pady=10)

        self.logout_button = ctk.CTkButton(self.sidebar_frame, text="Logout", command=self.logout)
        self.logout_button.grid(row=6, column=0, padx=20, pady=(10, 20), sticky="s")

        # --- Main Content Area ---
        self.main_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        self.booking_frame = self.create_booking_frame()
        self.tracking_frame = self.create_tracking_frame()
        style_treeview()

    def on_show(self, user):
        self.user = user
        self.welcome_label.configure(text=f"Welcome, {self.user['username']}")
        self.sender_name_entry.delete(0, 'end')
        self.sender_name_entry.insert(0, self.user.get('full_name', ''))
        self.sender_address_entry.delete(0, 'end')
        self.sender_address_entry.insert(0, self.user.get('address', ''))
        self.show_booking_frame()

    def logout(self):
        self.controller.logout()

    # ... (The rest of the methods remain the same, with minor styling tweaks)
    def show_booking_frame(self):
        self.tracking_frame.pack_forget()
        self.booking_frame.pack(fill="both", expand=True)

    def show_tracking_frame(self):
        self.booking_frame.pack_forget()
        self.tracking_frame.pack(fill="both", expand=True)
        self.load_client_couriers()

    def create_booking_frame(self):
        frame = ctk.CTkFrame(self.main_frame)
        label = ctk.CTkLabel(frame, text="Book a New Courier", font=ctk.CTkFont(size=20, weight="bold"))
        label.pack(pady=10, padx=10, anchor="w")
        form_frame = ctk.CTkFrame(frame)
        form_frame.pack(pady=10, padx=10, fill="x")
        ctk.CTkLabel(form_frame, text="Sender Name:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.sender_name_entry = ctk.CTkEntry(form_frame)
        self.sender_name_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        ctk.CTkLabel(form_frame, text="Sender Address:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.sender_address_entry = ctk.CTkEntry(form_frame)
        self.sender_address_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        ctk.CTkLabel(form_frame, text="Receiver Name:").grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.receiver_name_entry = ctk.CTkEntry(form_frame, placeholder_text="Receiver's full name")
        self.receiver_name_entry.grid(row=2, column=1, padx=10, pady=10, sticky="ew")
        ctk.CTkLabel(form_frame, text="Receiver Address:").grid(row=3, column=0, padx=10, pady=10, sticky="w")
        self.receiver_address_entry = ctk.CTkEntry(form_frame, placeholder_text="Receiver's full address")
        self.receiver_address_entry.grid(row=3, column=1, padx=10, pady=10, sticky="ew")
        ctk.CTkLabel(form_frame, text="Parcel Description:").grid(row=4, column=0, padx=10, pady=10, sticky="w")
        self.parcel_desc_entry = ctk.CTkEntry(form_frame, placeholder_text="e.g., Documents, Electronics")
        self.parcel_desc_entry.grid(row=4, column=1, padx=10, pady=10, sticky="ew")
        form_frame.grid_columnconfigure(1, weight=1)
        submit_button = ctk.CTkButton(frame, text="Submit Booking", command=self.submit_booking)
        submit_button.pack(pady=20, padx=10, anchor="e")
        return frame

    def create_tracking_frame(self):
        frame = ctk.CTkFrame(self.main_frame)
        label = ctk.CTkLabel(frame, text="My Courier History", font=ctk.CTkFont(size=20, weight="bold"))
        label.pack(pady=10, padx=10, anchor="w")
        tree_frame = ctk.CTkFrame(frame)
        tree_frame.pack(pady=10, padx=10, fill="both", expand=True)
        columns = ("tracking_number", "receiver_name", "receiver_address", "status", "created_at")
        self.couriers_tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
        for col in columns:
            self.couriers_tree.heading(col, text=col.replace("_", " ").title())
        self.couriers_tree.pack(fill="both", expand=True)
        return frame

    def submit_booking(self):
        sender_name = self.sender_name_entry.get()
        sender_address = self.sender_address_entry.get()
        receiver_name = self.receiver_name_entry.get()
        receiver_address = self.receiver_address_entry.get()
        parcel_desc = self.parcel_desc_entry.get()
        if not all([sender_name, sender_address, receiver_name, receiver_address, parcel_desc]):
            messagebox.showerror("Error", "Please fill all fields.")
            return
        tracking_number = "CR" + str(uuid.uuid4().hex)[:10].upper()
        client_id = self.user['id']
        conn = db.create_connection()
        if conn:
            try:
                cursor = db.execute_query(conn, "INSERT INTO couriers (tracking_number, sender_name, sender_address, receiver_name, receiver_address, parcel_description, client_id) VALUES (%s, %s, %s, %s, %s, %s, %s)", (tracking_number, sender_name, sender_address, receiver_name, receiver_address, parcel_desc, client_id))
                courier_id = cursor.lastrowid
                db.execute_query(conn, "INSERT INTO tracking_history (courier_id, status, remarks) VALUES (%s, 'Pending', 'Booking created.')", (courier_id,))
                messagebox.showinfo("Success", f"Booking successful! Your tracking number is: {tracking_number}")
                self.receiver_name_entry.delete(0, 'end')
                self.receiver_address_entry.delete(0, 'end')
                self.parcel_desc_entry.delete(0, 'end')
            except Exception as e:
                messagebox.showerror("Error", f"Booking failed: {e}")
            finally:
                conn.close()

    def load_client_couriers(self):
        for item in self.couriers_tree.get_children(): self.couriers_tree.delete(item)
        conn = db.create_connection()
        if conn:
            query = "SELECT tracking_number, receiver_name, receiver_address, status, created_at FROM couriers WHERE client_id = %s ORDER BY created_at DESC"
            couriers = db.fetch_all(conn, query, (self.user['id'],))
            conn.close()
            for courier in couriers: self.couriers_tree.insert("", "end", values=list(courier.values()))