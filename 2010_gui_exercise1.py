"""
Opgave "GUI step 1":

Som altid skal du læse hele opgavebeskrivelsen omhyggeligt, før du begynder at løse opgaven.

Kopier denne fil til din egen løsningsmappe. Skriv din løsning ind i kopien.

--------

Bruge det, du har lært i GUI-eksempelfilerne, og byg den GUI, der er afbildet i images/gui_2010.png

--------

Når dit program er færdigt, skal du skubbe det til dit github-repository.
"""


import tkinter as tk

padx = 8
pady = 12

gui = tk.Tk()
gui.title("my first GUI")
gui.geometry("300x300")

label_frame = tk.LabelFrame(gui, text="Container")
label = tk.Label(label_frame, text="Id")
entry = tk.Entry(label_frame, justify="center", width=5)
button = tk.Button(label_frame, text="Create", command=lambda: button_press(entry.get()))
id_label = tk.Label(gui)

label_frame.grid(row=0, column=0, padx=padx, pady=pady)  # Kan godt være jeg gik overboard med padding, er ikke lige 100% sikker på om jeg forstår det helt endnu.
label.grid(row=1, column=0, padx=padx * 2.5, pady=pady)
entry.grid(row=2, column=0)
button.grid(row=3, column=0, padx=padx * 2.5, pady=pady)
id_label.grid(row=1, column=0)

def button_press(entry_id):
	# print(f"Id is {entry_id if not entry_id == '' else 'not specified'}")
	id_label.configure(text=f"Id is {entry_id if not entry_id == '' else 'not specified'}")


if __name__ == "__main__":
	gui.mainloop()
