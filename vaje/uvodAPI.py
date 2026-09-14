import requests
import json

openmeteo = "https://api.open-meteo.com/v1/forecast?latitude=46.2389&daily=temperature_2m_mean&longitude=14.3556&daily=sunrise,sunset&current=temperature_2m,rain&timezone=Europe%2FBerlin&forecast_days=7"


call = requests.get(openmeteo)
callJSON = call.json()

if False:
    for key in callJSON.keys():
        print(f"{key}: {callJSON[key]}")
        
print(f"trenutna temperatura: {callJSON['current']['temperature_2m']}")
print(f"napovedana temperatura: {callJSON['daily']['temperature_2m_mean']}")

temperature = callJSON['daily']['temperature_2m_mean']
maxtemp = max(temperature)
maxtempDatum = callJSON['daily']['time'][temperature.index(maxtemp)]
print((maxtemp, maxtempDatum))


