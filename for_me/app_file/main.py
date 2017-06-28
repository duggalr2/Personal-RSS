from tweet_feed import execute_tweets
from brute_feed import feed_execute
import multiprocessing
# from rss_feed import feed_execute

##################

##################




if __name__ == '__main__':
    # p1 = multiprocessing.Process(target=feed_execute)
    p1 = multiprocessing.Process(target=feed_execute)
    p2 = multiprocessing.Process(target=execute_tweets)
    p1.start()
    p2.start()
    p1.join()
    p2.join()

