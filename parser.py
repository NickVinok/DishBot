import requests
import bs4
import pandas as pd

df = pd.DataFrame(columns=["Title", "Cook Time", "Difficulty",
    "Method", "Period", "Calories"])

Events = [
"Романтический вечер",
"Торжество",
"Сюрприз для нее",
"Пост",
"Новый год, Рождество",
"Пасха",
"Пикник",
"Медовый Спас",
'Яблочный Спас',
'День Святого Валентина',
'Масленица',
'На 23 февраля',
'на 8 марта',
'Время дня']

DayTime = ["Завтрак", "Обед", "Ужин", "Легко перекусить"]
CookingTypes = ["Способ готовки",
'Гриль',
'Варим',
'В духовке',
'Жарим',
'На костре',
'На пару',
'Замораживаем',
'Консервируем',
'В мультиварке']

Diet = ['Диета',
'Низкокалорийная',
'Вегетарианская',
'Фитнес',
'Острые блюда',
'Детям',
'Низкоуглеводная',
'Диета Дюкана']

url = 'http://ligakulinarov.ru/recepty?sort=new&page='
ending = "#recipeboard"
last = 259
lst = []
site = requests.get(url + "1" + ending)
text = site.text
soup = bs4.BeautifulSoup(text, "html.parser")
Lis = soup.findAll("div", {"class": "author-wrap"})
soup = bs4.BeautifulSoup(str(Lis), "html.parser")
result = []
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
    charachteristics_list1 = []
    tmp_charachteristics_list = []
    for a in soup.findAll("div", {'class':"item value"}):
        tmp_charachteristics_list.append(a.get_text().split('\n'))
    for charachteristic in tmp_charachteristics_list:
        for item in charachteristic:
            if item != "" or item != '':
                charachteristics_list1.append(item)
    typeWasChosen = False
    timeWasChosen = False
    dietWasChosen = False
    CookingType = ""
    TimeOfConsuming =""
    diet = ""
    for item in charachteristics_list1:
        if item not in Events:
            if item in CookingTypes and not(typeWasChosen):
                CookingType += item
                typeWasChosen = True
            elif item in DayTime and not(timeWasChosen):
                TimeOfConsuming += item
                timeWasChosen = True
                charachteristics_list.append(item)
            elif item in Diet and not(dietWasChosen):
                diet += item
                dietWasChosen = True
                charachteristics_list.append(item)
            else:
                continue
    result.append([title, cook_time, difficulty, CookingType, TimeOfConsuming, diet])
    df['Title']=title
    df['Cook Time']=cook_time
    df['Difficulty'] = difficulty
    df['Method'] = CookingType
    df['Period'] = TimeOfConsuming
    df['Calories'] = diet

print(df)
"""/html/body/div[2]/div[3]/div/div[1]/section/div/ul[3]/li[1]"""
