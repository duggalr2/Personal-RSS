import multiprocessing
import time
import sqlite3
import feedparser


##########################################
# RSS Feed Parser with multiprocessing
##########################################


# AFTER EVERYTHING IS DONE:
    # TODO: Add docstrings
    # TODO: Optimize this and get the complexity!


f = open('/Users/Rahul/Desktop/Side_projects/all_in_one/for_me/app_file/urls')
hit_list = [i.replace('\n', '') for i in f.readlines()]


def add_url(url, filename):
    with open(filename, 'a') as f:
        f.write(url + '\n')


def parse_feed(work_queue, result_queue):
    while True:

        try:
            feed_url = work_queue.get(block=False,)
        except:
            break  # this will end the processes

        parsed_feed = feedparser.parse(feed_url)
        for story in parsed_feed.get('entries'):
            title = story.get('title')
            link = story.get('link')
            result_queue.put([title, link])


def dump_queue(result_queue):
    li = []
    while True:
        if result_queue.get() == 'stop':
            break
        li.append(result_queue.get())
    return li


def multiprocess(items, target_function):
    """
    Multiprocessing Abstraction
    """
    work_queue = multiprocessing.Queue()
    for feed in items:
        work_queue.put(feed)

    result_queue = multiprocessing.Queue()

    workers = []
    for i in range(len(items)):
        worker = multiprocessing.Process(target=target_function, args=(work_queue, result_queue,))
        worker.start()
        workers.append(worker)

    for w in workers:
        w.join()

    result_queue.put('stop')  # to indicate last element in queue... qsize isn't working
    feed_list = dump_queue(result_queue)
    return feed_list


def feed_execute():
    """
    """
    start_time = time.time()
    conn = sqlite3.connect('/Users/Rahul/Desktop/Side_projects/all_in_one/for_me/db.nonsense')
    c = conn.cursor()
    c.execute("SELECT * FROM app_file_feeds")
    y = c.fetchall()
    if len(y) > 0:
        recent_primary_key = y[-1][0]
    else:
        recent_primary_key = 0
    while True:
        feeds = multiprocess(hit_list, parse_feed)
        for i in feeds:
            recent_primary_key += 1
            title = i[0]
            link = i[-1]
            print(recent_primary_key, title, link)
            # c.execute("INSERT INTO app_file_feeds VALUES (?, ?, ?)", (recent_primary_key, title, link))
            # conn.commit()
        print('RSS Done')
        time.sleep(60.0 - ((time.time() - start_time) % 60.0))


if __name__ == '__main__':
    feed_execute()









# conn = sqlite3.connect('db.nonsense')
# c = conn.cursor()
# c.execute("INSERT INTO app_file_feeds VALUES (?, ?, ?)", (1, 'gol', 'sdd'))
# conn.commit()
# c.execute("INSERT INTO app_file_feeds VALUES (?, ?, ?)", (2, 'dog', 'cat'))
# conn.commit()
# c.execute("SELECT * FROM app_file_feeds")
# print(c.fetchall())  # <-- that's the primary key;

# def main():
#     work_queue = multiprocessing.Queue()
#     for feed in hit_list:
#         work_queue.put(feed)
#
#     result_queue = multiprocessing.Queue()
#
#     workers = []
#     for i in range(len(hit_list)):
#         worker = multiprocessing.Process(target=parse_feed, args=(work_queue, result_queue, ))
#         worker.start()
#         workers.append(worker)
#
#     for w in workers:
#         w.join()
#
#     result_queue.put('stop')  # to indicate last element in queue... qsize isn't working
#     feed_list = dump_queue(result_queue)
#     return feed_list


# hit_list = ['https://news.ycombinator.com/rss', 'http://feeds.arstechnica.com/arstechnica/index/',
#             'http://feeds.feedburner.com/TechCrunch/', 'http://feeds.feedburner.com/TechCrunch/startups',
#             'http://planetpython.org/rss20.xml', 'http://waitbutwhy.com/feed',
#             'http://rss.slashdot.org/Slashdot/slashdotMain']

# f = FileProcessor('/Users/Rahul/Desktop/Main/Side_projects/all_in_one/for_me/app_file/urls', 'train')
# l = f.readFile()
# hit_list = [i.replace('\n', '') for i in l]
# print(hit_list)

# print(feedparser.parse(hit_list[3]))
# hit_list = ['https://news.ycombinator.com/rss']
