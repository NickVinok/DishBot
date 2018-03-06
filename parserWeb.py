import bs4
import requests
from config import EVENTS, DAYTIME, DIET, COOKINGTYPES


class Parser:
    url = 'http://ligakulinarov.ru/recepty?sort=new&page='
    ending = "#recipeboard"
    last = 259
    counter = 0
    final_dish_charachteristics = list()

    def parse_page_for_url(self):
        """
        Этот цикл идёт по страницам сайта
        и считывает оттуда url рецептов
        """
        for i in range(1, self.last):
            new_url = self.url + str(i) + self.ending
            r = requests.get(new_url)
            soup = bs4.BeautifulSoup(r.text, 'html.parser')
            recipes_on_page = []
            Lis = soup.findAll("div", {"class": "author-wrap"})
            soup = bs4.BeautifulSoup(str(Lis), "html.parser")
            for a in soup.find_all('a', href=True):
                if a["href"].startswith(
                        "/recepty") and a["href"] not in recipes_on_page:
                    recipes_on_page.append(a["href"])
            self.parse_page_with_recipes(recipes_on_page)

    def parse_page_with_recipes(self, recipes_on_page):
        """
        В этом цикле мы переходим на страницы рецептов
        И добавляем в список нужные нам данные
        TODO переделать список в словарь, ибо это логичнее
        Возможно стоит переделать в отдельный метод
        """
        for tmp_url in recipes_on_page:
            tmp_url = "http://ligakulinarov.ru" + tmp_url
            r = requests.get(tmp_url)
            soup = bs4.BeautifulSoup(r.text, "html.parser")

            title = soup.find("h1").get_text().strip()
            cook_time = self.finding_cooking_time(soup)[
                1:-1]  #Избавляемся от фигурных скобок в начале и конце текста
            difficulty = self.finding_cooking_difficulty(soup)

            charachteristics_list = []
            charachteristics_list1 = []
            tmp_charachteristics_list = []
            for a in soup.findAll("div", {'class': "item value"}):
                tmp_charachteristics_list.append(a.get_text().split('\n'))
            for charachteristic in tmp_charachteristics_list:
                for item in charachteristic:
                    if item != "":
                        charachteristics_list1.append(item)
            typeWasChosen = False
            timeWasChosen = False
            dietWasChosen = False
            CookingType = ""
            TimeOfConsuming = ""
            diet = ""
            for item in charachteristics_list1:
                if item not in EVENTS:
                    if item in COOKINGTYPES and not (typeWasChosen):
                        CookingType += item
                        typeWasChosen = True
                    elif item in DAYTIME and not (timeWasChosen):
                        TimeOfConsuming += item
                        timeWasChosen = True
                        charachteristics_list.append(item)
                    elif item in DIET and not (dietWasChosen):
                        diet += item
                        dietWasChosen = True
                        charachteristics_list.append(item)
                    else:
                        continue
            self.final_dish_charachteristics.append({
                "id": self.counter,
                "Title": title,
                "Cook Time": cook_time,
                "Difficulty": difficulty,
                "Method": CookingType,
                "Period": TimeOfConsuming,
                "Calories": diet,
                "Link": tmp_url
            })
            self.counter += 1

    def finding_cooking_time(self, soup):
        return bs4.BeautifulSoup(
            str(
                bs4.BeautifulSoup(
                    str(soup.find("span", {
                        'class': 'value oneline'
                    })), 'html.parser').contents), 'html.parser').get_text()

    def finding_cooking_difficulty(self, soup):
        return bs4.BeautifulSoup(
            str(
                bs4.BeautifulSoup(
                    str(
                        bs4.BeautifulSoup(
                            str(
                                soup.find("div", {
                                    'class': 'difficulty row oneline'
                                })), 'html.parser').contents),
                    'html.parser').find("span", {
                        'class': 'value oneline'
                    })), 'html.parser').get_text()


"""
df1 = pd.DataFrame(
    result,
    columns=[
        "Title", "Cook Time", "Difficulty", "Method", "Period",
        "Calories", "Link"
    ])
return df1
"""
