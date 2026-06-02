"""Opgave "Calculator with GUI"

Løs opgave 0700_calculator_exercise.py med en GUI

Kopier denne fil til din egen løsningsmappe. Skriv din løsning i kopien.

Hvis du går i stå, spørg Google, andre elever, en AI eller læreren.

Når dit program er færdigt, skub det til dit GitHub-repository.
"""

import tkinter as tk
# from tkinter import ttk


class Calculator:

	def __init__(self):
		self.gui_background_color = "#e0e0e0"
		self.button_color = "#adadad"
		self.test_color = "#0062ff"
		self.result = 0
		self.font_size = 30

		self.gui = tk.Tk()
		self.gui.title("Calculator")
		self.gui.geometry("350x500")

		self.gui.resizable(False, False)
		self.gui.configure(bg=self.gui_background_color)

		self.result_frame = tk.Frame(self.gui, bg=self.gui_background_color, width=350, height=100)
		self.result_frame.grid_propagate(False)
		self.result_frame.grid(row=0, column=0)

		self.result_label = tk.Label(self.result_frame, bg=self.gui_background_color, text=self.result, font=("Arial", self.font_size))
		self.result_label.grid(row=0, column=0, pady=50)

		self.button_frame = tk.Frame(self.gui, bg=self.button_color, width=350, height=400)
		self.button_frame.grid_propagate(False)
		self.button_frame.grid(row=1, column=0)

		self.button_1 = Button(self.button_frame, self.button_color, self.button_color, "Test", 5, 6)

	def set_result(self, number):
		new_size = (30 - (len(str(number)) - 15) * 2) if len(str(number)) > 15 else 30
		self.font_size = new_size if new_size > 15 else 15
		print(self.font_size)
		self.result_label.configure(text=number, font=("Arial", self.font_size))

class Button:

	instances = 0
	horizontal_buttons = 4

	def __init__(self, frame, background_color, focused_color, text, padx, pady):
		row = Button.get_instances() // 4
		column = Button.get_instances() - (row * 4)
		button_width = int(frame.cget("width") / Button.horizontal_buttons - padx * 8)
		self.button = tk.Button(frame, bg=background_color, activebackground=focused_color, text=text, width=button_width, height=int(button_width * 0.75))
		self.button.grid(row=row, column=column, padx=padx, pady=pady)
		Button.instances += 1

	@staticmethod
	def get_instances():
		return Button.instances


if __name__ == "__main__":
	calculator = Calculator()

	calculator.gui.mainloop()
