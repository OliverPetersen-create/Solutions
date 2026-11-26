from PyQt6.QtGui import QPixmap
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, Integer
import time
import datetime
import httpx
import random

Base = declarative_base()
KEY = "2a3891ce1248786a1398a888debb0368"


def get_weather(location, key=KEY):
	url = "https://api.openweathermap.org/data/2.5/weather?q=" + location + "&units=metric&APPID=" + key
	response = httpx.get(url)
	weather = response.json()

	if location == "test":
		return {
			"location": "test",
			"weather": "Snow" if random.randint(1, 2) > 1 else "Thunderstorm",
			"weather_detailed": "Lots of snow" if random.randint(1, 2) > 1 else "Thunderstorm with clouds",
			"weather_icon": "09n" if random.randint(1, 2) > 1 else "13n",
			"temp": float(random.randint(-5, 30)),
			"temp_feels_like": float(random.randint(-5, 30)),
			"temp_min": float(random.randint(-5, 30)),
			"temp_max": float(random.randint(-5, 30)),
			"humidity": float(random.randint(-5, 30)),
			"wind_speed": float(random.randint(-5, 30)),
			"wind_deg": float(random.randint(-5, 30)),
			"sunrise": 1795680061 if random.randint(1, 2) > 1 else 1795710954,
			"sunset": 1795702593 if random.randint(1, 2) > 1 else 1795737599,
			"timezone": (random.randint(1, 5) * 3600),
			"rain": None if random.randint(-10, 10) < 5 else {"1h": random.randint(1, 5)},
			"snow": None if random.randint(-10, 10) < 5 else {"1h": random.randint(1, 5)}
		}

	if location.lower() == "santa's workshop" or location.lower() == "santas workshop":
		return {
			"location": "Santa's Workshop",
			"weather": "Snow",
			"weather_detailed": "light snow",
			"weather_icon": "13d",
			"temp": float(22.36),
			"temp_feels_like": float(23.19),
			"temp_min": float(21.86),
			"temp_max": float(23.86),
			"humidity": float(89),
			"wind_speed": float(0),
			"wind_deg": float(0),
			"sunrise": 1795719666,
			"sunset": 1795738370,
			"timezone": -32400,
			"rain": None,
			"snow": {"1h": 0.12}
		}

	if weather["cod"] != 200:
		raise LocationNotFoundException("Location not found")
	return {
		"location": weather["name"],
		"weather": weather["weather"][0]["main"],
		"weather_detailed": weather["weather"][0]["description"],
		"weather_icon": weather["weather"][0]["icon"],
		"temp": float(weather["main"]["temp"]),
		"temp_feels_like": float(weather["main"]["feels_like"]),
		"temp_min": float(weather["main"]["temp_min"]),
		"temp_max": float(weather["main"]["temp_max"]),
		"humidity": float(weather["main"]["humidity"]),
		"wind_speed": float(weather["wind"]["speed"]),
		"wind_deg": float(weather["wind"]["deg"]),
		"sunrise": weather["sys"]["sunrise"],
		"sunset": weather["sys"]["sunset"],
		"timezone": weather["timezone"],
		"rain": weather.get("rain", None),
		"snow": weather.get("snow", None)
	}


class LocationNotFoundException(Exception):

	def __init__(self, msg):
		super(LocationNotFoundException, self).__init__(msg)


class Location(Base):
	__tablename__ = "location"
	id = Column(Integer, primary_key=True)
	location = Column(String, unique=True)

	def __repr__(self):
		return f"Location({self.id=}   {self.location=})"


class Weather:
	weather = {}

	def __init__(self, location):
		self.location = None
		self.weather = None
		self.weather_detailed = None
		self.weather_icon = None
		self.temp = None
		self.temp_feels_like = None
		self.temp_min = None
		self.temp_max = None
		self.humidity = None
		self.wind_speed = None
		self.wind_deg = None
		self.sunrise = None
		self.sunset = None
		self.timezone = None
		self.rain = None
		self.snow = None
		self.stop_updating = False
		self.updateWeather(location)
		self.label_ref = {}
		Weather.weather[location] = self

	def updateWeather(self, location):
		weather = get_weather(location, KEY)
		self.location = weather["location"]
		self.weather = weather["weather"]
		self.weather_detailed = weather["weather_detailed"]
		self.weather_icon = weather["weather_icon"]
		self.temp = weather["temp"]
		self.temp_feels_like = weather["temp_feels_like"]
		self.temp_min = weather["temp_min"]
		self.temp_max = weather["temp_max"]
		self.humidity = weather["humidity"]
		self.wind_speed = weather["wind_speed"]
		self.wind_deg = weather["wind_deg"]
		self.sunrise = weather["sunrise"]
		self.sunset = weather["sunset"]
		self.timezone = weather["timezone"]
		if weather.get("rain", None) is not None:
			self.rain = weather["rain"]["1h"]
		else:
			self.rain = None
		if weather.get("snow", None) is not None:
			self.snow = weather["snow"]["1h"]
		else:
			self.snow = None

	def updateLabels(self):
		if len(self.label_ref) < 1:
			return
		for label, options in self.label_ref.items():
			type_ = options.get("type", None)
			value = None
			if type_ != "function":
				value = self.__dict__[options["target"]]
				dynamic_visibility = options.get("dynamicVisibility", False)
				if value is None and dynamic_visibility:
					label.hide()
				elif value is not None and dynamic_visibility:
					label.show()
			decimal_ = options.get("decimal", None)
			round_ = options.get("round", None)
			if decimal_ is not None and value is not None:
				value = f"{value:.{decimal_}f}"
			if round_ is not None and value is not None:
				value = round(value)
			has_format = options.get("format", None)
			format_ = str(options.get("format", value))
			if type_ == "function":
				values = options["target"]()
				if has_format is not None:
					for i in range(len(values)):
						format_ = format_.replace(f"%value-{i + 1}%", str(values[i]))
				label.setText(format_)
				continue
			elif type_ == "icon":
				pixmap = QPixmap(f"images/{value}.png")
				label.setPixmap(pixmap)
				continue
			if has_format is not None:
				format_ = format_.replace("%value%", str(value))
			label.setText(format_)

	def getWindDirection(self):
		if 0 <= self.wind_deg < 45:
			return "N", "↑", int(self.wind_deg)
		elif 45 <= self.wind_deg < 90:
			return "NØ", "↗", int(self.wind_deg)
		elif 90 <= self.wind_deg < 135:
			return "Ø", "→", int(self.wind_deg)
		elif 135 <= self.wind_deg < 180:
			return "SØ", "↘", int(self.wind_deg)
		elif 180 <= self.wind_deg < 225:
			return "S", "↓", int(self.wind_deg)
		elif 225 <= self.wind_deg < 270:
			return "SV", "↙", int(self.wind_deg)
		elif 270 <= self.wind_deg < 315:
			return "V", "←", int(self.wind_deg)
		elif 315 <= self.wind_deg:
			return "NV", "↖", int(self.wind_deg)
		return "Ukendt", "↔", 0

	def getSunriseTime(self):
		return (datetime.datetime.fromtimestamp(self.sunrise, datetime.UTC) + datetime.timedelta(seconds=self.timezone)).strftime("%H:%M"), datetime.datetime.fromtimestamp(self.sunrise).strftime("%H:%M")

	def getSunsetTime(self):
		return (datetime.datetime.fromtimestamp(self.sunset, datetime.UTC) + datetime.timedelta(seconds=self.timezone)).strftime("%H:%M"), datetime.datetime.fromtimestamp(self.sunset).strftime("%H:%M")

	def __repr__(self):
		return (f"{self.location=} {self.weather=} {self.weather_detailed=} {self.weather_icon=}"
		        f"{self.temp=} {self.temp_feels_like=} {self.temp_min=} "
		        f"{self.temp_max=} {self.humidity=} {self.wind_speed=} "
		        f"{self.wind_deg=} {self.sunrise=}{self.sunset=} "
		        f"{self.timezone=} {self.rain=} {self.snow=}")

	@staticmethod
	def startUpdating():
		while True:
			for upd in Weather.weather.values():
				if upd.stop_updating:
					continue
				upd.updateWeather(upd.location)
				upd.updateLabels()
			time.sleep(60)

	@staticmethod
	def get_weather(location) -> Weather:
		return Weather.weather[location]


if __name__ == "__main__":
	try:
		weather1 = Weather("irkutsk")

	except LocationNotFoundException:
		print("Fejl")
