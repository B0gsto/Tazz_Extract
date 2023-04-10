import requests
from lxml import etree
import os


def get_tazz_page():
    tazz_response = requests.get("https://tazz.ro")
    with open("tazz_main.html", 'wb') as html_file:
        html_file.write(tazz_response.content)


class ExtractCitiesFromHtmlPage:
    def __init__(self):
        self.html_file = os.path.realpath("tazz_main.html")
        self.parser = etree.HTMLParser()
        self.cluj_cities = []

    def extract_tazz_cities(self):
        tree = etree.parse(self.html_file, self.parser)
        root = tree.getroot()
        cities = root.xpath('.//a[@class="city-card address-check"]')
        for city in cities:
            city_name = city.xpath(".//h3/text()")[0]
            link = city.get("href")
            link = link.replace("oras", "restaurante")
            self.cluj_cities.append([city_name, link])
        with open("tazz_cities.txt", 'w', encoding="UTF-8") as cities_file:
            for city in self.cluj_cities:
                cities_file.write(city[0] + ";" + city[1] + ";" + "\n")


def extract_and_save_tazz_cities():
    get_tazz_page()
    extractDataObj = ExtractCitiesFromHtmlPage()
    extractDataObj.extract_tazz_cities()
