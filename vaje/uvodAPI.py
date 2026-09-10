import requests
import json

openmeteo = "https://api.open-meteo.com/v1/forecast?latitude=46.2389&longitude=14.3556&daily=sunrise,sunset&current=temperature_2m,rain&timezone=Europe%2FBerlin&forecast_days=1"
nominatim = "https://nominatim.openstreetmap.org/search?city=kranj&format=jsonv2"


call = requests.get(nominatim)
callJSON = call.json()

for key in callJSON.keys():
    print(f"{key}: {callJSON[key]}")
