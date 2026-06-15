import tkinter as tk
from tkinter import ttk
import plusbus_data as pbd
import plusbus_database as pbdb


class Plusbus:
	def __init__(self):
		self.gui_background_color = "#2E2E2E"
		self.secondary_bg_color = "#4F4F4F"
		self.test_color = "#0045FF"
		self.button_press_color = "#696969"
		self.text_color = "#FFFFFF"
		self.error_color = "#FF0000"
		self.tree_view_selected = "#262626"
		self.evenrow_background = "#4A4A4A"
		self.oddrow_background = "#757575"
		self.row_height = 20
		self.kundeid = -1
		self.auth = 0
		self.selected = [-1, "", 0]

		self.gui = tk.Tk()
		self.gui.title("Plus bus app")
		self.gui.geometry("1200x700")
		self.gui.configure(bg=self.gui_background_color)

		#  Account login / Create account

		self.acc_frame = tk.Frame(self.gui, bg=self.gui_background_color)
		self.acc_frame.place(relx=0.5, rely=0.5, anchor="center")

		self.current_window = self.acc_frame

		self.acc_header_frame = tk.Frame(self.acc_frame)
		self.acc_header_frame.pack()

		self.acc_header_label = tk.Label(self.acc_header_frame, text="Login på din account", bg=self.gui_background_color, fg=self.text_color, font=("Arial", 50))
		self.acc_header_label.grid(row=0, column=0)

		self.acc_acc_frame = tk.Frame(self.acc_frame, bg=self.gui_background_color)
		self.acc_acc_frame.pack()

		self.tree_view_style = ttk.Style()
		self.tree_view_style.theme_use("default")
		self.tree_view_style.configure("Treeview", bg=self.gui_background_color, fg=self.text_color, rowheight=self.row_height, fieldbackground=self.secondary_bg_color)
		self.tree_view_style.map("Treeview", background=[("selected", self.tree_view_selected)])

		self.acc_scrollbar = tk.Scrollbar(self.acc_acc_frame)
		self.acc_scrollbar.grid(row=0, column=1, pady=(30, 0), sticky="ns")
		self.acc_treeview = ttk.Treeview(self.acc_acc_frame, yscrollcommand=self.acc_scrollbar.set, selectmode="browse")
		self.acc_treeview.grid(row=0, column=0, pady=(30, 0))
		self.acc_scrollbar.config(command=self.acc_treeview.yview)

		self.acc_treeview['columns'] = ("id", "efternavn", "kontakt", "auth")
		self.acc_treeview.column("#0", width=0, stretch=tk.NO)
		self.acc_treeview.column("id", width=50, anchor="w")
		self.acc_treeview.column("efternavn", width=125, anchor="w")
		self.acc_treeview.column("kontakt", width=125, anchor="w")
		self.acc_treeview.column("auth", width=35, anchor="w")

		self.acc_treeview.heading("#0", text="", anchor="w")
		self.acc_treeview.heading("id", text="Id", anchor="center")
		self.acc_treeview.heading("efternavn", text="Efternavn", anchor="center")
		self.acc_treeview.heading("kontakt", text="Kontakt", anchor="center")
		self.acc_treeview.heading("auth", text="Auth", anchor="center")

		self.acc_treeview.tag_configure("evenrow", background=self.evenrow_background, foreground=self.text_color)
		self.acc_treeview.tag_configure("oddrow", background=self.oddrow_background, foreground=self.text_color)

		self.acc_treeview.bind("<ButtonRelease-1>", lambda event: self.select_id(self.acc_treeview, "kundeid"))

		fill_treeview(self.acc_treeview, pbdb.select_all(pbd.Kunde))

		self.acc_button_frame = tk.Frame(self.acc_frame, bg=self.gui_background_color)
		self.acc_button_frame.pack()

		self.acc_button_login = tk.Button(self.acc_button_frame, text="Login", relief="flat", bg=self.secondary_bg_color,
		                                  fg=self.text_color, activebackground=self.button_press_color, font=("Arial", 15), command=self.login)
		self.acc_button_login.grid(row=0, column=0, pady=(50, 0))

		self.acc_button_label = tk.Label(self.acc_button_frame, text="Har du ikke en account?", bg=self.gui_background_color, fg=self.text_color, font=("Arial", 15))
		self.acc_button_label.grid(row=1, column=0, pady=(30, 0))
		self.acc_button_create_button = tk.Button(self.acc_button_frame, text="Opret account", relief="flat", bg=self.secondary_bg_color, fg=self.text_color,
		                                          activebackground=self.button_press_color, font=("Arial", 15), command=lambda: self.change_window(self.acc_create_frame))
		self.acc_button_create_button.grid(row=2, column=0, pady=(5, 80))

		#  Create account

		self.acc_create_frame = tk.Frame(self.gui, bg=self.gui_background_color)
		# self.acc_create_frame.place(relx=0.5, rely=0.5, anchor="center")

		self.acc_create_label = tk.Label(self.acc_create_frame, text="Opret din account", bg=self.gui_background_color, fg=self.text_color, font=("Arial", 40))
		self.acc_create_label.grid(row=0, column=0)

		self.acc_create_label_frame = tk.Frame(self.acc_create_frame, bg=self.gui_background_color)
		self.acc_create_label_frame.grid(row=1, column=0)

		self.acc_create_label_frame_label_efternavn = tk.Label(self.acc_create_label_frame, text="Efternavn", bg=self.gui_background_color, fg=self.text_color, font=("Arial", 20))
		self.acc_create_label_frame_label_efternavn.grid(row=0, column=0, padx=(0, 30))

		self.acc_create_label_frame_label_kontaktinfo = tk.Label(self.acc_create_label_frame, text="Kontaktinfo", bg=self.gui_background_color, fg=self.text_color, font=("Arial", 20))
		self.acc_create_label_frame_label_kontaktinfo.grid(row=0, column=1)

		self.acc_create_label_frame_entry_efternavn = tk.Entry(self.acc_create_label_frame, font=("Arial", 20), width=10)
		self.acc_create_label_frame_entry_efternavn.grid(row=1, column=0, padx=(0, 30))

		self.acc_create_label_frame_entry_kontaktinfo = tk.Entry(self.acc_create_label_frame, font=("Arial", 20), width=10)
		self.acc_create_label_frame_entry_kontaktinfo.grid(row=1, column=1)

		self.acc_create_back_button = tk.Button(self.acc_create_label_frame, text="Annuller", relief="flat", bg=self.secondary_bg_color, fg=self.text_color,
		                                        activebackground=self.button_press_color, font=("Arial", 20), command=lambda: self.change_window(self.acc_frame))
		self.acc_create_back_button.grid(row=2, column=0, pady=(30, 0), padx=(0, 30))

		self.acc_create_create_account_button = tk.Button(self.acc_create_label_frame, text="Opret account", relief="flat", bg=self.secondary_bg_color, fg=self.text_color,
		                                                  activebackground=self.button_press_color, font=("Arial", 20), command=lambda: self.create_account())
		self.acc_create_create_account_button.grid(row=2, column=1, pady=(30, 0))
		self.acc_create_label_frame_label_missing_info = tk.Label(self.acc_create_frame, text="", bg=self.gui_background_color, fg=self.error_color, font=("Arial", 50))
		self.acc_create_label_frame_label_missing_info.grid(row=2, column=0, pady=(30, 0))

		# Admin menu

		self.admin_frame = tk.Frame(self.gui, bg=self.gui_background_color)

		self.admin_frame_label = tk.Label(self.admin_frame, text="Admin panel", bg=self.gui_background_color, fg=self.text_color, font=("Arial", 40))
		self.admin_frame_label.grid(row=0, column=0)

		self.admin_rejse_frame = tk.Frame(self.admin_frame, bg=self.gui_background_color)
		self.admin_rejse_frame.grid(row=1, column=0)

		# self.admin_tree_view_style = ttk.Style()
		# self.admin_tree_view_style.theme_use("default")
		# self.admin_tree_view_style.configure("Treeview", bg=self.gui_background_color, fg=self.text_color, rowheight=self.row_height, fieldbackground=self.secondary_bg_color)
		# self.admin_tree_view_style.map("Treeview", background=[("selected", self.tree_view_selected)])

		self.admin_scrollbar = tk.Scrollbar(self.admin_rejse_frame)
		self.admin_scrollbar.grid(row=0, column=1, pady=(30, 0), sticky="ns")
		self.admin_treeview = ttk.Treeview(self.admin_rejse_frame, yscrollcommand=self.admin_scrollbar.set, selectmode="browse")
		self.admin_treeview.grid(row=0, column=0, pady=(30, 0))
		self.admin_scrollbar.config(command=self.admin_treeview.yview)

		self.admin_treeview['columns'] = ("id", "rute", "dato", "pladskapacitet")
		self.admin_treeview.column("#0", width=0, stretch=tk.NO)
		self.admin_treeview.column("id", width=50, anchor="w")
		self.admin_treeview.column("rute", width=125, anchor="w")
		self.admin_treeview.column("dato", width=125, anchor="w")
		self.admin_treeview.column("pladskapacitet", width=150, anchor="w")

		self.admin_treeview.heading("#0", text="", anchor="w")
		self.admin_treeview.heading("id", text="Id", anchor="center")
		self.admin_treeview.heading("rute", text="Rute", anchor="center")
		self.admin_treeview.heading("dato", text="Dato", anchor="center")
		self.admin_treeview.heading("pladskapacitet", text="Pladskapacitet", anchor="center")

		self.admin_treeview.tag_configure("evenrow", background=self.evenrow_background, foreground=self.text_color)
		self.admin_treeview.tag_configure("oddrow", background=self.oddrow_background, foreground=self.text_color)

		self.admin_treeview.bind("<ButtonRelease-1>", lambda event: self.select_id(self.admin_treeview, "rejseid"))

		fill_treeview(self.admin_treeview, pbdb.select_all(pbd.Rejse))

		self.admin_entry_frame = tk.Frame(self.admin_frame, bg=self.gui_background_color)
		self.admin_entry_frame.grid(row=2, column=0)

		self.admin_entry_frame_rute_label = tk.Label(self.admin_entry_frame, text="Rute", bg=self.gui_background_color, fg=self.text_color, font=("Arial", 20))
		self.admin_entry_frame_rute_label.grid(row=0, column=0, padx=(0, 30))

		self.admin_entry_frame_dato_label = tk.Label(self.admin_entry_frame, text="Dato", bg=self.gui_background_color, fg=self.text_color, font=("Arial", 20))
		self.admin_entry_frame_dato_label.grid(row=0, column=1, padx=(0, 30))

		self.admin_entry_frame_pladskapacitet_label = tk.Label(self.admin_entry_frame, text="Pladskapacitet", bg=self.gui_background_color, fg=self.text_color, font=("Arial", 20))
		self.admin_entry_frame_pladskapacitet_label.grid(row=0, column=2)

		self.admin_entry_frame_rute_entry = tk.Entry(self.admin_entry_frame, font=("Arial", 20), width=10)
		self.admin_entry_frame_rute_entry.grid(row=1, column=0, padx=(0, 30))

		self.admin_entry_frame_dato_entry = tk.Entry(self.admin_entry_frame, font=("Arial", 20), width=10)
		self.admin_entry_frame_dato_entry.grid(row=1, column=1, padx=(0, 30))

		self.admin_entry_frame_pladskapacitet_entry = tk.Entry(self.admin_entry_frame, font=("Arial", 20), width=10)
		self.admin_entry_frame_pladskapacitet_entry.grid(row=1, column=2)

		self.admin_button_frame = tk.Frame(self.admin_frame, bg=self.gui_background_color)
		self.admin_button_frame.grid(row=3, column=0, pady=(30, 0))

		self.admin_back_button = tk.Button(self.admin_button_frame, text="Tilbage", relief="flat", bg=self.secondary_bg_color, fg=self.text_color,
		                                   activebackground=self.button_press_color, font=("Arial", 20), command=lambda: self.change_window(self.acc_frame))
		self.admin_back_button.grid(row=0, column=0, padx=(0, 30))

		self.admin_slet_rejse_button = tk.Button(self.admin_button_frame, text="Slet rejse", relief="flat", bg=self.secondary_bg_color, fg=self.text_color,
		                                         activebackground=self.button_press_color, font=("Arial", 20), command=self.delete_rejse)
		self.admin_slet_rejse_button.grid(row=0, column=1, padx=(0, 30))

		self.admin_opret_rejse_button = tk.Button(self.admin_button_frame, text="Opret rejse", relief="flat", bg=self.secondary_bg_color, fg=self.text_color,
		                                          activebackground=self.button_press_color, font=("Arial", 20), command=self.opret_rejse)
		self.admin_opret_rejse_button.grid(row=0, column=2, padx=(0, 30))

		self.acc_create_label_frame_label_error = tk.Label(self.admin_frame, text="", bg=self.gui_background_color, fg=self.error_color, font=("Arial", 30))
		self.acc_create_label_frame_label_error.grid(row=4, column=0, pady=(30, 0))

		# Kunde menu

		self.kunde_frame = tk.Frame(self.gui, bg=self.gui_background_color)
		self.kunde_frame_treeview_frame = tk.Frame(self.kunde_frame, bg=self.gui_background_color)
		self.kunde_frame_treeview_frame.grid(row=0, column=0)

		# Rejser man kan booke treeview

		self.kunde_frame_treeview_rejse_frame = tk.Frame(self.kunde_frame_treeview_frame, bg=self.gui_background_color)
		self.kunde_frame_treeview_rejse_frame.grid(row=0, column=0)

		self.kunde_frame_treeview_rejse_label = tk.Label(self.kunde_frame_treeview_rejse_frame, text="Rejser du kan booke", bg=self.gui_background_color, fg=self.text_color, font=("Arial", 25))
		self.kunde_frame_treeview_rejse_label.grid(row=0, column=0)

		self.kunde_frame_treeview_rejse_scrollbar = tk.Scrollbar(self.kunde_frame_treeview_rejse_frame)
		self.kunde_frame_treeview_rejse_scrollbar.grid(row=1, column=1, pady=(30, 0), sticky="ns")
		self.kunde_frame_treeview_rejse_treeview = ttk.Treeview(self.kunde_frame_treeview_rejse_frame, yscrollcommand=self.kunde_frame_treeview_rejse_scrollbar.set, selectmode="browse")
		self.kunde_frame_treeview_rejse_treeview.grid(row=1, column=0, pady=(30, 0))
		self.kunde_frame_treeview_rejse_scrollbar.config(command=self.kunde_frame_treeview_rejse_treeview.yview)

		self.kunde_frame_treeview_rejse_treeview['columns'] = ("id", "rute", "dato", "pladskapacitet")
		self.kunde_frame_treeview_rejse_treeview.column("#0", width=0, stretch=tk.NO)
		self.kunde_frame_treeview_rejse_treeview.column("id", width=50, anchor="w")
		self.kunde_frame_treeview_rejse_treeview.column("rute", width=125, anchor="w")
		self.kunde_frame_treeview_rejse_treeview.column("dato", width=125, anchor="w")
		self.kunde_frame_treeview_rejse_treeview.column("pladskapacitet", width=150, anchor="w")

		self.kunde_frame_treeview_rejse_treeview.heading("#0", text="", anchor="w")
		self.kunde_frame_treeview_rejse_treeview.heading("id", text="Id", anchor="center")
		self.kunde_frame_treeview_rejse_treeview.heading("rute", text="Rute", anchor="center")
		self.kunde_frame_treeview_rejse_treeview.heading("dato", text="Dato", anchor="center")
		self.kunde_frame_treeview_rejse_treeview.heading("pladskapacitet", text="Pladskapacitet", anchor="center")

		self.kunde_frame_treeview_rejse_treeview.tag_configure("evenrow", background=self.evenrow_background, foreground=self.text_color)
		self.kunde_frame_treeview_rejse_treeview.tag_configure("oddrow", background=self.oddrow_background, foreground=self.text_color)

		self.kunde_frame_treeview_rejse_treeview.bind("<ButtonRelease-1>", lambda event: self.select_id(self.kunde_frame_treeview_rejse_treeview, "rejseid"))

		# Bookinger treeview

		self.kunde_frame_treeview_bookinger_frame = tk.Frame(self.kunde_frame_treeview_frame, bg=self.gui_background_color)
		self.kunde_frame_treeview_bookinger_frame.grid(row=0, column=1, padx=(50, 0))

		self.kunde_frame_treeview_bookinger_label = tk.Label(self.kunde_frame_treeview_bookinger_frame, text="Dine bookinger", bg=self.gui_background_color, fg=self.text_color, font=("Arial", 25))
		self.kunde_frame_treeview_bookinger_label.grid(row=0, column=1)

		self.kunde_frame_treeview_bookinger_scrollbar = tk.Scrollbar(self.kunde_frame_treeview_bookinger_frame)
		self.kunde_frame_treeview_bookinger_scrollbar.grid(row=1, column=2, pady=(30, 0), sticky="ns")
		self.kunde_frame_treeview_bookinger_treeview = ttk.Treeview(self.kunde_frame_treeview_bookinger_frame, yscrollcommand=self.kunde_frame_treeview_bookinger_scrollbar.set, selectmode="browse")
		self.kunde_frame_treeview_bookinger_treeview.grid(row=1, column=1, pady=(30, 0))
		self.kunde_frame_treeview_bookinger_scrollbar.config(command=self.kunde_frame_treeview_bookinger_treeview.yview)

		self.kunde_frame_treeview_bookinger_treeview['columns'] = ("id", "rejseid", "pladser")
		self.kunde_frame_treeview_bookinger_treeview.column("#0", width=0, stretch=tk.NO)
		self.kunde_frame_treeview_bookinger_treeview.column("id", width=50, anchor="w")
		self.kunde_frame_treeview_bookinger_treeview.column("rejseid", width=100, anchor="w")
		self.kunde_frame_treeview_bookinger_treeview.column("pladser", width=100, anchor="w")

		self.kunde_frame_treeview_bookinger_treeview.heading("#0", text="", anchor="w")
		self.kunde_frame_treeview_bookinger_treeview.heading("id", text="Id", anchor="center")
		self.kunde_frame_treeview_bookinger_treeview.heading("rejseid", text="Rejseid", anchor="center")
		self.kunde_frame_treeview_bookinger_treeview.heading("pladser", text="Pladser", anchor="center")

		self.kunde_frame_treeview_bookinger_treeview.tag_configure("evenrow", background=self.evenrow_background, foreground=self.text_color)
		self.kunde_frame_treeview_bookinger_treeview.tag_configure("oddrow", background=self.oddrow_background, foreground=self.text_color)

		self.kunde_frame_treeview_bookinger_treeview.bind("<ButtonRelease-1>", lambda event: self.select_id(self.kunde_frame_treeview_rejse_treeview, "rejseid"))

		self.kunde_frame_buttons = tk.Frame(self.kunde_frame, bg=self.gui_background_color)
		self.kunde_frame_buttons.grid(row=1, column=0)

		self.kunde_frame_back_button = tk.Button(self.kunde_frame_buttons, text="Annuller", relief="flat", bg=self.secondary_bg_color, fg=self.text_color,
		                                         activebackground=self.button_press_color, font=("Arial", 20), command=lambda: self.change_window(self.acc_frame))
		self.kunde_frame_back_button.grid(row=1, column=0, pady=(30, 0), padx=(0, 30))

		self.kunde_frame_book_rejse_button = tk.Button(self.kunde_frame_buttons, text="Annuller", relief="flat", bg=self.secondary_bg_color, fg=self.text_color,
		                                         activebackground=self.button_press_color, font=("Arial", 20), command=lambda: self.change_window(self.acc_frame))
		self.kunde_frame_book_rejse_button.grid(row=1, column=1, pady=(30, 0))

	def delete_rejse(self):
		if not self.selected[1] == "rejseid" or self.selected[0] == -1:
			return
		pbdb.soft_delete_rejse(pbdb.get_record(pbd.Rejse, self.selected[0]))
		self.selected = [-1, "", 0]
		refresh_treeview(self.admin_treeview, pbdb.select_all(pbd.Rejse))

	def opret_rejse(self):
		rute = self.admin_entry_frame_rute_entry.get()
		dato = self.admin_entry_frame_dato_entry.get()
		pladskapacitet = self.admin_entry_frame_pladskapacitet_entry.get()
		if rute == "" or dato == "" or pladskapacitet == "":
			self.acc_create_label_frame_label_error.configure(text="Manglende information")
			return
		try:
			pbdb.insert_data(pbdb.Rejse(rute=rute, dato=dato, pladskapacitet=int(pladskapacitet)))
		except ValueError:
			self.acc_create_label_frame_label_error.configure(text="Pladskapacitet skal være et tal!")
			return
		refresh_treeview(self.admin_treeview, pbdb.select_all(pbd.Rejse))
		self.acc_create_label_frame_label_error.configure(text="")
		self.admin_entry_frame_rute_entry.delete(0, tk.END)
		self.admin_entry_frame_dato_entry.delete(0, tk.END)
		self.admin_entry_frame_pladskapacitet_entry.delete(0, tk.END)

	def login(self):
		if not self.selected[1] == "kundeid" or self.selected[0] == -1:
			return
		self.kundeid = self.selected[0]
		self.auth = self.selected[2]
		self.selected = [-1, "", 0]
		if self.auth == 1:
			self.change_window(self.admin_frame)
		else:
			self.change_window(self.kunde_frame)
			fill_treeview(self.kunde_frame_treeview_rejse_treeview, pbdb.select_all(pbd.Rejse), pbdb.get_all_bookinger(self.kundeid))
			fill_treeview(self.kunde_frame_treeview_bookinger_treeview, pbdb.get_all_bookinger(self.kundeid))

	def change_window(self, next_window):
		self.current_window.place_forget()
		next_window.place(relx=0.5, rely=0.5, anchor="center")
		self.current_window = next_window

	def create_account(self):
		efternavn = self.acc_create_label_frame_entry_efternavn.get()
		kontaktinfo = self.acc_create_label_frame_entry_kontaktinfo.get()
		if efternavn == "" or kontaktinfo == "":
			self.acc_create_label_frame_label_missing_info.configure(text="Manglende information")
			return
		self.acc_create_label_frame_label_missing_info.configure(text="")
		self.kundeid = pbdb.insert_data(pbd.Kunde(efternavn=efternavn, kontakt=kontaktinfo, auth=pbd.PermissionLevel.LOW))
		self.change_window(self.acc_frame)
		refresh_treeview(self.acc_treeview, pbdb.select_all(pbd.Kunde))

	def select_id(self, treeview, type_):
		sel = treeview.focus()
		if len(sel) < 1:
			return
		values = treeview.item(sel, "values")
		self.selected = [int(values[0]), type_, int(values[3])]


def empty_treeview(treeview):
	treeview.delete(*treeview.get_children())


def refresh_treeview(treeview, values, cond1=()):
	empty_treeview(treeview)
	fill_treeview(treeview, values, cond1)


def fill_treeview(treeview, values, cond1=()):
	count = 0
	for records in values:
		if records.valid():
			if records not in cond1:
				if count % 2 == 0:
					treeview.insert(parent='', index='end', text='', values=records.convert_to_tuple(), tags='evenrow')
				else:
					treeview.insert(parent='', index='end', text='', values=records.convert_to_tuple(), tags='oddrow')
				count += 1


if __name__ == "__main__":
	plusbus = Plusbus()
	plusbus.gui.mainloop()
