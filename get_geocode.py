import sys
import requests
from bs4 import BeautifulSoup
import json
import codecs
import os

def yandex_geocoder(location):
    url = "https://geocode-maps.yandex.ru/1.x/?format=json&geocode=" + " алматы " + location + "&lang=en-US"
    yandex = requests.get(url = url)
    data = json.loads(yandex.text)
    if (data["response"]["GeoObjectCollection"]["metaDataProperty"]["GeocoderResponseMetaData"]["found"] != "0"):
        print(data["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["Point"]["pos"])
        point = data["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["Point"]["pos"]
    else:
        print("Not found")
        point = "0.0 0.0"
    return point


def save_new_data(name, data, index):
    cwd = os.getcwd()
    cwd = cwd + "/" + name
    if (os.path.isfile(cwd)):
        with codecs.open(name, "a", "utf-8") as myfile:
            myfile.write(str(data))
    else:
        with codecs.open(name, "w", "utf-8") as myfile:
            myfile.write(str(data))

    with open("last_item.txt", "w") as myfile:
        myfile.write(str(index))



def get_geocode(name):
    the_file = open(name, 'r')
    addresses = the_file.readlines()
    cwd = os.getcwd()
    cwd = cwd + "/last_item.txt"
    if (os.path.isfile(cwd)):
        with open("last_item.txt", 'r') as myfile:
            last_item = myfile.read()
            if (last_item == ''):
                last_item = 0
            else:
                last_item = int(last_item)
    else:
        with open("last_item.txt", "w") as myfile:
            last_item = 0
            myfile.write(str(last_item))

    for i in range(last_item, len(addresses)):
        adrs = addresses[i].split("\n")
        print(adrs[0])
        if (adrs[0] != " "):
            location = adrs[0].split(" ; ")
            print(location[1])
            point = yandex_geocoder(location[1])
            geo = point.split(" ")
            latitude = geo[1]
            longitude = geo[0]
            new_line = adrs[0] + " ; " + latitude + " ; " + longitude + " \n"
            save_new_data("with_geo.txt", new_line, i)



def main():
    get_geocode("tocsv.txt")


main()
