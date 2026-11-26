from PyQt6.QtCore import Qt
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6 import uic
from weather_data import Weather, Location, LocationNotFoundException
import threading
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
		thread = threading.Thread(target=Weather.startUpdating, daemon=True)
		thread.start()

		self.main_win = MainWindow()

		for location_from_database in weather_database.get_all_records():
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
		trimmed = self.text_ed.toPlainText().strip().lower()
		if len(trimmed) < 1:
			return
		if (weather_database.get_record(trimmed)) is not None:
			self.failed_label.setText("Lokation allerede tilføjet")
			self.failed_label.show()
			return
		try:
			weather = Weather(trimmed)
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

	def __init__(self):
		super(LocationDetailedFrame, self).__init__()
		self.frame: LocationFrame = None
		self.setMaximumWidth(800)
		self.setProperty("class", "content_frame")
		self.setStyleSheet(location_detailed_frame_stylesheet)
		self.setWidgetResizable(True)
		self.inner = QWidget(self)
		self.inner.setProperty("class", "transparent")
		self.lo = QGridLayout()
		self.inner.setLayout(self.lo)
		self.lo.setContentsMargins(20, 0, 20, 20)
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

		self.rain = Label("---")
		self.rain.setProperty("class", "header_text")
		self.rain.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
		self.rslo.addWidget(self.rain)

		self.snow = Label("---")
		self.snow.setProperty("class", "header_text")
		self.snow.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
		self.rslo.addWidget(self.snow)

		self.rain.hide()
		self.snow.hide()

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
		self.tlo = QVBoxLayout()
		self.tlo.setContentsMargins(0, 30, 0, 0)
		self.tlo.setSpacing(10)
		self.temp_widget.setLayout(self.tlo)

		self.htlo1 = QHBoxLayout()
		self.htlo2 = QHBoxLayout()
		self.htlo3 = QHBoxLayout()
		delLOSpace(self.htlo1)
		delLOSpace(self.htlo2)
		self.htlo2.setSpacing(20)
		delLOSpace(self.htlo3)
		self.htlo3.setSpacing(20)
		self.temp_widget1 = QWidget()
		self.temp_widget1.setLayout(self.htlo1)
		self.temp_widget2 = QWidget()
		self.temp_widget2.setLayout(self.htlo2)
		self.temp_widget3 = QWidget()
		self.temp_widget3.setLayout(self.htlo3)
		self.tlo.addWidget(self.temp_widget1)
		self.tlo.addWidget(self.temp_widget2)
		self.tlo.addWidget(self.temp_widget3)

		self.tempf = Label("---")
		self.tempf.setProperty("class", "small_text1")
		self.tempf.setContentsMargins(0, 0, 10, 0)
		self.htlo1.addWidget(self.tempf)
		self.htlo1.setAlignment(self.tempf, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)

		self.temp_freezing = QLabel()
		pixmap = QPixmap(f"images/13n.png")
		self.temp_freezing.setPixmap(pixmap)
		self.htlo1.addWidget(self.temp_freezing)
		self.htlo1.setAlignment(self.temp_freezing, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

		self.min_temp = Label("Min")
		self.min_temp.setProperty("class", "small_text1")
		self.min_temp.setContentsMargins(40, 0, 0, 0)
		self.htlo2.addWidget(self.min_temp)
		self.htlo2.setAlignment(self.min_temp, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)

		self.max_temp = Label("Max")
		self.max_temp.setProperty("class", "small_text1")
		self.max_temp.setContentsMargins(0, 0, 40, 0)
		self.htlo2.addWidget(self.max_temp)
		self.htlo2.setAlignment(self.max_temp, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)

		self.min_temp_num = Label("---")
		self.min_temp_num.setProperty("class", "small_text2")
		self.min_temp_num.setContentsMargins(40, 0, 0, 0)
		self.htlo3.addWidget(self.min_temp_num)
		self.htlo3.setAlignment(self.min_temp_num, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)

		self.max_temp_num = Label("---")
		self.max_temp_num.setProperty("class", "small_text2")
		self.max_temp_num.setContentsMargins(0, 0, 40, 0)
		self.htlo3.addWidget(self.max_temp_num)
		self.htlo3.setAlignment(self.max_temp_num, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)

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
		weather_database.delete_record(self.frame.weather.location.lower())
		self.frame.weather.stop_updating = True
		self.frame.hide()

	def back(self):
		self.hide()
		self.frame.parent.scroll_area.show()

		self.frame.weather.label_ref = {
			self.frame.location_label: {"target": "location"},
			self.frame.temp_label: {"target": "temp", "format": "%value% °C", "round": True},
			self.frame.weather_label: {"target": "weather"},
			self.frame.weather_icon: {"target": "weather_icon", "type": "icon"},
			self.frame.wind_label: {"target": "wind_speed", "format": "%value% m/s ༄", "decimal": 1}
		}

	def setup(self, weather: Weather, frame: LocationFrame):
		self.frame = frame
		self.rain.hide()
		self.snow.hide()
		self.temp_freezing.hide()
		self.title.setText(weather.location)
		self.temp.setText(f"{weather.temp} °C")
		self.tempf.setText(f"Føles som {weather.temp_feels_like} °C")
		self.min_temp_num.setText(f"{weather.temp_min} °C")
		self.max_temp_num.setText(f"{weather.temp_max} °C")
		self.weather.setText(weather.weather)
		self.weather_detailed.setText(weather.weather_detailed)
		pixmap = QPixmap(f"images/{weather.weather_icon}.png")
		self.weather_icon.setPixmap(pixmap)
		self.humidity.setText(f"{round(weather.humidity)}% luftfugtighed")
		self.wind.setText(f"{weather.wind_speed} meter/s vind ༄")
		wind_direction = weather.getWindDirection()
		self.wind_deg.setText(f"{wind_direction[0]} {wind_direction[1]} ({wind_direction[2]}°)")
		sunrise = weather.getSunriseTime()
		sunset = weather.getSunsetTime()
		self.sunrise_label.setText(f"Solopgang\n{sunrise[0]}\n({sunrise[1]} lokal tid)")
		self.sunset_label.setText(f"Solnedgang\n{sunset[0]}\n({sunset[1]} lokal tid)")
		if weather.temp_feels_like <= 1:
			self.temp_freezing.show()
		if weather.rain is not None:
			self.rain.show()
			self.rain.setText(f"{weather.rain}mm regn i timen")
		if weather.snow is not None:
			self.snow.show()
			self.snow.setText(f"{weather.snow}mm sne i timen")
		weather.label_ref = {
			self.title: {"target": "location"},
			self.temp: {"target": "temp", "format": "%value% °C"},
			self.tempf: {"target": "temp_feels_like", "format": "Føles som %value% °C"},
			self.min_temp_num: {"target": "temp_min", "format": "%value% °C"},
			self.max_temp_num: {"target": "temp_max", "format": "%value% °C"},
			self.weather: {"target": "weather"},
			self.weather_detailed: {"target": "weather_detailed"},
			self.weather_icon: {"target": "weather_icon", "type": "icon"},
			self.humidity: {"target": "humidity", "format": "%value%% luftfugtighed", "round": True},
			self.wind: {"target": "wind_speed", "format": "%value% meter/s vind ༄"},
			self.wind_deg: {"target": weather.getWindDirection, "type": "function", "format": "%value-1% %value-2% (%value-3%°)"},
			self.sunrise_label: {"target": weather.getSunriseTime, "type": "function", "format": "Solopgang\n%value-1%\n(%value-2% lokal tid)"},
			self.sunset_label: {"target": weather.getSunsetTime, "type": "function", "format": "Solnedgang\n%value-1%\n(%value-2% lokal tid)"},
			self.rain: {"target": "rain", "format": "%value%mm regn i timen", "dynamicVisibility": True},
			self.snow: {"target": "snow", "format": "%value%mm sne i timen", "dynamicVisibility": True}
		}


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
		self.layout = QVBoxLayout()
		delLOSpace(self.layout)
		self.layout.setContentsMargins(25, 20, 25, 0)
		self.layout.setSpacing(0)

		self.widget_1 = QWidget()
		self.widget_2 = QWidget()
		self.lo_1 = QHBoxLayout()
		self.lo_2 = QHBoxLayout()
		self.widget_1.setLayout(self.lo_1)
		self.widget_2.setLayout(self.lo_2)
		delLOSpace(self.lo_1)
		delLOSpace(self.lo_2)

		self.location_label = Label(weather.location)
		self.location_label.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
		self.location_label.setContentsMargins(0, 0, 15, 0)
		self.temp_label = Label(f"{round(weather.temp)} °C")
		self.temp_label.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
		self.weather_label = Label(f"{weather.weather}")
		self.weather_label.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
		self.weather_label.setContentsMargins(0, 0, 15, 0)
		self.weather_icon = QLabel()
		pixmap = QPixmap(f"images/{weather.weather_icon}.png")
		self.weather_icon.setPixmap(pixmap)
		self.weather_icon.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
		self.wind_label = Label(f"{weather.wind_speed:.1f} m/s ༄")
		self.wind_label.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)

		self.location_label.setProperty("class", "bigfont")
		self.temp_label.setProperty("class", "bigfont")
		self.weather_label.setProperty("class", "smallfont")
		self.weather_icon.setProperty("class", "smallfont")
		self.wind_label.setProperty("class", "smallfont")

		self.lo_1.addWidget(self.location_label)
		self.lo_1.addWidget(self.temp_label)
		self.lo_2.addWidget(self.weather_label)
		self.lo_2.addWidget(self.weather_icon)
		self.lo_2.addStretch()
		self.lo_2.addWidget(self.wind_label)

		self.lo_1.setAlignment(self.location_label, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
		self.lo_1.setAlignment(self.temp_label, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)
		self.lo_2.setAlignment(self.weather_label, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
		self.lo_2.setAlignment(self.weather_icon, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
		self.lo_2.setAlignment(self.wind_label, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

		self.layout.addWidget(self.widget_1)
		self.layout.addWidget(self.widget_2)
		self.layout.addStretch()

		weather.label_ref = {
			self.location_label: {"target": "location"},
			self.temp_label: {"target": "temp", "format": "%value% °C", "round": True},
			self.weather_label: {"target": "weather"},
			self.weather_icon: {"target": "weather_icon", "type": "icon"},
			self.wind_label: {"target": "wind_speed", "format": "%value% m/s ༄", "decimal": 1}
		}

		self.setLayout(self.layout)

	def mousePressEvent(self, e: QMouseEvent):
		self.parent.scroll_area.hide()
		self.parent.location_detailed_widget.setup(self.weather, self)
		self.parent.location_detailed_widget.show()


if __name__ == "__main__":
	weatherapp = WeatherApp()
	weatherapp.exec()
