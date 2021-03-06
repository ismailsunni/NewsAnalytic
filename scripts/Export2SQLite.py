import sqlite3
import os

# import NewsTitle
from Crawler import load_pickle

try:
    news_titles = []
    public_figures = ['jokowi',
                      'wiranto',
                      'sby',
                      'anis matta',
                      'aburizal bakrie',
                      'hatta rajasa',
                      'jusuf kalla',
                      'prabowo']
    sites = ['detik.com', 'kompas.com', 'viva.co.id', 'okezone.com',
             'tribunnews.com', 'tempo.co', 'inilah.com', 'republika.co.id',
             'antaranews.com', 'metrotvnews.com']
    for public_figure in public_figures:
        for site in sites:
            filename = 'newstitles_' + \
                       public_figure + '_' + site.replace('.','') + '.pickle'
            # noinspection PyUnresolvedReferences
            filepath = os.path.join('..', '..', 'data', filename)
            if not os.path.exists(filepath):
                print public_figure, site, 'does not exist'
                continue
            print filepath
            data = load_pickle(filepath)
            for news_title in data:
                title = news_title.title
                public_figure = news_title.public_figure
                site = news_title.site
                url = news_title.url
                short_title = news_title.short_title
                desc = news_title.desc

                news_titles.append((title, public_figure,
                                    site, url, short_title, desc))

    con = sqlite3.connect('../data/news_data.db')
    cur = con.cursor()
    cur.execute('DROP TABLE IF EXISTS news')
    query = '''CREATE TABLE news(id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_title TEXT,
                public_figure TEXT,
                site TEXT,
                url TEXT,
                short_title TEXT,
                description TEXT,
                parsed_words TEXT,
                negation INTEGER,
                sentiment INTEGER,
                training_data INTEGER)'''
    cur.execute(query)
    query = 'INSERT INTO news(full_title, public_figure, site, url, ' \
            'short_title, description) VALUES(?,?,?,?,?,?)'
    print 'Run query :', query
    cur.executemany(query, news_titles)

    con.commit()
    con.close()
except sqlite3.Error, e:
    print e