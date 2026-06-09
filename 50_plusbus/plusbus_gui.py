import tkinter as tk
from tkinter import ttk
import plusbus_data as pbd
import plusbus_database as pbdb

class Plusbus:
	def __init__(self):
		self.gui_background_color = "#2E2E2E"
		self.secondary_bg_color = "#4F4F4F"
		self.button_press_color = "#696969"
		self.text_color = "#FFFFFF"
		self.row_height = 20

		self.gui = tk.Tk()
		self.gui.title("Plus bus app")

		self.acc_frame = tk.Frame(self.gui, bg=self.gui_background_color, width=800, height=700)
		self.acc_frame.grid_propagate(False)
		self.acc_frame.grid(row=0, column=0)

		self.acc_header_frame = tk.Frame(self.acc_frame, bg=self.gui_background_color, width=800, height=150)
		self.acc_header_frame.grid_propagate(False)
		self.acc_header_frame.grid(row=0, column=0)

		self.acc_header_label = tk.Label(self.acc_header_frame, text="Login på din account", bg=self.gui_background_color, fg=self.text_color, font=("Arial", 50))
		self.acc_header_label.grid(row=0, column=0, padx=100, pady=50)

		self.acc_acc_frame = tk.Frame(self.acc_frame, bg=self.gui_background_color, width=800, height=250, padx=250)
		self.acc_acc_frame.grid_propagate(False)
		self.acc_acc_frame.grid(row=1, column=0)

		self.tree_view_style = ttk.Style()
		self.tree_view_style.theme_use("default")
		self.tree_view_style.configure("Treeview", bg=self.gui_background_color, fg=self.text_color, rowheight=self.row_height, fieldbackground=self.secondary_bg_color)
		self.tree_view_style.map("Treeview", background=[("selected", self.text_color)])

		self.acc_scollbar = tk.Scrollbar(self.acc_acc_frame)
		self.acc_scollbar.grid(row=0, column=1, sticky="ns")
		self.acc_treeview = ttk.Treeview(self.acc_acc_frame, yscrollcommand=self.acc_scollbar.set, selectmode="browse")
		self.acc_treeview.grid(row=0, column=0)
		self.acc_scollbar.config(command=self.acc_treeview.yview)

		self.acc_treeview['columns'] = "accounts"
		self.acc_treeview.column("#0", width=0, stretch=tk.NO)
		self.acc_treeview.column("accounts", width=300, anchor="w")

		self.acc_treeview.heading("#0", text="", anchor="w")
		self.acc_treeview.heading("accounts", text="Accounts", anchor="center")

		self.acc_button_frame = tk.Frame(self.acc_frame, bg=self.gui_background_color, width=800, height=150)
		self.acc_button_frame.grid_propagate(False)
		self.acc_button_frame.grid(row=2, column=0)

		self.acc_button_login = tk.Button(self.acc_button_frame, text="Login", relief="flat", bg=self.secondary_bg_color, fg=self.text_color, activebackground=self.button_press_color, font=("Arial", 15))
		self.acc_button_login.grid(row=0, column=0, padx=375)


if __name__ == "__main__":
	plusbus = Plusbus()
	plusbus.gui.mainloop()