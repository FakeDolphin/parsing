import requests
import json

def html_page():
    try:
        page = requests.get('https://apigate.tui.ru/api/office/cities')
        content = page.json()
        city_id = take_all_cities(content) #Получаем список городов
        url_list = full_url(city_id) #Получаем список юрлов
        companies = json_list(url_list) #Получаем список компаний
        to_json = []
        json_data =[]
        for company in companies:
            for item in company['offices']:
                to_json.append(item)
        for item in to_json:
            list_hoursofoperation = {}
            list_phones = item['phones']
            phone = [phone['phone'] for phone in list_phones]
            list_hoursofoperation = item['hoursOfOperation']
            workdays = list_hoursofoperation['workdays']
            workdays_start = workdays['startStr']
            workdays_end = workdays['endStr']
            work = 'Пн-пт ' + workdays_start + ' до ' + workdays_end
            saturday = list_hoursofoperation['saturday']
            isdayoff = saturday['isDayOff']
            if isdayoff==True:
                work_saturday = 'Сб выходной'
            else:
                weekend_start = saturday['startStr']
                weekend_end = saturday['endStr']
                work_saturday = 'Cб ' + weekend_start + '-' + weekend_end
            sunday = list_hoursofoperation['sunday']
            isdayoffs = sunday['isDayOff']
            if isdayoffs == True:
                work_sunday = 'Вс выходной'
            else:
                weekend_start = sunday['startStr']
                weekend_end = sunday['endStr']
                work_sunday = 'Вс ' + weekend_start + '-' + weekend_end
            json_data.append([{'address' : item['address'],
                               'latlon' : [item['latitude'], item['longitude']],
                               'name' : item['name'], 'phones' : phone,
                               'working_hours' : [work, work_saturday, work_sunday]}])
        with open("data_file.json", "w") as write_file:
            json.dump(json_data, write_file, ensure_ascii=False, indent="\t") #Может выдавать ошибку по кодировке
    except(requests.RequestException, ValueError):
        print('Проверьте кодировку')

def take_all_cities(content):
    city_id = []
    list_cities = content['cities']
    for item in list_cities:
        city_id.append(item['cityId'])
    return city_id

def full_url(city_id):
    list_urls = []
    url_start = 'https://apigate.tui.ru/api/office/list?cityId='
    url_end = '&subwayId=&hoursFrom=&hoursTo=&serviceIds=all&toBeOpenOnHolidays=false'
    for item in city_id:
        item = url_start + str(item) + url_end
        list_urls.append(item)
    return list_urls

def json_list(url_list):
    companies = []
    for url in url_list:
        url = requests.get(url)
        companies.append(url.json())
    return companies

html_page()
