from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String
import httpx

Base = declarative_base()
KEY = "2a3891ce1248786a1398a888debb0368"

def get_weather(city, key=KEY):
	url = "http://api.openweathermap.org/data/2.5/weather?q=" + city + "&units=metric&APPID=" + key
	response = httpx.get(url)
	weather = response.json()

	if weather["cod"] != 200:
		return "Ukendt lokation"
	return {
		"City": weather["name"],
		"Weather": weather["weather"][0]["main"],
		"WeatherDetailed": weather["weather"][0]["description"],
		"Temp": float(weather["main"]["temp"]),
		"TempFeelsLike": float(weather["main"]["feels_like"]),
		"Humidity": float(weather["main"]["humidity"]),
		"WindSpeed": float(weather["wind"]["speed"]),
		"WindDeg": float(weather["wind"]["deg"]),
		"Country": [weather["sys"]["country"]]
	}

class WeatherIcon:
	CLOUDS = "☁"
	CLEAR = "☀️"
	RAIN = "☔"
	PARTIALLY_CLOUDY = "⛅"

	@staticmethod
	def get_icon_from_weather(weather: str, weather_detail: str):
		if weather_detail == "few clouds" or weather_detail == "broken clouds" or weather_detail == "scattered clouds":
			return WeatherIcon.PARTIALLY_CLOUDY
		return WeatherIcon.__dict__[weather.upper()]

class City(Base):
	__tablename__ = "city"
	id = Column(String, primary_key=True)

	def __init__(self, city, *pargs):
		super().__init__(*pargs)
		self.weather = Weather(city)

	def __repr__(self):
		return f"City({self.id=}   Weather({self.weather=}))"

	def valid(self):
		return self.id == "$deleted"

class Weather:

	def __init__(self, city):
		weather = get_weather(city, KEY)
		self.city = weather["city"]
		self.weather = weather["weather"]
		self.weatherDetailed = weather["weatherDetailed"]
		self.temp = weather["temp"]
		self.temp_feels_like = weather["tempfeelslike"]
		self.humidity = weather["humidity"]
		self.wind_speed = weather["windspeed"]
		self.wind_deg = weather["winddeg"]
		self.country = weather["country"]


if __name__ == "__main__":
	weather1 = get_weather("høje taastrup", KEY)
	print(weather1)
	print(WeatherIcon.get_icon_from_weather(weather1["Weather"], weather1["WeatherDetailed"]))