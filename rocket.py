import requests
import json
from bs4 import BeautifulSoup

def html_page():
    url = 'https://www.mebelshara.ru/contacts'
    try:
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        newlist = soup.findAll('div', {'class' : 'city-item'})
        results = selection_city(newlist)
        json_file(results)
    except(requests.RequestException, ValueError):
        print('Server error')

def selection_city(list):
    try:
        list_atributes = []
        for item in list:
            city = item.find('h4', {'class' : 'js-city-name'}).text
            div = item.find_all('div', class_='shop-list-item')
            for one in div:
                atributes = one.attrs
                atributes['data-shop-address'] = city+', '+atributes['data-shop-address']
                list_atributes.append(atributes)
        return list_atributes
    except(ValueError):
        print('something go wrong')

def json_file(list):
    try:
        to_json = []
        for item in list:
            to_json.append({'address' : item['data-shop-address'], 'latlon' :
                [item['data-shop-latitude'], item['data-shop-longitude']], 'name' :
                item['data-shop-name'], 'phones' : [item['data-shop-phone']], 'working_hours' :
                [item['data-shop-mode2'],item['data-shop-mode1']]})
        with open("data_file.json", "w") as write_file:
            json.dump(to_json, write_file, ensure_ascii=False, indent="\t")
    except(ValueError):
        print('something go wrong')

html_page()