# import tkinter as tk
# from tkinter import ttk
# from PIL import ImageTk, Image
#
# class BackgroundImage(tk.Frame):
# 	def __init__(self, parent, *pargs):
# 		tk.Frame.__init__(self, parent, *pargs)
#
# 		self.img = Image.open("./images/bg.png")
# 		self.img_copy = self.img.copy()
#
# 		self.bg_img = ImageTk.PhotoImage(self.img)
#
# 		self.bg = tk.Label(self, image=self.bg_img)
# 		self.bg.place(x=0, y=0, relwidth=1, relheight=1)
# 		# self.bg.pack(fill="both", expand=True)
# 		self.bg.bind("<Configure>", self._resize_image)
#
# 	def _resize_image(self, event):
#
# 		new_width = event.width
# 		new_height = event.height
#
# 		self.img = self.img_copy.resize((new_width, new_height))
#
# 		self.bg_img = ImageTk.PhotoImage(self.img)
# 		self.bg.configure(image=self.bg_img)
#
# class WeatherApp:
#
# 	def __init__(self):
# 		self.root = tk.Tk()
# 		self.root.title("Weather app")
# 		self.root.geometry("1200x700")
# 		self.root.wm_attributes("-fullscreen", True)
# 		self.root.wm_attributes("-transparentcolor", "white")
# 		self.root.config(bg="white")
# 		self.root.wm_iconphoto(False, ImageTk.PhotoImage(Image.open("./images/icon.png")))
# 		# self.root.attributes("-alphacolor", 0.5)
# 		self.root.bind("<Escape>", self.end_fullscreen)
# 		self.root.bind("<F11>", self.toggle_fullscreen)
# 		self.fullscreen = True
# 		self.bg = BackgroundImage(self.root)
# 		self.bg.pack(fill="both", expand=True)
# 		self.gui = tk.Label(self.root, text="MMMMMMMMMMMMMMM", font=("Arial", 50), bg="magenta")
# 		self.gui.place(relx=0.5, rely=0.5)
# 		self.gui.config(bg="white")
#
# 	# def transparent_bg(self, element):
# 	# 	element.wm_attributes
#
# 	def toggle_fullscreen(self, event=None):
# 		self.fullscreen = not self.fullscreen
# 		self.root.attributes("-fullscreen", self.fullscreen)
# 		return "break"
#
# 	def end_fullscreen(self, event=None):
# 		self.fullscreen = False
# 		self.root.attributes("-fullscreen", False)
# 		return "break"
#
#
# if __name__ == "__main__":
# 	weatherApp = WeatherApp()
# 	weatherApp.root.mainloop()
from PyQt6.QtCore import Qt
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *


class WeatherApp:

	def __init__(self):

		self.app = QApplication([])
		self.main_win = MainWindow()
		self.layout = QWidget(parent=self.main_win)
		self.main_win.setCentralWidget(self.layout)

		self.holder = QWidget()
		self.holder.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Expanding)
		self.holder.setMaximumWidth(800)
		self.holder.setStyleSheet("""
			QWidget {
				border: 10px solid red;
			}
		""")

		vbox = QGridLayout()
		vbox.addWidget(self.holder)
		vbox.setContentsMargins(150, 50, 150, 50)

		self.layout.setLayout(vbox)

		self.main_win.show()
		self.main_win.showFullScreen()

class MainWindow(QMainWindow):

	def __init__(self):
		super().__init__()
		self.setWindowTitle("Weather App")
		self.setWindowIcon(QIcon("./images/icon.png"))
		self.setMinimumSize(600, 350)
		self.setMaximumSize(1920, 1080)
		self.setGeometry(50, 50, 1200, 700)

		self.fullScreen = True

		self.setStyleSheet("""
				QMainWindow {
					background-image: url("./images/bg.png");
					background-repeat: no-repeat;
					background-position: center;
				}
		""")

	def keyPressEvent(self, event: QKeyEvent):
		k = event.key()
		if k == Qt.Key.Key_F11:
			self.toggleFullScreen(self.fullScreen)
		elif k == Qt.Key.Key_Escape:
			self.toggleFullScreen(True)

	def toggleFullScreen(self, bool_):
		if bool_:
			if self.fullScreen != bool_:
				return
			self.showNormal()
		else:
			self.showFullScreen()
		self.fullScreen = not self.fullScreen


if __name__ == "__main__":
	weatherapp = WeatherApp()
	weatherapp.app.exec()
