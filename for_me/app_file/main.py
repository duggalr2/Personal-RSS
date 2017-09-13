import multiprocessing
from for_me.app_file.etweet_feed import execute_tweets
from for_me.app_file.enew_rss import run_it


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

