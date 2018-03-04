import bs4
import requests
import re
import sqlite3
import os
import pandas as pd

class Parser:
    def parsepy(self):
        url = 'http://ligakulinarov.ru/recepty?sort=new&page='
        ending = "#recipeboard"
        last = 259

        Events = ["Романтический вечер","Торжество","Сюрприз для нее","Пост",
        "Новый год, Рождество","Пасха","Пикник","Медовый Спас",'Яблочный Спас',
        'День Святого Валентина','Масленица','На 23 февраля','на 8 марта','Время дня']

        DayTime = ["Завтрак", "Обед", "Ужин", "Легко перекусить"]
        CookingTypes = ["Способ готовки",'Гриль','Варим','В духовке','Жарим',
        'На костре','На пару','Замораживаем','Консервируем','В мультиварке']

        Diet = ['Диета','Низкокалорийная','Вегетарианская','Фитнес','Острые блюда',
        'Детям','Низкоуглеводная','Диета Дюкана']


        counter = 0
        for i in range(1, last//2):
            new_url = url + str(i) + ending
            r = requests.get(new_url)
            text = r.text
            soup = bs4.BeautifulSoup(text, 'html.parser')
            lst = []
            Lis = soup.findAll("div", {"class": "author-wrap"})
            soup = bs4.BeautifulSoup(str(Lis), "html.parser")
            result = []
            for a in soup.find_all('a', href=True):
                if a["href"].startswith("/recepty") and a["href"] not in lst:
                    lst.append(a["href"])
            for tmp_url in lst:
                tmp_url = "http://ligakulinarov.ru" + tmp_url
                r = requests.get(tmp_url)
                soup = bs4.BeautifulSoup(r.text, "html.parser")
                title = soup.find("h1").get_text().strip()
                cook_time = bs4.BeautifulSoup(str(bs4.BeautifulSoup(str(soup.find("span",
                {'class':'value oneline'})),'html.parser').contents), 'html.parser').get_text()
                cook_time = cook_time[1:-1]
                difficulty = bs4.BeautifulSoup(str
                 (bs4.BeautifulSoup(str(
                  bs4.BeautifulSoup(str(soup.find("div",
                  {'class':'difficulty row oneline'})),'html.parser').contents
                  ),'html.parser').find("span", {'class':'value oneline'})),'html.parser').get_text()
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
                counter+=1
                result.append([ title, cook_time, difficulty, CookingType, TimeOfConsuming, diet, tmp_url])
        df1 = pd.DataFrame(result, columns=[ "Title", "Cook Time", "Difficulty",
            "Method", "Period", "Calories", "Link"])
        return df1
