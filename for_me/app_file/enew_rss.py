from multiprocessing.pool import ThreadPool  # uses threads, not processes
import feedparser
import sqlite3
from sumy.parsers.html import HtmlParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words


f = open('/Users/Rahul/Desktop/Side_projects/all_in_one/for_me/app_file/urls')
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


def parse_feed(feed_url):  # Todo: Dictionary possible?
    result = []
    parsed_feed = feedparser.parse(feed_url)
    for story in parsed_feed.get('entries'):
        title = story.get('title')
        link = story.get('link')
        category = categorize(feed_url)
        result.append([title, link, category])
    return result


def summarize(url):
    LANGUAGE = "english"
    SENTENCES_COUNT = 10

    # url = "https://medium.com/@shlominissan/object-oriented-programming-in-vanilla-javascript-f3945b15f08a"
    parser = HtmlParser.from_url(url, Tokenizer(LANGUAGE))
    stemmer = Stemmer(LANGUAGE)

    summarizer = Summarizer(stemmer)
    summarizer.stop_words = get_stop_words(LANGUAGE)

    s = ''
    for sentence in summarizer(parser.document, SENTENCES_COUNT):
        s += str(sentence) + ' '
    return s
    # for sentence in summarizer(parser.document, SENTENCES_COUNT):
    #     print(sentence)

conn = sqlite3.connect('/Users/Rahul/Desktop/Side_projects/all_in_one/for_me/db.nonsense', check_same_thread=False)
c = conn.cursor()


def feed_execute(parsed_feed):
    c.execute('SELECT MAX(id) FROM app_file_feeds')
    recent_primary_key = c.fetchone()
    if recent_primary_key[0] is None:
        recent_primary_key = 1
    else:
        recent_primary_key = recent_primary_key[0]

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
    """ Main function used in Django view to fetch all rss feeds"""
    c.execute("DELETE FROM app_file_feeds")
    conn.commit()
    pool = ThreadPool()
    results = pool.map(parse_feed, hit_list)
    for result in results:
        feed_execute(result)
