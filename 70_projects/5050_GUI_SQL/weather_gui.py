from PyQt6.QtCore import Qt
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6 import uic
from weather_data import Weather, City, CityNotFoundException
import weather_database


main_stylesheet = """
	QWidget[objectName="scroll_area"], QWidget[objectName="scroll_area_grid"] {
		background: transparent;
	}
"""

add_city_btn_stylesheet = """
	QPushButton[objectName="add_city_btn"] {
		font: 50pt "Arial";
		background: rgba(125, 125, 125, 0.75);
		border-radius: 30px;
	}
	QPushButton[objectName="add_city_btn"]:hover {
		background: rgba(160, 160, 160, 0.75);
	}
	
	QPushButton[objectName="add_city_btn"]:pressed {
		background: rgba(125, 125, 125, 0.75);
	}
"""

add_city_widget_stylesheet = """
	QFrame[cssClass="content"] {
		background: rgb(125, 125, 125);
		color: white;
	}
	QLabel[cssClass="failed"] {
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

city_frame_stylesheet = """
	QFrame[cssClass="cityframe"] {
		background: rgba(125, 125, 125, 0.75);
		border-radius: 10px;
	}
	QFrame[cssClass="cityframe"]:hover {
		background: rgba(160, 160, 160, 0.75);
	}
	QFrame[cssClass="cityframe"]:pressed {
		background: rgba(125, 125, 125, 0.75);
	}
	QLabel[cssClass="bigfont"] {
		font: 30pt "Arial";
	}
	QLabel[cssClass="smallfont"] {
		font: 25pt "Arial";
	}
"""

city_detailed_frame_stylesheet = """
	QFrame {
		background: rgba(125, 125, 125, 0.75);
		border-radius: 10px;
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

		for city_from_database in weather_database.get_all_records(City):
			self.addCityFrame(city_from_database.city)

		self.main_win.show()
		self.main_win.showFullScreen()

	def addCityFrame(self, city):
		weather = Weather(city)
		self.main_win.scroll_area_content.layout().insertWidget(0, CityFrame(self.main_win, weather))

class MainWindow(QMainWindow):

	def __init__(self):
		super(MainWindow, self).__init__()
		uic.loadUi(r".\design.ui", self)
		self.scroll_area.setStyleSheet(main_stylesheet)
		self.add_city_btn.setStyleSheet(add_city_btn_stylesheet)
		self.add_city_btn.clicked.connect(self.add_city_press)
		self.city_detailed_frame = QCityDetailedFrame()
		self.layout.layout().addWidget(self.city_detailed_frame)
		self.city_detailed_frame.hide()

		self.add_city_layout = QGridLayout()
		self.add_city_layout.setContentsMargins(0, 0, 0, 0)
		self.add_city_layout.setSpacing(0)
		self.add_city_widget = QWidget()
		self.add_city_widget.setLayout(self.add_city_layout)
		self.add_city_widget.setStyleSheet(add_city_widget_stylesheet)

		self.add_city_content = QFrame()
		self.add_city_content.setProperty("cssClass", "content")
		self.add_city_content.setMinimumHeight(200)
		self.add_city_content.setMaximumHeight(200)
		self.add_city_content.setMinimumWidth(400)
		self.add_city_content.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)

		self.failed_label = QLabel("Ukendt by")
		self.failed_label.setProperty("cssClass", "failed")
		addShadows(self.failed_label)

		self.verticalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
		self.add_city_layout.addItem(self.verticalSpacer, 0, 1)
		self.add_city_layout.addWidget(self.failed_label, 1, 1)
		self.add_city_layout.setAlignment(self.failed_label, Qt.AlignmentFlag.AlignHCenter)
		self.add_city_layout.addWidget(self.add_city_content, 2, 1)
		self.add_city_layout.addItem(self.verticalSpacer, 3, 1)

		self.layout.layout().addWidget(self.add_city_widget, 0, 1)

		self.city_frame_layout = QVBoxLayout()
		self.add_city_layout.setContentsMargins(0, 0, 0, 0)
		self.add_city_layout.setSpacing(0)
		self.add_city_content.setLayout(self.city_frame_layout)

		#
		# Add content to add city frame
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
		self.cancel_btn.clicked.connect(self.cancelAddCity)
		self.cancel_btn.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
		self.add_btn = QPushButton("Tilføj by")
		self.add_btn.clicked.connect(self.addCity)
		self.add_btn.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)

		self.container_lo.addWidget(self.cancel_btn)
		self.container_lo.addWidget(self.add_btn)

		self.city_frame_layout.addWidget(self.text_ed)
		self.city_frame_layout.addWidget(self.container_widget)

		self.failed_label.hide()
		self.add_city_widget.hide()

		self.fullScreen = True

	def addCity(self):
		if len(self.text_ed.toPlainText()) < 1:
			return
		if (weather_database.get_record(self.text_ed.toPlainText().lower())) is not None:
			self.failed_label.setText("By allerede tilføjet")
			self.failed_label.show()
			return
		try:
			weather = Weather(self.text_ed.toPlainText())
			weather_database.insert_data(City(city=self.text_ed.toPlainText().lower()))
			self.scroll_area_content.layout().insertWidget(0, CityFrame(self, weather))
			self.text_ed.setPlainText("")
			self.add_city_widget.hide()
			self.failed_label.hide()
		except CityNotFoundException:
			self.failed_label.setText("Ukendt by")
			self.failed_label.show()

	def cancelAddCity(self):
		self.text_ed.setPlainText("")
		self.add_city_widget.hide()
		self.failed_label.hide()
		self.add_city_widget.hide()

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

	def add_city_press(self):
		if not self.add_city_widget.isHidden():
			return
		self.add_city_widget.show()

class TextEdit(QPlainTextEdit):

	def __init__(self, inst: MainWindow):
		super(TextEdit, self).__init__()
		self.inst = inst

	def keyPressEvent(self, e: QKeyEvent):
		k = e.key()
		if k == Qt.Key.Key_Enter or k == Qt.Key.Key_Return:
			self.inst.addCity()
			e.ignore()
			return
		super().keyPressEvent(e)

class QCityDetailedFrame(QFrame):

	def __init__(self):
		super(QCityDetailedFrame, self).__init__()
		self.weather = None
		self.setMaximumWidth(800)
		self.setStyleSheet(city_detailed_frame_stylesheet)

	def show(self, weather: Weather):
		print(self.weather)
		super().show()
		self.weather = weather
		print(self.weather)

class CityFrame(QFrame):

	def __init__(self, parent: MainWindow, weather: Weather):
		super(CityFrame, self).__init__()
		self.weather = weather;
		self.parent = parent
		self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
		self.setMinimumHeight(200)
		self.setMaximumHeight(200)
		self.setProperty("cssClass", "cityframe")
		self.setStyleSheet(city_frame_stylesheet)
		layout = QGridLayout()
		layout.setContentsMargins(30, 30, 30, 0)
		layout.setSpacing(10)

		self.city_label = QLabel(weather.city)
		self.city_label.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
		self.temp_label = QLabel(f"{round(weather.temp)} °C")
		self.temp_label.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
		self.weather_label = QLabel(f"{weather.weather} {Weather.get_icon_from_weather(weather.weather, weather.weather_detailed)}")
		self.weather_label.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
		self.wind_label = QLabel(f"{weather.wind_speed:.1f} m/s ༄")
		self.wind_label.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
		self.verticalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

		self.city_label.setProperty("cssClass", "bigfont")
		self.temp_label.setProperty("cssClass", "bigfont")
		self.weather_label.setProperty("cssClass", "smallfont")
		self.wind_label.setProperty("cssClass", "smallfont")

		addShadows(self.city_label, self.temp_label, self.weather_label, self.wind_label)

		layout.addWidget(self.city_label, 0, 0)
		layout.addWidget(self.temp_label, 0, 1)
		layout.addWidget(self.weather_label, 1, 0)
		layout.addWidget(self.wind_label, 1, 1)
		layout.addItem(self.verticalSpacer, 2, 0)
		layout.addItem(self.verticalSpacer, 2, 1)

		layout.setAlignment(self.city_label, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
		layout.setAlignment(self.temp_label, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)
		layout.setAlignment(self.weather_label, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
		layout.setAlignment(self.wind_label, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)

		self.setLayout(layout)

	def mousePressEvent(self, e: QMouseEvent):
		self.parent.scroll_area.hide()
		self.parent.city_detailed_frame.show(self.weather)


if __name__ == "__main__":
	weatherapp = WeatherApp()
	weatherapp.exec()
