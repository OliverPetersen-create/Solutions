from dateutil.tz import UTC
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, Integer
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
		self.rain = weather["rain"]
		self.snow = weather["snow"]
		Weather.weather[location] = self

	def getSunriseTime(self):
		return datetime.datetime.fromtimestamp(self.sunrise, datetime.UTC) + datetime.timedelta(seconds=self.timezone), datetime.datetime.fromtimestamp(self.sunrise)

	def getSunsetTime(self):
		return datetime.datetime.fromtimestamp(self.sunset, datetime.UTC) + datetime.timedelta(seconds=self.timezone), datetime.datetime.fromtimestamp(self.sunset)

	def __repr__(self):
		return (f"{self.location=} {self.weather=} {self.weather_detailed=} {self.weather_icon=}"
		        f"{self.temp=} {self.temp_feels_like=} {self.temp_min=} "
		        f"{self.temp_max=} {self.humidity=} {self.wind_speed=} "
		        f"{self.wind_deg=} {self.country=} {self.sunrise=} "
		        f"{self.sunset=} {self.timezone=} {self.rain=} {self.snow=}")

	@staticmethod
	def get_weather(location) -> Weather:
		return Weather.weather[location]


if __name__ == "__main__":
	try:
		weather1 = Weather("irkutsk")
		print(weather1.rain)
		print(weather1.snow)

	except LocationNotFoundException:
		print("Fejl")
