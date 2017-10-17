from sumy.parsers.html import HtmlParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words


def summarize():
    LANGUAGE = "english"
    SENTENCES_COUNT = 10

    url = "https://medium.com/@shlominissan/object-oriented-programming-in-vanilla-javascript-f3945b15f08a"
    parser = HtmlParser.from_url(url, Tokenizer(LANGUAGE))
    stemmer = Stemmer(LANGUAGE)

    summarizer = Summarizer(stemmer)
    summarizer.stop_words = get_stop_words(LANGUAGE)
    s = ''
    for sentence in summarizer(parser.document, SENTENCES_COUNT):
        s += str(sentence ) + ' '
    return s
    summary = summarizer(parser.document, SENTENCES_COUNT)
    return [sentence for sentence in summarizer(parser.document, SENTENCES_COUNT)]

print(summarize())