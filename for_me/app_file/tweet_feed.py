import tweepy
import time
import sqlite3
import multiprocessing
from rss_feed import multiprocess

####################
# Fetching Tweets with Multiprocessing
####################


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
        tweet_info = [status.text for status in
                      self.api.user_timeline(user_id, count=10)]
        # w = [status.entities for status in self.api.user_timeline(user_id, count=10)]
        return tweet_info

    def get_search_tweets(self, work_queue, result_queue):
        while True:

            try:
                word = work_queue.get(block=False,)
            except:
                break
            search_results = [status.text for status in self.api.search(q=word, count=10)]
            result_queue.put(search_results)


def execute_tweets():
    """
    """
    start_time = time.time()
    conn = sqlite3.connect('/Users/Rahul/Desktop/Main/Side_projects/all_in_one/for_me/db.nonsense')
    c = conn.cursor()
    c.execute("SELECT * FROM app_file_tweet")
    y = c.fetchall()
    t = UserTweets()
    if len(y) > 0:
        recent_primary_key = y[-1][0]
    else:
        recent_primary_key = 0
    while True:
        feeds = multiprocess(tweet_hit_list, t.get_search_tweets)
        timeline = t.get_user_tweets('theduggal07')
        for i in feeds:
            i = [y for y in i if y != '\n']
            ti = [i for i in timeline if i != '\n']
            for y in range(len(i)):
                recent_primary_key += 1
                c.execute("INSERT INTO app_file_tweet VALUES (?, ?)", (recent_primary_key, i[y]))
                conn.commit()
                recent_primary_key += 1
                c.execute("INSERT INTO app_file_tweet VALUES (?, ?)", (recent_primary_key, ti[y]))
                conn.commit()
        #     for y in i:
        #         recent_primary_key += 1
        #         c.execute("INSERT INTO app_file_tweet VALUES (?, ?)", (recent_primary_key, y))
        #         conn.commit()
        print('Twitter Done')
        time.sleep(60.0 - ((time.time() - start_time) % 60.0))

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
