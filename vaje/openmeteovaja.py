import requests

def trenutna_temp2(lat, lon):
    global base_url
    params = {"latitude": lat,
              "longitude": lon,
              "current": "temperature_2m",
              "timezone": "auto",
              "forecast_days": 1
              }
    call = requests.get(base_url, params=params)
    callurl = call.url
    calljson = call.json()
    print(callurl)
    
def getForecast(url, lat, lon, days):
    params = {
        "latitude":lat,
        "longitude":lon,
        "forecast_days":days,
        "daily":"temperature_2m_mean,sunrise,sunset,rain_sum"
    }
    call = requests.get(url, params=params)
    print(call.url)
    return call.json()
    
def getCityData(url, name, count):
    params = {
        "name": name,
        "count": count,
        "language":"en",
        "format": "json"
    }
    call = requests.get(url, params=params)
    if count == 1 or len(call.json["results"])==1:
        return call.json()["results"][0], False
    return call.json()["results"], True

def betterInput(text:str, requiredtype:type, default=None):
    inp = None
    safe = False
    while not safe:
        safe = True
        inp = input(text)
        if not default is None and inp=="":
            inp = default
            break
        for char in inp:
            if type(char) != requiredtype:
                safe = False
    return requiredtype(inp)
            

def main():
    forecast_url = "https://api.open-meteo.com/v1/forecast"
    geocoding_url = "https://geocoding-api.open-meteo.com/v1/search"
    city = betterInput("Enter city name: ", str)
    options = betterInput("How many options (press ENTER for default): ", int, 1)
    citydata = getCityData(geocoding_url, city, options)
    if citydata[1]:
        citydata = citydata[0]
        print("MULTIPLE POSSIBLE RESULTS FOUND!")
        for item in citydata:
            print(f"{citydata.index(item)+1}: {item["name"]}, {item["country"]} (pop: {item["population"]}, timezone: {item["timezone"]})")
        selection = betterInput("Select the city you wanted (press ENTER for default): ", int, 1)
        citydata = citydata[selection]
    else:
        citydata = citydata[0]
    forecastDays = betterInput("For how many days should the forecast be?(press ENTER for default): ", int, 7)
    forecast = getForecast(forecast_url, citydata["latitude"], citydata["longitude"], forecastDays)
    print(f"-------- FORECAST FOR {citydata["name"].upper()}, {citydata["country"].upper()} --------")
    for item in forecast:
        print(f"{item}: {forecast[item]}")
    
    
    
if __name__ == "__main__":
    main()