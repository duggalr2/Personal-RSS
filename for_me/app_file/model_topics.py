from newspaper import Article
# import nltk
import sqlite3

#############################################
# Categorizing each article: Training Set
#############################################


# url = 'http://cr.openjdk.java.net/~dlsmith/values.html'
# article = Article(url)
# article.download()
# article.parse()
# article.nlp()
# y = article.keywords
# print(article.summary)
# print(', '.join(y))


def get_all_keyWords():
    """Get all the keywords for the first 10000 articles in the database """
    conn = sqlite3.connect('/Users/Rahul/Desktop/Side_projects/all_in_one/for_me/db.nonsense')
    c = conn.cursor()
    c.execute("SELECT link FROM app_file_feeds")
    links = c.fetchall()
    for link in links:
        article = Article(link)
        article.parse()
        article.nlp()
        keyword = article.keywords  # list of keywords
        string_keyword = ', '.join(keyword)
        c.execute("INSERT INTO app_file_feeds (keyword) VALUES (?)", string_keyword)
    print('Done')
        # c.execute("INSERT INTO app_file_feeds VALUES (?, ?, ?)", (recent_primary_key, title, link))

if __name__ == '__main__':
    get_all_keyWords()