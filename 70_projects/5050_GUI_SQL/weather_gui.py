from PyQt6.QtCore import Qt
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6 import uic
from weather_data import Weather, Location, LocationNotFoundException
import weather_database

main_stylesheet = """
	QWidget[objectName="scroll_area"], QWidget[objectName="scroll_area_grid"]{
		background: transparent;
	}
"""

add_location_btn_stylesheet = """
	QPushButton[objectName="add_location_btn"] {
		font: 50pt "Arial";
		background: rgba(125, 125, 125, 0.75);
		border-radius: 30px;
	}
	QPushButton[objectName="add_location_btn"]:hover {
		background: rgba(160, 160, 160, 0.75);
	}
	
	QPushButton[objectName="add_location_btn"]:pressed {
		background: rgba(125, 125, 125, 0.75);
	}
"""

add_location_widget_stylesheet = """
	QFrame[class="content"] {
		background: rgb(125, 125, 125);
		color: white;
	}
	QLabel[class="failed"] {
		font: 50pt "Arial";
		color: red;
	}
	QPlainTextEdit {
		font: 50pt "Arial";
		border: none;
		border-bottom: 3px solid rgb(75, 75, 75);
	}
	QPushButton {
		font: 40pt "Arial";
	}
"""

location_frame_stylesheet = """
	QFrame[class="locationframe"] {
		background: rgba(125, 125, 125, 0.75);
		border-radius: 10px;
	}
	QFrame[class="locationframe"]:hover {
		background: rgba(160, 160, 160, 0.75);
	}
	QLabel[class="bigfont"] {
		font: 30pt "Arial";
		
	}
	QLabel[class="smallfont"] {
		font: 25pt "Arial";
	}
"""


def addShadows(*labels):
	for label in labels:
		drop_shadow = QGraphicsDropShadowEffect()
		drop_shadow.setBlurRadius(1)
		drop_shadow.setOffset(3, 3)
		label.setGraphicsEffect(drop_shadow)


class WeatherApp(QApplication):

	def __init__(self):
		super(WeatherApp, self).__init__([])
		self.main_win = MainWindow()

		for location_from_database in weather_database.get_all_records(Location):
			self.addLocationFrame(location_from_database.location)

		self.main_win.show()
		self.main_win.showFullScreen()

	def addLocationFrame(self, location):
		weather = Weather(location)
		self.main_win.scroll_area_content.layout().insertWidget(0, LocationFrame(self.main_win, weather))


class MainWindow(QMainWindow):

	def __init__(self):
		super(MainWindow, self).__init__()
		uic.loadUi(r".\design.ui", self)
		self.scroll_area.setStyleSheet(main_stylesheet)
		self.add_location_btn.setStyleSheet(add_location_btn_stylesheet)
		self.add_location_btn.clicked.connect(self.add_location_press)
		self.location_detailed_widget = LocationDetailedFrame()
		self.layout.layout().addWidget(self.location_detailed_widget, 0, 1)

		# self.location_detailed_widget.hide()
		self.scroll_area.hide()

		self.add_location_layout = QGridLayout()
		self.add_location_layout.setContentsMargins(0, 0, 0, 0)
		self.add_location_layout.setSpacing(0)
		self.add_location_widget = QWidget()
		self.add_location_widget.setLayout(self.add_location_layout)
		self.add_location_widget.setStyleSheet(add_location_widget_stylesheet)

		self.add_location_content = QFrame()
		self.add_location_content.setProperty("class", "content")
		self.add_location_content.setMinimumHeight(200)
		self.add_location_content.setMaximumHeight(200)
		self.add_location_content.setMinimumWidth(400)
		self.add_location_content.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)

		self.failed_label = QLabel("Ukendt lokation")
		self.failed_label.setProperty("class", "failed")
		addShadows(self.failed_label)

		self.verticalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
		self.add_location_layout.addItem(self.verticalSpacer, 0, 1)
		self.add_location_layout.addWidget(self.failed_label, 1, 1)
		self.add_location_layout.setAlignment(self.failed_label, Qt.AlignmentFlag.AlignHCenter)
		self.add_location_layout.addWidget(self.add_location_content, 2, 1)
		self.add_location_layout.addItem(self.verticalSpacer, 3, 1)

		self.layout.layout().addWidget(self.add_location_widget, 0, 1)

		self.location_frame_layout = QVBoxLayout()
		self.add_location_layout.setContentsMargins(0, 0, 0, 0)
		self.add_location_layout.setSpacing(0)
		self.add_location_content.setLayout(self.location_frame_layout)

		#
		# Add content to add location frame
		#

		self.text_ed = TextEdit(self)
		self.text_ed.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
		self.text_ed.setMaximumHeight(100)

		self.container_lo = QHBoxLayout()
		self.container_lo.setContentsMargins(0, 0, 0, 0)
		self.container_lo.setSpacing(0)
		self.container_widget = QWidget()
		self.container_widget.setLayout(self.container_lo)
		self.cancel_btn = QPushButton("Annuller")
		self.cancel_btn.clicked.connect(self.cancelAddLocation)
		self.cancel_btn.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
		self.add_btn = QPushButton("Tilføj lokation")
		self.add_btn.clicked.connect(self.addLocation)
		self.add_btn.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)

		self.container_lo.addWidget(self.cancel_btn)
		self.container_lo.addWidget(self.add_btn)

		self.location_frame_layout.addWidget(self.text_ed)
		self.location_frame_layout.addWidget(self.container_widget)

		self.failed_label.hide()
		self.add_location_widget.hide()

		self.fullScreen = True

	def addLocation(self):
		if len(self.text_ed.toPlainText()) < 1:
			return
		if (weather_database.get_record(self.text_ed.toPlainText().lower())) is not None:
			self.failed_label.setText("Lokation allerede tilføjet")
			self.failed_label.show()
			return
		try:
			weather = Weather(self.text_ed.toPlainText())
			weather_database.insert_data(Location(location=self.text_ed.toPlainText().lower()))
			self.scroll_area_content.layout().insertWidget(0, LocationFrame(self, weather))
			self.text_ed.setPlainText("")
			self.add_location_widget.hide()
			self.failed_label.hide()
		except LocationNotFoundException:
			self.failed_label.setText("Ukendt lokation")
			self.failed_label.show()

	def cancelAddLocation(self):
		self.text_ed.setPlainText("")
		self.add_location_widget.hide()
		self.failed_label.hide()
		self.add_location_widget.hide()

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

	def add_location_press(self):
		if not self.add_location_widget.isHidden():
			return
		self.add_location_widget.show()


class TextEdit(QPlainTextEdit):

	def __init__(self, inst: MainWindow):
		super(TextEdit, self).__init__()
		self.inst = inst

	def keyPressEvent(self, e: QKeyEvent):
		k = e.key()
		if k == Qt.Key.Key_Enter or k == Qt.Key.Key_Return:
			self.inst.addLocation()
			e.ignore()
			return
		super().keyPressEvent(e)


location_detailed_frame_stylesheet = """
	QWidget[class="transparent"]{
		background: transparent;
	}
	LocationDetailedFrame[class="content_frame"] {
		background: rgba(125, 125, 125, 0.75);
		border-radius: 10px;
	}
	
	QLabel[class="title_text"] {
		font-size: 50pt;
	}
	
	QLabel {
		border: 1px solid red;
	}
	
"""

class LocationDetailedFrame(QScrollArea):

	def __init__(self):
		super(LocationDetailedFrame, self).__init__()
		self.weather = None
		self.setMaximumWidth(800)
		self.setProperty("class", "content_frame")
		self.setStyleSheet(location_detailed_frame_stylesheet)
		self.self_lo = QStackedLayout()
		self.self_lo.setProperty("class", "transparent")
		self.self_lo.setContentsMargins(0, 0, 0, 0)
		self.setLayout(self.self_lo)

		self.holder = QWidget()
		self.holder.setProperty("class", "transparent")
		self.holder_lo = QGridLayout()
		self.holder.setLayout(self.holder_lo)
		self.holder_lo.setSpacing(0)
		self.holder_lo.setContentsMargins(0, 0, 0, 0)

		self.vertical_spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
		self.horizontal_spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

		#
		# Location details:
		#

		self.title = QLabel("Høje Taastrup")
		# self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
		self.title.setProperty("class", "title_text")
		self.holder_lo.addWidget(self.title, 0, 1)

		#
		#
		#

		self.setWidget(self.holder)

	def setup(self, weather: Weather):
		self.weather = weather


class LocationFrame(QFrame):

	def __init__(self, parent: MainWindow, weather: Weather):
		super(LocationFrame, self).__init__()
		self.weather = weather
		self.parent = parent
		self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
		self.setMinimumHeight(200)
		self.setMaximumHeight(200)
		self.setProperty("class", "locationframe")
		self.setStyleSheet(location_frame_stylesheet)
		layout = QGridLayout()
		layout.setContentsMargins(30, 30, 30, 0)
		layout.setSpacing(0)

		self.location_label = QLabel(weather.location)
		self.location_label.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
		self.temp_label = QLabel(f"{round(weather.temp)} °C")
		self.temp_label.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
		self.weather_label = QLabel(f"{weather.weather}")
		self.weather_label.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
		self.weather_label.setContentsMargins(0, 0, 10, 0)
		self.weather_icon = QLabel()
		pixmap = QPixmap(f"images/{weather.weather_icon}.png")
		self.weather_icon.setPixmap(pixmap)
		self.weather_icon.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
		self.wind_label = QLabel(f"{weather.wind_speed:.1f} m/s ༄")
		self.wind_label.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
		self.vertical_spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
		self.horizontal_spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

		self.location_label.setProperty("class", "bigfont")
		self.temp_label.setProperty("class", "bigfont")
		self.weather_label.setProperty("class", "smallfont")
		self.weather_icon.setProperty("class", "smallfont")
		self.wind_label.setProperty("class", "smallfont")

		addShadows(self.location_label, self.temp_label, self.weather_label, self.wind_label)

		layout.addWidget(self.location_label, 0, 0, 1, 2)
		layout.addWidget(self.temp_label, 0, 3)
		layout.addWidget(self.weather_label, 1, 0)
		layout.addWidget(self.weather_icon, 1, 1)
		layout.addItem(self.horizontal_spacer, 1, 2)
		layout.addWidget(self.wind_label, 1, 3)
		layout.addItem(self.vertical_spacer, 2, 0)
		layout.addItem(self.vertical_spacer, 2, 3)

		layout.setAlignment(self.location_label, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
		layout.setAlignment(self.temp_label, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)
		layout.setAlignment(self.weather_label, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
		layout.setAlignment(self.weather_icon, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
		layout.setAlignment(self.wind_label, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

		self.setLayout(layout)

	def mousePressEvent(self, e: QMouseEvent):
		self.parent.scroll_area.hide()
		self.parent.location_detailed_frame.show()
		self.parent.location_detailed_frame.setup(self.weather)


if __name__ == "__main__":
	weatherapp = WeatherApp()
	weatherapp.exec()
