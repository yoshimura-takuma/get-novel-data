import sqlite3

DB_NAME = "./resource/2022novel.sqlite3"
conn = sqlite3.connect(DB_NAME)
# SQLiteを操作するためのカーソルを作成
cur = conn.cursor()
cur.execute(
    'CREATE TABLE url_html(crawl_date INTEGER PRIMARY KEY, url STRING, html STRING)'
)
conn.close()