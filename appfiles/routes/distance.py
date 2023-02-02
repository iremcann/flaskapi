from flask import Flask, render_template, request, Blueprint
import requests, json
from numpy import sin, cos, arccos, pi, round
import math

distance_page = Blueprint('distance_page', __name__,
                          template_folder='templates')

@distance_page.route('/distance', methods=['POST'])
def process():
    city1 = request.form["city1"]
    city2 = request.form["city2"]
    def yandex_geocode(city):
        url = "https://geocode-maps.yandex.ru/1.x"
        params = {
            "apikey": "93f0069b-eb46-4a12-a9de-e483a7977999",
            "geocode": city,
            "format": "json"
        }
        response = requests.get(url, params=params)
        if response.status_code != 200:
            return None
        else:
            data = response.json()
        if "GeoObjectCollection" not in data["response"]:
            return None
        elif "featureMember" not in data["response"]["GeoObjectCollection"]:
            return None
        elif data["response"]["GeoObjectCollection"]["metaDataProperty"]        ["GeocoderResponseMetaData"]["found"]==0:
            return None
        else:
            coordinates = data["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["Point"]["pos"]
            longitude, latitude = map(float, coordinates.split())
        return (latitude, longitude)

    def calculate_distance(location1, location2):
        lat1, lon1 = location1
        lat2, lon2 = location2
        radius = 6371  # radius of earth in km

        dlat = math.radians(lat2-lat1)
        dlon = math.radians(lon2-lon1)
        a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        distance = radius * c
        distance = round(distance)
        return distance
    
    location1 = yandex_geocode(city1)
    location2 = yandex_geocode(city2)

    if location1 is None or location2 is None:
        return render_template("error.html", message="HATALI ŞEHİR İSMİ GİRİLDİ", city1=city1, city2=city2)
    else:
      distance = calculate_distance(location1, location2)
      return render_template("response.html", city1=city1, city2=city2, distance=distance)