import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image

class BackgroundImage(tk.Frame):
	def __init__(self, parent, *pargs):
		tk.Frame.__init__(self, parent, *pargs)

		self.img = Image.open("./images/test.png")
		self.img_copy = self.img.copy()

		self.bg_img = ImageTk.PhotoImage(self.img)

		self.bg = tk.Label(self, image=self.bg_img)
		self.bg.pack(fill="both", expand=True)
		self.bg.bind("<Configure>", self._resize_image)

	def _resize_image(self, event):

		new_width = event.width
		new_height = event.height

		self.img = self.img_copy.resize((new_width, new_height))

		self.bg_img = ImageTk.PhotoImage(self.img)
		self.bg.configure(image=self.bg_img)

class WeatherApp:

	def __init__(self):
		self.root = tk.Tk();
		self.root.title("Weather app")
		self.root.geometry("1200x700")
		self.root.attributes("-fullscreen", True)
		self.root.wm_iconphoto(False, ImageTk.PhotoImage(Image.open("./images/icon.png")))
		self.root.bind("<Escape>", self.end_fullscreen)
		self.root.bind("<F11>", self.toggle_fullscreen)
		self.fullscreen = True
		self.gui = tk.Frame(self.root)
		self.gui.pack(fill="both", expand=True)
		self.bg = BackgroundImage(self.gui)
		self.bg.pack(fill="both", expand=True)

	def toggle_fullscreen(self, event=None):
		self.fullscreen = not self.fullscreen
		self.root.attributes("-fullscreen", self.fullscreen)
		return "break"

	def end_fullscreen(self, event=None):
		self.fullscreen = False
		self.root.attributes("-fullscreen", False)
		return "break"


if __name__ == "__main__":
	weatherApp = WeatherApp()
	weatherApp.root.mainloop()