from bs4 import BeautifulSoup
import sqlite3
import time
import datetime
import lxml

DB_NAME = "./resource/2022novel.sqlite3"

start_date = int(input("input START_DATE: "))
end_date = int(input("input START_DATE: "))

def get_html(start_date, end_date, dbname):
    # sqlite3に接続
    conn = sqlite3.connect(dbname)
    curs = conn.cursor()
    try:
        # DBにキャッシュがあるかどうかをチェックする
        select = "SELECT html FROM url_html WHERE crawl_date >= ? AND crawl_date <= ? ORDER BY crawl_date DESC"
        curs.execute(select, (start_date, end_date, ))
        l = curs.fetchall()
        htmls = l[0]
    except Exception as e:
        raise e
    finally:
        curs.close()
        conn.close()
    return htmls


htmls = get_html(start_date, end_date, DB_NAME)
for html in htmls:
    soup = BeautifulSoup(html, 'lxml')
    for sep in soup.find_all('div', class_='ranking_list'):
        # print(sep.find('a').text)
        l = []
        for keyword in sep.find('td', class_='keyword').find_all('a'):
            l.append(keyword.text)
        print(l)