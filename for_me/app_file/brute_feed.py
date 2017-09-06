import time
import sqlite3
import feedparser


f = open('/Users/Rahul/Desktop/Main/Side_projects/all_in_one/for_me/app_file/urls')
hit_list = [i.replace('\n', '') for i in f.readlines()]
# for url in hit_list:
#     print(url)


def categorize(url):
    if 'reddit' in url:
        category = 'Reddit'
    elif 'google' in url:
        category = 'Google'
    elif 'ycombinator' in url:
        category = 'Hacker News'
    elif 'python' in url:
        category = 'Python'
    else:
        category = 'Other'
    return category


def add_url(url, filename):
    with open(filename, 'a') as f:
        f.write(url + '\n')


def parse_feed(items):
    result, category_list = [], []
    for url in items:
        parsed_feed = feedparser.parse(url)
        category = categorize(url)
        for story in parsed_feed.get('entries'):
            title = story.get('title')
            link = story.get('link')
            result.append([title, link])
            category_list.append(category)
    return result, category_list


def feed_execute():
    """
    """
    start_time = time.time()
    conn = sqlite3.connect('/Users/Rahul/Desktop/Main/Side_projects/all_in_one/for_me/db.nonsense')
    c = conn.cursor()
    c.execute("SELECT * FROM app_file_feeds")
    y = c.fetchall()
    if len(y) > 0:
        recent_primary_key = y[-1][0]  # TODO: Do the faster way, wtf is this..
    else:
        recent_primary_key = 0

    feeds, category_list = parse_feed(hit_list)
    print(len(category_list), len(feeds))
    for number in range(len(feeds)):
        recent_primary_key += 1
        title = feeds[number][0]
        link = feeds[number][-1]
        category = category_list[number]
        c.execute("INSERT INTO app_file_feeds VALUES (?, ?, ?, ?)",
                  (recent_primary_key, title, link, category))
        conn.commit()
    print('RSS Done')

    # for i in feeds:
    #     recent_primary_key += 1
    #     title = i[0]
    #     link = i[-1]
    #     c.execute("INSERT INTO app_file_feeds VALUES (id, title, link, category)", (recent_primary_key, title, link, cate))
    #     conn.commit()
    #     c.execute("INSERT INTO app_file_feeds VALUES ()", (recent_primary_key, title, link))
    #     conn.commit()
    # print('RSS Done')
    # time.sleep(60.0 - ((time.time() - start_time) % 60.0))

# feed_execute()

