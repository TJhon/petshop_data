from bs4 import BeautifulSoup
import requests

html = requests.get("https://mascotaveloz.pe/bravery-chicken-adult-cat/").text

a = BeautifulSoup(html, 'html.parser')

b =a.find('div', class_='summary entry-summary')
print(b)