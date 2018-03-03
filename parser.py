import bs4
import requests
import re


url = 'http://ligakulinarov.ru/recepty?sort=new&page='
ending = "#recipeboard"
last = 259



'''with open('recipes.csv', 'wt', encoding="utf-8") as f:
    f.write('"title";"type";"calories";"difficulties";"method";"link"'+'\n')'''


for i in range(1, last+1):
    new_url = url + str(i) + ending
    r = requests.get(new_url)
    text = r.text
    soup = bs4.BeautifulSoup(text, 'html.parser')
    lst = []
    Lis = soup.findAll("div", {"class": "author-wrap"})
    soup = bs4.BeautifulSoup(str(Lis), "html.parser")
    for a in soup.find_all('a', href=True):
        if a["href"].startswith("/recepty"):
            lst.append(a["href"])
    for tmp_url in lst:
        r =requests.get('http://ligakulinarov.ru'+tmp_url)
        soup = bs4.BeautifulSoup(r.text, "html.parser")
        soup.find('h1')
        #soup.find ('value oneline')

#'/recepty/drojjevye-pirogi/krupy-muka/pletenka-s-makom-i-orehami-104528'
