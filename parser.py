import requests
import bs4

url = 'http://ligakulinarov.ru/recepty?sort=new&page='
ending = "#recipeboard"
last = 259
lst = []
site = requests.get(url + "1" + ending)
text = site.text
soup = bs4.BeautifulSoup(text, "html.parser")
Lis = soup.findAll("div", {"class": "author-wrap"})
soup = bs4.BeautifulSoup(str(Lis), "html.parser")
for a in soup.find_all('a', href=True):
    if a["href"].startswith("/recepty"):
        lst.append(a["href"])
for tmp_url in lst:
    tmp_url = "http://ligakulinarov.ru" + tmp_url
    r = requests.get(tmp_url)
    soup = bs4.BeautifulSoup(r.text, "html.parser")
    title = soup.find("h1")
    cook_time = bs4.BeautifulSoup(str(bs4.BeautifulSoup(str(soup.find("span",
    {'class':'value oneline'})),'html.parser').contents), 'html.parser').get_text()
    cook_time = cook_time[1:-1]
    print(cook_time)
    difficulty = bs4.BeautifulSoup(str
     (bs4.BeautifulSoup(str(
      bs4.BeautifulSoup(str(soup.find("div",
      {'class':'difficulty row oneline'})),'html.parser').contents
      ),'html.parser').find("span", {'class':'value oneline'})),'html.parser').get_text()
    print(difficulty)
    charachteristics_list = []
    tmp_charachteristics_list = []
    for a in soup.findAll("div", {'class':"item value"}):
        tmp_charachteristics_list.append(a.get_text().split('\n'))
    for charachteristic in tmp_charachteristics_list:
        for item in charachteristic:
            if item != "" or item != '':
                charachteristics_list.append(item)
    print(charachteristics_list)

"""/html/body/div[2]/div[3]/div/div[1]/section/div/ul[3]/li[1]"""
