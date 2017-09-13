import tweepy
import time
import sqlite3
import multiprocessing
# from rss_feed import multiprocess

####################
# Fetching Tweets with Multiprocessing
####################


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


CONSUMER_KEY = 'DIVFNO658PjKMozopS1oLMOwo'
CONSUMER_SECRET = 'f8f8waBmcifaoiz0ohfwDMG3YPq0qnKzOL4aSRGBUb3JR2wc6g'
ACCESS_TOKEN = '1536654752-A4oOpKBfNjz0hOlRd0vl7y8DHKN5RlUORpcT0CM'
ACCESS_SECRET = 'yw5HYPaqt7C87jw8lQ1AFH7u9kfYYZL1prRd52YREFvFD'

f = open('/Users/Rahul/Desktop/Main/Side_projects/all_in_one/for_me/app_file/twitter_search_words')
tweet_hit_list = [line.replace('\n', '') for line in f.readlines()]


class UserTweets(object):

    """Using Tweepy to fetch tweets"""

    def __init__(self):
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
        self.api = tweepy.API(auth)

    def get_user_tweets(self, user_id):
        # tweet_info = [status.text for status in
        #               self.api.user_timeline(user_id, count=10)]
        tweet_info = []
        for status in self.api.user_timeline(user_id, count=10):
            urls = status.entities['urls']
            if len(urls) > 0:
                for y in urls:
                    tweet_info.append([status.text, y.get('url')])
            else:
                tweet_info.append([status.text])
        return tweet_info

    def get_search_test(self, word):
        search_result = []
        for status in self.api.search(q=word, count=10):
            urls = status.entities['urls']
            if len(urls) > 0:
                for y in urls:
                    search_result.append([status.text, y.get('url')])
            else:
                search_result.append([status.text])
        # search_results = [status.text for status in self.api.search(q=word, count=10)]
        # return list(zip(search_results, url_list))
        return search_result

    def get_search_tweets(self, work_queue, result_queue):
        while True:
            try:
                word = work_queue.get(block=False,)
            except:
                break

            search_result = []
            for status in self.api.search(q=word, count=10):
                urls = status.entities['urls']
                if len(urls) > 0:
                    for y in urls:
                        search_result.append([status.text, y.get('url')])
                else:
                    search_result.append([status.text])

            # search_results = [status.text for status in self.api.search(q=word, count=10)]
            result_queue.put(search_result)


# t = UserTweets()
# search_results = t.get_search_test('smart')
# for y in search_results:
#     print(y)


def execute_tweets():
    """
    """
    # start_time = time.time()
    default = 'https://twitter.com/'
    conn = sqlite3.connect('/Users/Rahul/Desktop/Main/Side_projects/all_in_one/for_me/db.nonsense')
    c = conn.cursor()
    c.execute("SELECT * FROM app_file_tweet")
    y = c.fetchall()
    t = UserTweets()
    if len(y) > 0:
        recent_primary_key = y[-1][0]
    else:
        recent_primary_key = 0

    feeds = multiprocess(tweet_hit_list, t.get_search_tweets)
    timeline = t.get_user_tweets('theduggal07')
    for i in feeds:
        i = [y for y in i if y != '\n']
        ti = [i for i in timeline if i != '\n']
        for tweet in i:
            recent_primary_key += 1
            if len(tweet) > 1:
                # c.execute("INSERT INTO app_file_tweet (id, tweet) VALUES (?, ?)", (recent_primary_key, tweet[0]))
                # conn.commit()
                # c.execute("INSERT INTO app_file_tweet (id, url) VALUES (?, ?)", (recent_primary_key, tweet[1]))
                # conn.commit()
                c.execute("INSERT INTO app_file_tweet (id, tweet, url) VALUES (?, ?, ?)",
                          (recent_primary_key, tweet[0], tweet[1]))
                conn.commit()
            else:
                c.execute("INSERT INTO app_file_tweet (id, tweet, url) VALUES (?, ?, ?)", (recent_primary_key, tweet[0], default))
                conn.commit()
        c.execute('SELECT MAX(Id) FROM app_file_tweet')
        new_id = c.fetchone()[0]
        recent_primary_key = new_id
        for tweet in ti:
            recent_primary_key += 1
            if len(tweet) > 1:
                c.execute("INSERT INTO app_file_tweet (id, tweet, url) VALUES (?, ?, ?)",
                          (recent_primary_key, tweet[0], tweet[1]))
                conn.commit()
            else:
                c.execute("INSERT INTO app_file_tweet (id, tweet, url) VALUES (?, ?, ?)",
                          (recent_primary_key, tweet[0], default))
                conn.commit()

        # for y in range(len(i)):
        #     recent_primary_key += 1
        #     c.execute("INSERT INTO app_file_tweet VALUES (?, ?)", (recent_primary_key, i[y]))
        #     conn.commit()
        #     recent_primary_key += 1
        #     c.execute("INSERT INTO app_file_tweet VALUES (?, ?)", (recent_primary_key, ti[y]))
        #     conn.commit()
    print('Twitter Done')

    # time.sleep(60.0 - ((time.time() - start_time) % 60.0))


# if __name__ == '__main__':
#     execute_tweets()



















# w = UserTweets()
# l = w.get_user_tweets('theduggal07')
# print(l)

# if __name__ == '__main__':

#     l = t.get_user_tweets('theduggal07')
#     execute_tweets()


    # for i in l:
    #     if i != '\n':
    #         print(i)
    # tweets = multiprocess(tweet_hit_list, t.get_search_tweets)

    # conn = sqlite3.connect('/Users/Rahul/Desktop/Main/Side_projects/all_in_one/for_me/db.nonsense')
    # c = conn.cursor()
    # c.execute("SELECT * FROM app_file_tweet")
    # c.execute("INSERT INTO app_file_tweet VALUES (?, ?)", (0, 'nonsense'))
    # conn.commit()
