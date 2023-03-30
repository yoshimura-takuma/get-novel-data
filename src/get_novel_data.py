import requests
from bs4 import BeautifulSoup
import sqlite3
import time
import datetime
import lxml

# セッティング
WAIT_TIME = 10
DB_NAME = "./resource/2022novel.sqlite3"
#CSV_NAME = "tripadvisor.csv"
headers = {'User-Agent': 'UH Crawler System'}

def get_html_web(url):
    try:
        print("Webより取得中：{}".format(url))
        r = requests.get(url, headers=headers)
        html = r.text
        print(f"{WAIT_TIME}秒待ち")
        time.sleep(WAIT_TIME)
    except HTTPError as e:
        print(e)
        raise e
    except URLError as e:
        print("Not Found: " + url)
        raise e
    return html

def get_html(url, dbname):
    # sqlite3に接続
    conn = sqlite3.connect(dbname)
    curs = conn.cursor()
    try:
        # DBにキャッシュがあるかどうかをチェックする
        select = "SELECT crawl_date FROM url_html WHERE crawl_date = ? ORDER BY html DESC"
        curs.execute(select, (date, ))
        l = curs.fetchall()
        if len(l) == 0:
            html = get_html_web(url)
            # DBへ保存
            insert = "INSERT INTO url_html(crawl_date, url, html) VALUES(?, ?, ?)"
            curs.execute(insert, (date, url, html))
            conn.commit()
        else:
            print("DBより取得：{}".format(url))
            select = "SELECT html FROM url_html WHERE crawl_date = ? ORDER BY html DESC"
            curs.execute(select, (date, ))
            l = curs.fetchall()
            html = l[0][0]
    except Exception as e:
        raise e
    finally:
        curs.close()
        conn.close()
    return html

year = datetime.datetime.today().year
month = datetime.datetime.today().month
day = datetime.datetime.today().day

date = int(year)*10000+int(month)*100+int(day)
url = 'https://yomou.syosetu.com/rank/list/type/daily_total/'
html = get_html(url, DB_NAME)
# print(html)
soup = BeautifulSoup(html, 'lxml')
for sep in soup.find_all('div', class_='ranking_list'):
    # print(sep.find('a').text)
    l = []
    for keyword in sep.find('td', class_='keyword').find_all('a'):
        l.append(keyword.text)
    print(l)