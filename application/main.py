import tkinter as tk
from auth import Auth
from admin_page import AdminPage
from user_page import UserPage


class CashTrackApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cash Track")
        self.root.geometry("600x350")

        self.auth = Auth(self.root, self.show_admin_home, self.show_user_home)
        self.auth.show_login_screen()

    def show_admin_home(self, username):
        self.clear_screen()
        self.admin_page = AdminPage(self.root, username, self.show_login_screen)

    def show_user_home(self, username):
        self.clear_screen()
        self.user_page = UserPage(
            self.root, username, self.show_login_screen, auth_instance=self.auth
        )

    def show_login_screen(self):
        self.clear_screen()
        self.auth.show_login_screen()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = CashTrackApp(root)
    root.mainloop()
