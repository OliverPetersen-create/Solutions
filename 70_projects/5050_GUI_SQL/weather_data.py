from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, Integer
import httpx

Base = declarative_base()
KEY = "2a3891ce1248786a1398a888debb0368"

def get_weather(city, key=KEY):
	url = "https://api.openweathermap.org/data/2.5/weather?q=" + city + "&units=metric&APPID=" + key
	response = httpx.get(url)
	weather = response.json()

	if weather["cod"] != 200:
		raise CityNotFoundException("City not found")
	return {
		"city": weather["name"],
		"weather": weather["weather"][0]["main"],
		"weather_detailed": weather["weather"][0]["description"],
		"temp": float(weather["main"]["temp"]),
		"temp_feels_like": float(weather["main"]["feels_like"]),
		"humidity": float(weather["main"]["humidity"]),
		"wind_speed": float(weather["wind"]["speed"]),
		"wind_deg": float(weather["wind"]["deg"]),
		"country": [weather["sys"]["country"]]
	}

class CityNotFoundException(Exception):

	def __init__(self, msg):
		super(CityNotFoundException, self).__init__(msg)

class City(Base):
	__tablename__ = "city"
	id = Column(Integer, primary_key=True)
	city = Column(String, unique=True)

	def __repr__(self):
		return f"City({self.id=}   {self.city=})"

class Weather:
	CLOUDS = "☁"
	CLEAR = "☀️"
	RAIN = "☔"
	PARTIALLY_CLOUDY = "⛅"

	weather = {}

	def __init__(self, city):
		weather = get_weather(city, KEY)
		self.city = weather["city"]
		self.weather = weather["weather"]
		self.weather_detailed = weather["weather_detailed"]
		self.temp = weather["temp"]
		self.temp_feels_like = weather["temp_feels_like"]
		self.humidity = weather["humidity"]
		self.wind_speed = weather["wind_speed"]
		self.wind_deg = weather["wind_deg"]
		self.country = weather["country"]
		Weather.weather[city] = self

	def __repr__(self):
		return f"{self.city=} {self.weather=} {self.weather_detailed=} {self.temp=} {self.temp_feels_like=} {self.humidity=} {self.wind_speed=} {self.wind_deg=} {self.country=}"

	@staticmethod
	def get_weather(city) -> Weather:
		return Weather.weather[city]

	@staticmethod
	def get_icon_from_weather(weather: str, weather_detail: str):
		if weather_detail == "few clouds" or weather_detail == "broken clouds" or weather_detail == "scattered clouds":
			return Weather.PARTIALLY_CLOUDY
		return Weather.__dict__[weather.upper()]


if __name__ == "__main__":
	try:
		weather1 = Weather("høje taastrup")
		print(weather1)
	except CityNotFoundException:
		print("Fejl")
