import requests
import json

openmeteo = "https://api.open-meteo.com/v1/forecast?latitude=46.2389&daily=temperature_2m_mean,sunrise,sunset&longitude=14.3556&current=temperature_2m,rain&timezone=Europe%2FBerlin&forecast_days=7"
nominatim = "https://nominatim.openstreetmap.org/search?city=Kranj&country=Slovenia"
params = {"city": "Kranj",
          "country": "Slovenia"}
headers = {
    "User-Agent": "School_API_Practice/1.0 (joj.sitecen@gmail.com)"
}

call = requests.get(nominatim)
callJSON = call.json()

if False:
    for key in callJSON.keys():
        print(f"{key}: {callJSON[key]}")
        
if False:
    print(f"trenutna temperatura: {callJSON['current']['temperature_2m']}")
    print(f"napovedana temperatura: {callJSON['daily']['temperature_2m_mean']}")

    temperature = callJSON['daily']['temperature_2m_mean']
    maxtemp = max(temperature)
    maxtempDatum = callJSON['daily']['time'][temperature.index(maxtemp)]
    print((maxtemp, maxtempDatum))


