#install requests using pip first
#data refreshes every 10 minutes
import requests

t = u"\u00b0"

city_id = "5122534"
url = "http://api.openweathermap.org/data/2.5/weather?id="+ city_id + "&units=imperial&APPID=c3e072c5029f60ac53dac3d1c7d9b06f"
json_data = requests.get(url).json()

temp_val = str(json_data["main"]["temp"])
temp_val = temp_val[:len(temp_val) - 3]

description = str(json_data["weather"][0]["description"])
description = description.capitalize()

format_add = description + "\n" + "Temperature: " + temp_val + " " + t + "F"
print(format_add)

