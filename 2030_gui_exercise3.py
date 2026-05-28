"""Opgave "GUI step 3":

Som altid skal du læse hele opgavebeskrivelsen omhyggeligt, før du begynder at løse opgaven.

Kopier denne fil til din egen løsningsmappe. Skriv din løsning ind i kopien.

--------

Bruge det, du har lært i GUI-eksempelfilerne, og byg den GUI, der er afbildet i images/gui_2030.png

Genbrug din kode fra "GUI step 2".

GUI-strukturen bør være som følger:
    main window
        labelframe
            frame
                treeview and scrollbar
            frame
                labels and entries
            frame
                buttons

Funktionalitet:
    Klik på knappen "clear entry boxes" sletter teksten i alle indtastningsfelter (entries).

--------

Når dit program er færdigt, skal du skubbe det til dit github-repository.
"""


import tkinter as tk
from tkinter import ttk

def button_press():
	print("Clear button pressed")
	entry_id.delete(0, tk.END)
	entry_weight.delete(0, tk.END)
	entry_destination.delete(0, tk.END)
	entry_weather.delete(0, tk.END)


padx = 8
pady = 4
rowheight = 24
treeview_background = "#eeeeee"
treeview_foreground = "black"
treeview_selected = "#773333"

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

tree_1['columns'] = ("weight", "destination")
tree_1.column("#0", width=30, anchor="e")
tree_1.column("weight", width=100, anchor="w")
tree_1.column("destination", width=200, anchor="w")

tree_1.heading("#0", text="Id", anchor="center")
tree_1.heading("weight", text="Weight", anchor="center")
tree_1.heading("destination", text="Destination", anchor="center")

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
button_create = tk.Button(frame_buttons, text="Create")
button_update = tk.Button(frame_buttons, text="Update")
button_delete = tk.Button(frame_buttons, text="Delete")
button_clear = tk.Button(frame_buttons, text="Clear Entry Boxes", command=button_press)

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

if __name__ == "__main__":
	gui.mainloop()
