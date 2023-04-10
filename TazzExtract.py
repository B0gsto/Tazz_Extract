import requests
import re
from lxml import etree
import os


def get_tazz_restaurants_page(link):
    tazz_response = requests.get(link)
    with open("tazz.html", 'wb') as html_file:
        html_file.write(tazz_response.content)


class ExtractDataFromHtmlPage:

    def __init__(self):

        self.html_file = os.path.realpath("tazz.html")
        self.parser = etree.HTMLParser()
        self.cluj_restaurants = []

    def extract_tazz_restaurants(self):
        tree = etree.parse(self.html_file, self.parser)
        root = tree.getroot()
        real_path = root.find('.//div[@class = "partnersListLayout"]')
        cards = real_path.xpath('.//div[contains(@class, "store-card ") or contains(@class, "store-card store-card-closed ")]')
        # verify if cards can be found
        verify_if_none=root.xpath('.//div[@class="store-card full filters-no-results"]')
        if len(verify_if_none) != 0:
            with open("tazz_restaurants.txt", 'w', encoding="UTF-8") as restaurants_file:
                restaurants_file.write("No restaurants found:::")
            return
        for card in cards:
            # Cost livrare
            a = card.xpath(".//div[@class='store-delivery']/text()")[1]
            pattern = r'D.+i|Livrare gratuită'
            match = re.search(pattern, a)
            delivery_fee = match.group()

            # Nume restaurant
            name_element = card.find('.//h3[@class="store-name"]')
            name = name_element.text

            # Stele restaurant
            try:
                b = card.xpath(".//div[@class='store-rating']/text()")[1]
                pattern = r'\d\.\d'
                match = re.search(pattern, b)
                stars = match.group()
            except IndexError:
                stars = '-'
            self.cluj_restaurants.append([name, delivery_fee, stars])
        with open("tazz_restaurants.txt", 'w', encoding="UTF-8") as restaurants_file:
            for restaurant in self.cluj_restaurants:
                restaurants_file.write(restaurant[0] + ":" + restaurant[1]+ ":" + restaurant[2] + ":" + "\n")

def get_link_for_city(city):
    with open("tazz_cities.txt", 'r', encoding="UTF-8") as cities_file:
        for line in cities_file:
            line = line.strip()
            if city in line:
                line = line.split(";")
                return line[1]



def extract_and_save_tazz_restaurants(option):
    print(option)
    a = get_link_for_city(option)
    print(a)
    get_tazz_restaurants_page(a)
    extractDataObj = ExtractDataFromHtmlPage()
    extractDataObj.extract_tazz_restaurants()

