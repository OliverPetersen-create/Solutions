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

def delLOSpace(layout):
	layout.setContentsMargins(0, 0, 0, 0)
	layout.setSpacing(0)

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
		self.location_detailed_widget = LocationDetailedFrame(self)
		self.layout.layout().addWidget(self.location_detailed_widget, 0, 1)

		self.location_detailed_widget.hide()

		self.add_location_layout = QGridLayout()
		delLOSpace(self.add_location_layout)
		self.add_location_widget = QWidget()
		self.add_location_widget.setLayout(self.add_location_layout)
		self.add_location_widget.setStyleSheet(add_location_widget_stylesheet)

		self.add_location_content = QFrame()
		self.add_location_content.setProperty("class", "content")
		self.add_location_content.setMinimumHeight(200)
		self.add_location_content.setMaximumHeight(200)
		self.add_location_content.setMinimumWidth(400)
		self.add_location_content.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)

		self.failed_label = Label("Ukendt lokation")
		self.failed_label.setProperty("class", "failed")

		self.verticalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
		self.add_location_layout.addItem(self.verticalSpacer, 0, 1)
		self.add_location_layout.addWidget(self.failed_label, 1, 1)
		self.add_location_layout.setAlignment(self.failed_label, Qt.AlignmentFlag.AlignHCenter)
		self.add_location_layout.addWidget(self.add_location_content, 2, 1)
		self.add_location_layout.addItem(self.verticalSpacer, 3, 1)

		self.layout.layout().addWidget(self.add_location_widget, 0, 1)

		self.location_frame_layout = QVBoxLayout()
		delLOSpace(self.add_location_layout)
		self.add_location_content.setLayout(self.location_frame_layout)

		#
		# Add content to add location frame
		#

		self.text_ed = TextEdit(self)
		self.text_ed.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
		self.text_ed.setMaximumHeight(100)

		self.container_lo = QHBoxLayout()
		delLOSpace(self.container_lo)
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
			weather_database.insert_data(Location(location=weather.location.lower()))
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
	QLabel[class="temp_text"] {
		font-size: 30pt;
	}
	QLabel[class="header_text"] {
		font-size: 30pt;
	}
	QLabel[class="small_text1"] {
		font-size: 25pt;
	}
	QLabel[class="small_text2"] {
		font-size: 20pt;
	}
	QPushButton[class="btn"] {
		font: 20pt "Arial";
		background: rgba(75, 75, 75, 0.75);
		padding: 20px 30px;
		border-radius: 10px;
	}
	QPushButton[class="btn"]:hover {
		background: rgba(100, 100, 100, 0.75);
	}
	
	QPushButton[class="btn"]:pressed {
		background: rgba(75, 75, 75, 0.75);
	}
	
"""

class LocationDetailedFrame(QScrollArea):

	def __init__(self, parent: MainWindow):
		super(LocationDetailedFrame, self).__init__()
		self.weather_obj: Weather = None
		self.frame: LocationFrame = None
		self.parent = parent
		self.setMaximumWidth(800)
		self.setProperty("class", "content_frame")
		self.setStyleSheet(location_detailed_frame_stylesheet)
		self.setWidgetResizable(True)
		self.inner = QWidget(self)
		self.inner.setProperty("class", "transparent")
		self.lo = QGridLayout()
		self.inner.setLayout(self.lo)
		self.lo.setContentsMargins(20, 0, 20, 0)
		self.lo.setSpacing(0)
		self.setWidget(self.inner)

		#
		# Add content inside of area
		#

		vertical_spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
		horizontal_spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

		self.title = Label("---")
		self.title.setProperty("class", "title_text")
		self.lo.addWidget(self.title, 0, 0, 1, -1)
		self.lo.setAlignment(self.title, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)

		self.temp = Label(f"---")
		self.temp.setProperty("class", "temp_text")
		self.lo.addWidget(self.temp, 1, 0, 1, -1)
		self.lo.setAlignment(self.temp, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)

		# --------- Rain/Snow ---------

		self.rs_widget = QWidget()
		self.lo.addWidget(self.rs_widget, 2, 0, 1, -1)
		self.rslo = QHBoxLayout()
		delLOSpace(self.rslo)
		self.rs_widget.setLayout(self.rslo)

		self.rain: QLabel = None
		self.snow: QLabel = None

		# --------- Weather widget ---------

		self.weather_widget = QWidget()
		self.lo.addWidget(self.weather_widget, 3, 0)
		self.wlo = QGridLayout()
		delLOSpace(self.wlo)
		self.wlo.setContentsMargins(0, 30, 0, 0)
		self.weather_widget.setLayout(self.wlo)

		self.weather = Label("---")
		self.weather.setProperty("class", "header_text")
		self.weather.setContentsMargins(0, 0, 10, 0)
		self.wlo.addWidget(self.weather, 0, 0)
		self.wlo.setAlignment(self.weather, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

		self.weather_detailed = Label("---")
		self.weather_detailed.setProperty("class", "small_text1")
		self.wlo.addWidget(self.weather_detailed, 1, 0, 1, -1)
		self.wlo.setAlignment(self.weather_detailed, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
		# self.wlo.addItem(vertical_spacer)

		self.weather_icon = QLabel()
		self.wlo.addWidget(self.weather_icon, 0, 1)
		self.wlo.setAlignment(self.weather_icon, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

		# --------- Temp widget ---------

		self.temp_widget = QWidget()
		self.lo.addWidget(self.temp_widget, 3, 2)
		self.lo.addItem(horizontal_spacer, 3, 1)
		self.tlo = QGridLayout()
		delLOSpace(self.tlo)
		self.tlo.setContentsMargins(0, 30, 0, 0)
		self.temp_widget.setLayout(self.tlo)

		self.tempf = Label("---")
		self.tempf.setProperty("class", "small_text1")
		self.tempf.setContentsMargins(0, 0, 10, 0)
		self.tlo.addWidget(self.tempf, 0, 1)
		self.tlo.setAlignment(self.tempf, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

		self.temp_freezing: QLabel = None

		self.min_temp = Label("Min")
		self.min_temp.setProperty("class", "small_text1")
		self.min_temp.setContentsMargins(40, 0, 0, 0)
		self.tlo.addWidget(self.min_temp, 1, 1, 1, 2)
		self.tlo.setAlignment(self.min_temp, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

		self.max_temp = Label("Max")
		self.max_temp.setProperty("class", "small_text1")
		self.max_temp.setContentsMargins(0, 0, 40, 0)
		self.tlo.addWidget(self.max_temp, 1, 1, 1, 2)
		self.tlo.setAlignment(self.max_temp, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

		self.min_temp_num = Label("---")
		self.min_temp_num.setProperty("class", "small_text2")
		self.min_temp_num.setContentsMargins(40, 0, 0, 0)
		self.tlo.addWidget(self.min_temp_num, 2, 1, 1, 2)
		self.tlo.setAlignment(self.min_temp_num, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

		self.max_temp_num = Label("---")
		self.max_temp_num.setProperty("class", "small_text2")
		self.max_temp_num.setContentsMargins(0, 0, 40, 0)
		self.tlo.addWidget(self.max_temp_num, 2, 1, 1, 2)
		self.tlo.setAlignment(self.max_temp_num, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

		self.tlo.addItem(horizontal_spacer, 0, 0, -1, 1)
		self.tlo.addItem(horizontal_spacer, 0, 3, -1, 1)

		# --------- Wind widget ---------

		self.wind_widget = QWidget()
		self.lo.addWidget(self.wind_widget, 4, 2)
		self.lo.addItem(horizontal_spacer, 4, 1)
		self.wilo = QGridLayout()
		delLOSpace(self.wilo)
		self.wilo.setContentsMargins(0, 30, 0, 0)
		self.wind_widget.setLayout(self.wilo)

		self.wind = Label("---")
		self.wind.setProperty("class", "header_text")
		self.wilo.addWidget(self.wind, 0, 0)
		self.wilo.setAlignment(self.wind, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)

		self.wind_deg = Label("---")
		self.wind_deg.setProperty("class", "small_text1")
		self.wilo.addWidget(self.wind_deg, 1, 0)
		self.wilo.setAlignment(self.wind_deg, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)

		# ----------------------------------

		self.humidity = Label(f"---")
		self.humidity.setContentsMargins(0, 20, 0, 0)
		self.humidity.setProperty("class", "small_text1")
		self.lo.addWidget(self.humidity, 4, 0)
		self.lo.setAlignment(self.humidity, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

		# --------- Sunrise/Sunset widget ---------

		self.sun_widget = QWidget()
		self.lo.addWidget(self.sun_widget, 5, 0, 1, -1)
		self.sunlo = QHBoxLayout()
		delLOSpace(self.sunlo)
		self.sunlo.setContentsMargins(0, 50, 0, 50)
		self.sun_widget.setLayout(self.sunlo)

		# Sunrise

		self.sunrise_widget = QWidget()
		self.sunlo.addWidget(self.sunrise_widget)
		self.sunrise_lo = QVBoxLayout()
		delLOSpace(self.sunrise_lo)
		self.sunrise_widget.setLayout(self.sunrise_lo)

		sunrise_pixmap = QPixmap(f"images/sunrise.png")
		self.sunrise_icon = QLabel()
		self.sunrise_icon.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
		self.sunrise_icon.setPixmap(sunrise_pixmap)
		self.sunrise_lo.addWidget(self.sunrise_icon)

		self.sunrise_label = Label("---")
		self.sunrise_label.setProperty("class", "small_text1")
		self.sunrise_label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
		self.sunrise_lo.addWidget(self.sunrise_label)

		# Sunset

		self.sunset_widget = QWidget()
		self.sunlo.addWidget(self.sunset_widget)
		self.sunset_lo = QVBoxLayout()
		delLOSpace(self.sunset_lo)
		self.sunset_widget.setLayout(self.sunset_lo)

		sunset_pixmap = QPixmap(f"images/sunset.png")
		self.sunset_pixmap = QLabel()
		self.sunset_pixmap.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
		self.sunset_pixmap.setPixmap(sunset_pixmap)
		self.sunset_lo.addWidget(self.sunset_pixmap)

		self.sunset_label = Label("---")
		self.sunset_label.setProperty("class", "small_text1")
		self.sunset_label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
		self.sunset_lo.addWidget(self.sunset_label)

		# ----------------------------------

		self.back_btn = QPushButton("Tilbage")
		self.back_btn.setProperty("class", "btn")
		self.back_btn.pressed.connect(self.back)
		self.del_btn = QPushButton("Slet")
		self.del_btn.setProperty("class", "btn")
		self.del_btn.pressed.connect(self.delete)
		self.lo.addWidget(self.back_btn, 6, 0, 1, -1, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
		self.lo.addWidget(self.del_btn, 6, 0, 1, -1, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

		self.lo.addItem(vertical_spacer)

	def delete(self):
		self.back()
		weather_database.delete_record(self.weather_obj.location.lower())
		for children in self.parent.scroll_area_content.children():
			if children is self.frame:
				children.setParent(None)

	def back(self):
		self.hide()
		self.parent.scroll_area.show()

	def setup(self, weather: Weather, frame: LocationFrame):
		self.weather_obj = weather
		self.frame = frame
		if self.rain or self.snow is not None:
			while self.rslo.count():
				child = self.rslo.takeAt(0)
				if child.widget():
					child.widget().deleteLater()
			self.rain = None
			self.snow = None
		if self.temp_freezing is not None:
			self.temp_freezing.deleteLater()
			self.temp_freezing = None
		self.title.setText(weather.location)
		self.temp.setText(f"{weather.temp} °C")
		self.weather.setText(weather.weather)
		self.weather_detailed.setText(weather.weather_detailed)
		pixmap = QPixmap(f"images/{weather.weather_icon}.png")
		self.weather_icon.setPixmap(pixmap)
		self.tempf.setText(f"Føles som {weather.temp_feels_like} °C")
		self.min_temp_num.setText(f"{weather.temp_min} °C")
		self.max_temp_num.setText(f"{weather.temp_max} °C")
		self.humidity.setText(f"{round(weather.humidity)}% luftfugtighed")
		self.wind.setText(f"{weather.wind_speed} meter/s vind ༄")
		self.wind_deg.setText(f"fra {round(weather.wind_deg)}° graders vinkel")
		sunrise = weather.getSunriseTime()
		sunset = weather.getSunsetTime()
		self.sunrise_label.setText(f"Solopgang\n{sunrise[0].strftime("%H:%M")}\n({sunrise[1].strftime("%H:%M")} lokal tid)")
		self.sunset_label.setText(f"Solopgang\n{sunset[0].strftime("%H:%M")}\n({sunset[1].strftime("%H:%M")} lokal tid)")
		if weather.temp_feels_like <= 1:
			self.temp_freezing = QLabel()
			pixmap = QPixmap(f"images/13n.png")
			self.temp_freezing.setPixmap(pixmap)
			self.tlo.addWidget(self.temp_freezing, 0, 2)
			self.tlo.setAlignment(self.temp_freezing, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
		if weather.rain is not None:
			self.rain = Label(f"{weather.rain['1h']}mm regn i timen")
			self.rain.setProperty("class", "header_text")
			self.rain.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
			self.rslo.addWidget(self.rain)
		if weather.snow is not None:
			self.snow = Label(f"{weather.snow['1h']}mm sne i timen")
			self.snow.setProperty("class", "header_text")
			self.snow.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
			self.rslo.addWidget(self.snow)


class Label(QLabel):

	def __init__(self, text=""):
		super(Label, self).__init__(text)
		drop_shadow = QGraphicsDropShadowEffect()
		drop_shadow.setBlurRadius(1)
		drop_shadow.setOffset(3, 3)
		self.setGraphicsEffect(drop_shadow)

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

		self.location_label = Label(weather.location)
		self.location_label.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
		self.temp_label = Label(f"{round(weather.temp)} °C")
		self.temp_label.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
		self.weather_label = Label(f"{weather.weather}")
		self.weather_label.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
		self.weather_label.setContentsMargins(0, 0, 10, 0)
		self.weather_icon = QLabel()
		pixmap = QPixmap(f"images/{weather.weather_icon}.png")
		self.weather_icon.setPixmap(pixmap)
		self.weather_icon.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
		self.wind_label = Label(f"{weather.wind_speed:.1f} m/s ༄")
		self.wind_label.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
		self.vertical_spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
		self.horizontal_spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

		self.location_label.setProperty("class", "bigfont")
		self.temp_label.setProperty("class", "bigfont")
		self.weather_label.setProperty("class", "smallfont")
		self.weather_icon.setProperty("class", "smallfont")
		self.wind_label.setProperty("class", "smallfont")

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
		self.parent.location_detailed_widget.setup(self.weather, self)
		self.parent.location_detailed_widget.show()


if __name__ == "__main__":
	weatherapp = WeatherApp()
	weatherapp.exec()
