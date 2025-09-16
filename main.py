import customtkinter as ctk
from login_view import LoginView, RegistrationView
from admin_view import AdminView
from employee_view import EmployeeView
from client_view import ClientView

class MainApp(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set a global theme
        ctk.set_appearance_mode("System")  # Can be "Dark", "Light"
        ctk.set_default_color_theme("dark-blue")

        self.title("Courier Management System")
        self.geometry("1200x720") # Increased size for better layout

        self.current_user = None

        container = ctk.CTkFrame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        all_frames = (LoginView, RegistrationView, AdminView, EmployeeView, ClientView)

        for F in all_frames:
            page_name = F.__name__
            frame = F(master=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("LoginView")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

    def on_login_success(self, user):
        self.current_user = user
        role = user.get('role')
        
        page_name_map = {
            'admin': 'AdminView',
            'employee': 'EmployeeView',
            'client': 'ClientView'
        }
        
        page_name = page_name_map.get(role)
        
        if page_name:
            self.title(f"Courier Management System - Welcome {user['username']}")
            dashboard_frame = self.frames[page_name]
            dashboard_frame.on_show(user)
            self.show_frame(page_name)
        else:
            self.show_frame("LoginView")

    def logout(self):
        """Logs the user out and returns to the login screen."""
        self.current_user = None
        self.title("Courier Management System")
        self.show_frame("LoginView")


if __name__ == "__main__":
    app = MainApp()
    app.mainloop()