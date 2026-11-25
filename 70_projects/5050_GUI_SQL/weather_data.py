from PyQt6.QtGui import QPixmap
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, Integer
import time
import datetime
import httpx

Base = declarative_base()
KEY = "2a3891ce1248786a1398a888debb0368"


def get_weather(location, key=KEY):
	url = "https://api.openweathermap.org/data/2.5/weather?q=" + location + "&units=metric&APPID=" + key
	response = httpx.get(url)
	weather = response.json()
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
		"country": weather["sys"]["country"],
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
		self.local_location = location
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
		self.country = None
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
		self.country = weather["country"]
		self.sunrise = weather["sunrise"]
		self.sunset = weather["sunset"]
		self.timezone = weather["timezone"]
		if weather.get("rain", None) is not None:
			self.rain = weather["rain"]["1h"]
		if weather.get("snow", None) is not None:
			self.snow = weather["snow"]["1h"]

	def updateLabels(self):
		if len(self.label_ref) < 1:
			return
		for label, options in self.label_ref.items():
			type_ = options.get("type", None)
			value = None
			if type_ != "function":
				value = self.__dict__[options["target"]]
			decimal_ = options.get("decimal", None)
			round_ = options.get("round", None)
			if decimal_ is not None:
				value = f"{value:.{decimal_}f}"
			if round_ is not None:
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

	def getSunriseTime(self):
		return (datetime.datetime.fromtimestamp(self.sunrise, datetime.UTC) + datetime.timedelta(seconds=self.timezone)).strftime("%H:%M"), datetime.datetime.fromtimestamp(self.sunrise).strftime("%H:%M")

	def getSunsetTime(self):
		return (datetime.datetime.fromtimestamp(self.sunset, datetime.UTC) + datetime.timedelta(seconds=self.timezone)).strftime("%H:%M"), datetime.datetime.fromtimestamp(self.sunset).strftime("%H:%M")

	def __repr__(self):
		return (f"{self.location=} {self.weather=} {self.weather_detailed=} {self.weather_icon=}"
		        f"{self.temp=} {self.temp_feels_like=} {self.temp_min=} "
		        f"{self.temp_max=} {self.humidity=} {self.wind_speed=} "
		        f"{self.wind_deg=} {self.country=} {self.sunrise=} "
		        f"{self.sunset=} {self.timezone=} {self.rain=} {self.snow=}")

	@staticmethod
	def startUpdating():
		while True:
			for upd in Weather.weather.values():
				if upd.stop_updating:
					continue
				upd.updateWeather(upd.local_location)
				upd.updateLabels()
			time.sleep(5)

	@staticmethod
	def get_weather(location) -> Weather:
		return Weather.weather[location]


if __name__ == "__main__":
	try:
		weather1 = Weather("irkutsk")

	except LocationNotFoundException:
		print("Fejl")
