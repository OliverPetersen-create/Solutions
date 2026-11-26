from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *


class Game(QApplication):

	def __init__(self):
		super(Game, self).__init__([])
		self.main_win = MainWindow()
		self.main_win.show()
		self.main_win.showFullScreen()


main_stylesheet = """
	MainWindow {
		background-image: url("assets/wall");
		background-position: center;
		background-size: cover;
	}
	QWidget[class="text_frame"] {
		background: rgba(0, 255, 0, 0.5);
	}
	QLabel {
		font-size: 20pt;
		color: black;
		
	}
	
"""


def delLOSpace(layout):
	layout.setContentsMargins(0, 0, 0, 0)
	layout.setSpacing(0)


class MainWindow(QMainWindow):

	def __init__(self):
		super(MainWindow, self).__init__()
		center = self.screen().geometry().center()
		self.setGeometry(center.x() - 600, center.y() - 350, 1200, 700)
		self.setMinimumSize(600, 350)
		self.setWindowTitle("Text Game")
		self.setStyleSheet(main_stylesheet)
		self.fullscreen = True

		self.central_widget = QWidget()
		self.setCentralWidget(self.central_widget)
		self.lo = QVBoxLayout()
		delLOSpace(self.lo)
		self.lo.setSpacing(30)
		self.central_widget.setLayout(self.lo)

		self.response_holder = QFrame()
		self.response_holder.setProperty("class", "test1")
		self.response_lo = QVBoxLayout()
		self.response_holder.setLayout(self.response_lo)
		self.response_lo.setContentsMargins(0, 0, 0, 0)
		self.response_lo.setSpacing(10)

		self.lower_holder = QWidget()
		self.lower_lo = QHBoxLayout()
		self.lower_holder.setLayout(self.lower_lo)
		delLOSpace(self.lower_lo)
		self.lower_lo.setSpacing(30)

		self.actions_holder = QFrame()
		self.actions_holder.setProperty("class", "test2")
		self.actions_lo = QVBoxLayout()
		self.actions_holder.setLayout(self.actions_lo)
		delLOSpace(self.actions_lo)
		self.actions_lo.setSpacing(10)

		self.inventory_icon = QLabel()
		self.inventory_icon.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
		pixmap = QPixmap("assets/backpack.png").scaled(64, 64, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
		self.inventory_icon.setProperty("class", "test3")
		self.inventory_icon.setPixmap(pixmap)

		self.lo.addWidget(self.response_holder)
		self.lo.addWidget(self.lower_holder)
		self.lower_lo.addWidget(QWidget())
		self.lower_lo.addWidget(self.actions_holder)
		self.lower_lo.addWidget(self.inventory_icon)

		self.response_lo.addStretch()
		self.response_lo.addWidget(Response("Test"))
		self.response_lo.addWidget(Response("Hej med dig jeg er ikke klar over om det her er særlig godt at gøre det her er er mget meget meget god historie"))
		self.response_lo.addWidget(Response("Test response3"))
		self.response_lo.addStretch()

		self.actions_lo.addWidget(Action("Click this button"))
		self.actions_lo.addWidget(Action("Maybe this one"))
		self.actions_lo.addWidget(Action("Or this one"))
		self.actions_lo.addStretch()


	def keyPressEvent(self, e: QKeyEvent):
		k = e.key()
		if k == Qt.Key.Key_F11:
			self.fullscreen = not self.fullscreen
			self.toggleFullscreen(self.fullscreen)
		elif k == Qt.Key.Key_Escape:
			self.deleteLater()
			# self.fullscreen = False
			# self.toggleFullscreen(False)

	def toggleFullscreen(self, state):
		if state:
			self.showFullScreen()
		else:
			if not self.isFullScreen():
				return
			self.showNormal()


class Response(QFrame):

	def __init__(self, text):
		super(Response, self).__init__()
		self.lo = QHBoxLayout()
		delLOSpace(self.lo)
		self.setLayout(self.lo)
		self.label = QLabel(text)
		self.label.setProperty("class", "text_frame")
		self.label.setContentsMargins(30, 5, 30, 10)
		self.label.setWordWrap(True)
		self.lo.addStretch()
		self.lo.addWidget(self.label)
		self.lo.addStretch()

class Action(QPushButton):

	actions = 0

	def __init__(self, text):
		super(Action, self).__init__()
		self.setProperty("class", "text_frame")
		self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
		Action.actions += 1
		self.lo = QGridLayout()
		delLOSpace(self.lo)
		self.setLayout(self.lo)
		self.label = QLabel(f"{Action.actions}.) {text}")
		self.lo.addWidget(self.label, 0, 0)
		self.label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
		self.label.setWordWrap(True)

	def __del__(self):
		Action.actions -= 1


if __name__ == "__main__":
	game = Game()
	game.exec()
