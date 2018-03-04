import os
import sqlite3
import pandas as pd
import parserWeb
import requests

def initiate_query(listOfChoises):
    db = sqlite3.connect(r'C:\Users\Ric124\Desktop\Programming\Python\CookProj\db.db')
    for i in range(len(listOfChoises)):
        if listOfChoises[i] == "":
            listOfChoises[i] = "NULL"
    print(listOfChoises)
    curr = db.cursor()


def add_to_db():
    ps = parserWeb.Parser()
    df = ps.parsepy()
    df.set_index("Title")
    db = sqlite3.connect(r'C:\Users\Ric124\Desktop\Programming\Python\CookProj\db.db')

    df.to_csv(r'C:\Users\Ric124\Desktop\Programming\Python\CookProj\out.csv', encoding = 'cp1251')
    chunks = pd.read_csv(r'C:\Users\Ric124\Desktop\Programming\Python\CookProj\out.csv',
     encoding='cp1251',index_col="Title", chunksize=3)
    for chunk in chunks:
        chunk.columns = [column.replace(' ','_') for column in chunk.columns]
        chunk.to_sql('Recipes', db, if_exists='append')
