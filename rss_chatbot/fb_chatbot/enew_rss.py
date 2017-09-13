from multiprocessing.pool import ThreadPool  # uses threads, not processes
import feedparser
import sqlite3


f = open('/Users/Rahul/Desktop/Main/Side_projects/all_in_one/for_me/app_file/urls')
hit_list = [i.replace('\n', '') for i in f.readlines()]


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


def parse_feed(feed_url):
    result, category_list = [], []
    parsed_feed = feedparser.parse(feed_url)
    category = categorize(feed_url)
    for story in parsed_feed.get('entries'):
        title = story.get('title')
        link = story.get('link')
        result.append([title, link, category])
    return result


def feed_execute(parsed_feed):
    """
    """

    conn = sqlite3.connect('/Users/Rahul/Desktop/Main/Side_projects/all_in_one/for_me/db.nonsense')
    c = conn.cursor()
    c.execute('SELECT * FROM app_file_feeds WHERE id = (SELECT MAX(id) FROM app_file_feeds);')
    recent_primary_key = c.fetchone()[0]
    for number in range(len(parsed_feed)):
        recent_primary_key += 1
        title = parsed_feed[number][0]
        link = parsed_feed[number][1]
        category = parsed_feed[number][-1]
        c.execute("INSERT INTO app_file_feeds VALUES (?, ?, ?, ?)",
                  (recent_primary_key, title, link, category))
        conn.commit()
    print('RSS Done')


def run_it():
    """ Main function used in Django view"""
    pool = ThreadPool()   # ThreadPool instead of Pool
    results = pool.map(parse_feed, hit_list)
    for result in results:
        feed_execute(result)

# if __name__=="__main__":
#     run_it()
#     pool = ThreadPool()   # ThreadPool instead of Pool
#     results = pool.map(parse_feed, hit_list)
#     for result in results:
#         feed_execute(result)
