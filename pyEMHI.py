import requests, xmltodict
from bs4 import BeautifulSoup

def GetHistoricWeatherData(Day, Month, Year, Hour):
    Month = str(Month)
    Day = str(Day)
    Year = str(Year)
    Hour = str(Hour)
    Result = dict()
    url = "http://www.ilmateenistus.ee/ilm/ilmavaatlused/vaatlusandmed/?lang=et&filter%5BmaxDate%5D=09.11.2014&filter%5BminDate%5D=30.01.2004&filter%5Bdate%5D=" + Day + "." + Month + "." + Year + "&filter%5Bhour%5D=" + str(Hour) + "&filter%5BmapLayer%5D=air-temp"
    r = requests.get(url)
    soup = BeautifulSoup(r.text)
    for div in soup.find_all("div"):
        Classes = div.attrs.get("class", "NoValue")
        if Classes != "NoValue" and len(Classes) > 1:
            if Classes[0] == "station-container":
                for span in div.find_all("span"):
                    datalayer_div = div.find("div")
                    Classes2 = datalayer_div.attrs.get("class", "NoValue")
                    if Classes2 != "NoValue" and len(Classes2) > 1 and Classes2[1] == "layer-data-air-temp" and len(span.text.encode("ascii", "ignore").replace(",", ".").strip().replace(" ", "")) > 1:
                        Result[Classes[1]] = float(span.text.encode("ascii", "ignore").replace(",", ".").strip().replace(" ", ""))
    return Result

def GetCurrentWeatherData():
    r = requests.get("http://www.ilmateenistus.ee/ilma_andmed/xml/observations.php")
    WData = xmltodict.parse(r.text)
    WeatherData = dict()
    WeatherData["Time"] = WData["observations"]["@timestamp"]
    WeatherData["Stations"] = []
    for station in WData["observations"]["station"]:
        Station = dict()
        Station["name"] = station["name"]
        Station["wmocode"] = station["wmocode"]
        Station["phenomen"] = station["phenomenon"]
        Station["visibility"] = station["visibility"]
        Station["precipitations"] = station["precipitations"]
        Station["airpressure"] = station["airpressure"]
        Station["humidity"] = station["relativehumidity"]
        Station["airtemp"] = station["airtemperature"]
        Station["winddirection"] = station["winddirection"]
        Station["windspeed"] = station["windspeed"]
        Station["windspeedmax"] = station["windspeedmax"]

        WeatherData["Stations"].append(Station)
    return WeatherDataw

print(GetHistoricWeatherData(28, 5, 2018, 7))
