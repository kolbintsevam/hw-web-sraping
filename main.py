import requests
from bs4 import BeautifulSoup
from fake_headers import Headers
import json

json_link = []

url = 'https://spb.hh.ru/search/vacancy?area=1&area=2&enable_snippets=true&ored_clusters=true&text=python&order_by=publication_time'

heders_fake = fake_headers.Headers(browser='firefox', os='win').generate()

response = requests.get(url, headers=heders_fake)
soup = BeautifulSoup(response.text, 'lxml')

quotes = soup.find_all('div', class_='serp-item')

for i in quotes:
    url_href = i.find('a', class_='serp-item__title').get('href')
    heders_fake2 = fake_headers.Headers(browser='firefox', os='win').generate()
    response2 = requests.get(url_href, headers=heders_fake2)
    soup2 = BeautifulSoup(response2.text, 'lxml')

    money_and_name_companu = soup2.find_all('span', class_='bloko-header-section-2 bloko-header-section-2_lite')
    sity = soup2.find_all('div', class_='vacancy-company-redesigned')
    if 'bloko-link bloko-link_kind-tertiary bloko-link_disable-visited' in str(sity):
        sity2 = sity[0].find('span', {'data-qa': "vacancy-view-raw-address"}).get_text()
        sity_3 = sity2.split()
        sity3 = sity_3[0]
    else:
        sity3 = sity[0].find('p', {'data-qa': "vacancy-view-location"}).get_text()

    quotes2 = soup2.find_all('div', class_='vacancy-branded-user-content')
    if len(quotes2) == 0:
        quotes2 = soup2.find_all('div', class_='g-user-content')

    if 'Django' in str(quotes2[0]) or 'Flask' in str(quotes2[0]):
        json_link.append({'Ссылка': url_href})
        json_link.append({'Вилка ЗП': money_and_name_companu[0].text})
        json_link.append({'Название компании': money_and_name_companu[1].text})
        json_link.append({'Город': sity3})
        print()
        print(url_href)
        print(money_and_name_companu[0].text)
        print(money_and_name_companu[1].text)
        print(sity3)
        print()

with open('data.json', 'w') as f:
    f.write(json.dumps(json_link))