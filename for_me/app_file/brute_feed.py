import time
import sqlite3
import feedparser


f = open('/Users/Rahul/Desktop/Main/Side_projects/all_in_one/for_me/app_file/urls')
hit_list = [i.replace('\n', '') for i in f.readlines()]


def add_url(url, filename):
    with open(filename, 'a') as f:
        f.write(url + '\n')


def parse_feed(items):
    result = []
    for url in items:
        parsed_feed = feedparser.parse(url)
        for story in parsed_feed.get('entries'):
            title = story.get('title')
            link = story.get('link')
            result.append([title, link])
    return result


def feed_execute():
    """
    """
    start_time = time.time()
    conn = sqlite3.connect('/Users/Rahul/Desktop/Main/Side_projects/all_in_one/for_me/db.nonsense')
    c = conn.cursor()
    c.execute("SELECT * FROM app_file_feeds")
    y = c.fetchall()
    if len(y) > 0:
        recent_primary_key = y[-1][0]
    else:
        recent_primary_key = 0
    while True:
        feeds = parse_feed(hit_list)
        for i in feeds:
            recent_primary_key += 1
            title = i[0]
            link = i[-1]
            c.execute("INSERT INTO app_file_feeds VALUES (?, ?, ?)", (recent_primary_key, title, link))
            conn.commit()
        print('RSS Done')
        time.sleep(60.0 - ((time.time() - start_time) % 60.0))



