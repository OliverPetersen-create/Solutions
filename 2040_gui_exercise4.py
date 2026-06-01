""" Opgave "GUI step 4":

Som altid skal du læse hele opgavebeskrivelsen omhyggeligt, før du begynder at løse opgaven.

Kopier denne fil til din egen løsningsmappe. Skriv din løsning ind i kopien.

--------

Bruge det, du har lært i GUI-eksempelfilerne, og byg den GUI, der er afbildet i images/gui_2040.png

Genbrug din kode fra "GUI step 3".

Fyld treeview'en med testdata.
Leg med farveværdierne. Find en farvekombination, som du kan lide.

Funktionalitet:
    Klik på knappen "clear entry boxes" sletter teksten i alle indtastningsfelter (entries).
    Hvis du klikker på en datarække i træoversigten, kopieres dataene i denne række til indtastningsfelterne.

--------

Når dit program er færdigt, skal du skubbe det til dit github-repository.
"""

import tkinter as tk
from tkinter import ttk


def clear_entries():
	entry_id.delete(0, tk.END)
	entry_weight.delete(0, tk.END)
	entry_destination.delete(0, tk.END)
	entry_weather.delete(0, tk.END)

def create_data(tree):
	if entry_id.get() == "" or entry_weight.get() == "" or entry_destination.get() == "":
		return
	data.append((entry_id.get(), entry_weight.get(), entry_destination.get()))
	if (len(data) - 1) % 2 == 0:
		tree.insert(parent='', index='end', text='', values=data[-1], tags='evenrow')
	else:
		tree.insert(parent='', index='end', text='', values=data[-1], tags='oddrow')
	clear_entries()

def remove_data(tree):
	if len(tree.selection()) < 1:
		return
	sel = tree.selection()[0]
	clear_entries()
	tree.delete(sel)

def insert_data(tree):
	count = 0
	for records in data:
		if count % 2 == 0:
			tree.insert(parent='', index='end', text='', values=records, tags='evenrow')
		else:
			tree.insert(parent='', index='end', text='', values=records, tags='oddrow')
		count += 1

def edit_record(tree):  # Kunne ikke lide at den sagde at den klagede over at man ikke brugte event, så prøvede at fjerne det, og det ser stadig ud til at du
	sel = tree.focus()
	if len(sel) < 1:
		return
	values = tree.item(sel, "values")
	clear_entries()
	entry_id.insert(0, values[0])
	entry_weight.insert(0, values[1])
	entry_destination.insert(0, values[2])


data = [("1", "heh", "københavn"),
        ("2", "test", "københavn"),
        ("3", "jhjh", "københavn"),
        ("4", "seys", "københavn"),
        ("5", "luhl", "københavn"),
        ("6", "123", "københavn"),
        ("7", 5678, "københavn"),
        (8, "heh", "københavn"),
        (9, True, "københavn"),
        (10, False, "københavn"),
        (11, [1, 2, 3], "københavn"),
        ("12", 17.35, "københavn"),
        ("13", "yes", "københavn"),
        ("14", "no", "københavn"),
        ("15", {"Hej": 12, "Med": "Dig"}, "københavn")
        ]

padx = 8
pady = 4
rowheight = 24
treeview_background = "#eeeeee"
treeview_foreground = "black"
treeview_selected = "#773333"
evenrow_background = "#00bfff"
oddrow_background = "#4fd3ff"

gui = tk.Tk()
gui.title("my first GUI")
gui.geometry("600x500")

label_frame = tk.LabelFrame(gui, text="Container", padx=10)

style = ttk.Style()
style.theme_use("default")
style.configure("Treeview", background=treeview_background, foreground=treeview_foreground, rowheight=rowheight, fieldbackground=treeview_background)
style.map("Treeview", background=[("selected", treeview_selected)])

frame_treeview = tk.Frame(label_frame)
tree_1_scrollbar = tk.Scrollbar(frame_treeview)
tree_1_scrollbar.grid(row=0, column=1, pady=pady, sticky="ns")
tree_1 = ttk.Treeview(frame_treeview, yscrollcommand=tree_1_scrollbar.set, selectmode="browse")
tree_1.grid(row=0, column=0, pady=pady)
tree_1_scrollbar.config(command=tree_1.yview)

tree_1['columns'] = ("id", "weight", "destination")
tree_1.column("#0", width=0, stretch=tk.NO)
tree_1.column("id", width=30, anchor="w")
tree_1.column("weight", width=100, anchor="w")
tree_1.column("destination", width=200, anchor="w")

tree_1.heading("#0", text="", anchor="w")
tree_1.heading("id", text="Id", anchor="center")
tree_1.heading("weight", text="Weight", anchor="center")
tree_1.heading("destination", text="Destination", anchor="center")

tree_1.tag_configure("evenrow", background=evenrow_background)
tree_1.tag_configure("oddrow", background=oddrow_background)

tree_1.bind("<ButtonRelease-1>", lambda event: edit_record(tree_1))  # Kunne ikke lide at den sagde at den klagede over at man ikke brugte event, så prøvede at fjerne det, og det ser stadig ud til at du

frame_entries = tk.Frame(label_frame)
label_id = tk.Label(frame_entries, text="Id")
label_weight = tk.Label(frame_entries, text="Weight")
label_destination = tk.Label(frame_entries, text="Destination")
label_weather = tk.Label(frame_entries, text="Weather")
entry_id = tk.Entry(frame_entries, width=5)
entry_weight = tk.Entry(frame_entries, width=8)
entry_destination = tk.Entry(frame_entries, width=18)
entry_weather = tk.Entry(frame_entries, width=15)

frame_buttons = tk.Frame(label_frame)
button_create = tk.Button(frame_buttons, text="Create", command=lambda: create_data(tree_1))
button_update = tk.Button(frame_buttons, text="Update")
button_delete = tk.Button(frame_buttons, text="Delete", command=lambda: remove_data(tree_1))
button_clear = tk.Button(frame_buttons, text="Clear Entry Boxes", command=clear_entries)

label_frame.grid(row=0, column=0, padx=padx, pady=pady)

frame_entries.grid(row=1, column=0, padx=padx, pady=pady)
label_id.grid(row=0, column=0, padx=padx, pady=pady)
label_weight.grid(row=0, column=1, padx=padx, pady=pady)
label_destination.grid(row=0, column=2, padx=padx, pady=pady)
label_weather.grid(row=0, column=3, padx=padx, pady=pady)
entry_id.grid(row=1, column=0, padx=padx, pady=pady)
entry_weight.grid(row=1, column=1, padx=padx, pady=pady)
entry_destination.grid(row=1, column=2, padx=padx, pady=pady)
entry_weather.grid(row=1, column=3, padx=padx, pady=pady)

frame_buttons.grid(row=2, column=0, padx=padx, pady=pady)
button_create.grid(row=0, column=0, padx=padx, pady=pady)
button_update.grid(row=0, column=1, padx=padx, pady=pady)
button_delete.grid(row=0, column=2, padx=padx, pady=pady)
button_clear.grid(row=0, column=3, padx=padx, pady=pady)

frame_treeview.grid(row=0, column=0, padx=padx, pady=pady)

insert_data(tree_1)

if __name__ == "__main__":
	gui.mainloop()
