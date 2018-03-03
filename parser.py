import bs4
import requests

url = 'http://ligakulinarov.ru/recepty?sort=new&page='
ending = "#recipeboard"
last = 259

for i in range(last):
    new_url = url + str(i) + ending
    r = requests.get(new_url)
    with open('test.html', 'w') as output_file:
    output_file.write(r.text.encode('cp1251'))
