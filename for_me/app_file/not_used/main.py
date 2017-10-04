import multiprocessing

from for_me.app_file.enew_rss import run_it
from not_used.etweet_feed import execute_tweets


def main_run():
    p1 = multiprocessing.Process(target=run_it)
    p2 = multiprocessing.Process(target=execute_tweets)
    p1.start()
    p2.start()
    p1.join()
    p2.join()


# if __name__ == '__main__':
#     # p1 = multiprocessing.Process(target=feed_execute)
#     p1 = multiprocessing.Process(target=run_it)
#     p2 = multiprocessing.Process(target=execute_tweets)
#     p1.start()
#     p2.start()
#     p1.join()
#     p2.join()

