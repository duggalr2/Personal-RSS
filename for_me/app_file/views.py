from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, HttpResponseRedirect, HttpResponse, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import generic
from .models import Feeds, Tweet, BookMark
from .rss_feed import add_url
import json, requests
from .forms import UrlForm, FeedBookMark, TweetBookMark
from pprint import pprint
from .brute_feed import feed_execute
from .tweet_feed import execute_tweets
from django.views.decorators.csrf import csrf_exempt
from sklearn.feature_extraction.text import TfidfVectorizer


def pag(a, request):
    paginator = Paginator(a, 30)
    page = request.GET.get('page')
    try:
        blog_post = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        blog_post = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        blog_post = paginator.page(paginator.num_pages)
    return blog_post


def similarity(new_header):
    filepath = '/Users/Rahul/Desktop/Main/Side_projects/all_in_one/for_me/app_file/track_headers'
    f = open(filepath)
    lines = f.readlines()
    lines = [line.replace('\n', '') for line in lines]
    vect = TfidfVectorizer(min_df=1)
    scores = []
    for line in lines:
        tfidf = vect.fit_transform([line, new_header])
        cosine_similarity = (tfidf * tfidf.T).A[0,1]
        scores.append(cosine_similarity)
    scores.sort(reverse=True)
    return scores[0]


@csrf_exempt
def home(request):
    """Main Page"""
    b = Feeds.objects.all().order_by('-pk')
    if request.POST.get('url'):
        url = request.POST.get('url')
        add_url(url, '/Users/Rahul/Desktop/Main/Side_projects/all_in_one/for_me/app_file/urls')
        messages.success(request, 'Form submission successful')

    if request.method == 'GET' and 'refresh' in request.GET:
        recommend_id = feed_execute()
        execute_tweets()
        print(recommend_id)


    if request.method == 'POST' and 'pieFact' in request.POST:
        header = request.POST['pieFact']
        if header != 'More': # TODO: remove newsfeed, etc. as well
            with open('/Users/Rahul/Desktop/Main/Side_projects/all_in_one/for_me/app_file/track_headers', 'a') as f:
                f.write(header + '\n')
        return HttpResponse('success')

    return render(request, 'te.html', {'object_list': pag(b, request)})


def reddit(request):
    reddit_list = Feeds.objects.all().filter(category='Reddit').order_by('-pk')
    return render(request, 'reddit.html', {'object_list': pag(reddit_list, request)})


def google(request):
    google_list = Feeds.objects.all().filter(category='Google').order_by('-pk')
    return render(request, 'google.html', {'object_list': pag(google_list, request)})


def hacker_news(request):
    hn_list = Feeds.objects.all().filter(category='Hacker News').order_by('-pk')
    return render(request, 'hacker_news.html', {'object_list': pag(hn_list, request)})


def python(request):
    python_list = Feeds.objects.all().filter(category='Python').order_by('-pk')
    return render(request, 'python.html', {'object_list': pag(python_list, request)})


def other(request):
    other_list = Feeds.objects.all().filter(category='Other').order_by('-pk')
    return render(request, 'other.html', {'object_list': pag(other_list, request)})


def twitter(request):
    """Twitter Page"""
    tweets = Tweet.objects.all().order_by('-pk')
    if request.POST.get('search_word'):
        word = request.POST.get('search_word')
        add_url(word, '/Users/Rahul/Desktop/Main/Side_projects/all_in_one/for_me/app_file/twitter_search_words')
    return render(request, 'twitter.html', {'object_list': pag(tweets, request)})


def bookmark(request, new_id):
    """Handle's the bookmarking"""
    if request.method == 'GET' and 'feed_bookmark' in request.GET:
        instance = get_object_or_404(Feeds, id=new_id)
        form = FeedBookMark(request.GET, instance=instance)
        if form.is_valid():
            b = BookMark.objects.create(title=instance.title, link=instance.link)
            b.save()
            return redirect('home')

    elif request.method == 'GET' and 'tweet_bookmark' in request.GET:
        instance = get_object_or_404(Tweet, id=new_id)
        form = TweetBookMark(request.GET, instance=instance)
        if form.is_valid():
            b = BookMark.objects.create(title=instance.tweet)
            b.save()
            return redirect('twitter')


def bookmark_page(request):
    """Bookmark Page"""
    b = BookMark.objects.all().order_by('-pk')
    return render(request, 'bookmark.html', {'object_list': pag(b, request)})





############### CHATBOT ###############

# ACCESS_TOKEN = 'EAADFtkIzrDgBAMM5GfFUQ6CNnR1GUr4hib9XX6oC9EcrYtqr6LjftQwZCAGRVuhed5hY9pFDU8ukNDemq4KL4wCOiRwRntc0TScsVV9Rmv6yGCt3ZAZA56dd1t0TbgqPWT4gg1JFN0URbB7zUyihitHVGLitkkpISmjN38lvAZDZD'
#
# def post_facebook_message(fbid, received_message):
#     """Responding to incoming messages; helper function to post()"""
#
#     user_details_url = "https://graph.facebook.com/v2.6/%s" % fbid
#     user_details_params = {'fields': 'first_name,last_name,profile_pic', 'access_token': PAGE_ACCESS_TOKEN}
#     user_details = requests.get(user_details_url, user_details_params).json()
#     joke_text = 'Yo ' + user_details['first_name'] + '..! ' + joke_text
#
#     post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s' % PAGE_ACCESS_TOKEN
#     response_msg = json.dumps({"recipient": {"id": fbid}, "message": {"text": joke_text}})
#     status = requests.post(post_message_url, headers={"Content-Type": "application/json"}, data=response_msg)
#     pprint(status.json())
#
#
# class FeedBot(generic.View):
#
#     def get(self, request, *args, **kwargs):
#         """Verifying the access token"""
#
#         if self.request.GET['hub.verify_token'] == ACCESS_TOKEN:
#             return HttpResponse(self.request.GET['hub.challenge'])
#         else:
#             return HttpResponse('Error, invalid token')
#
#     @method_decorator(csrf_exempt)
#     def dispatch(self, request, *args, **kwargs):
#         return generic.View.dispatch(self, request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         """Handling incoming messages"""
#         # Converts the text payload into a python dictionary
#         incoming_message = json.loads(self.request.body.decode('utf-8'))
#         # Facebook recommends going through every entry since they might send
#         # multiple messages in a single call during high load
#         for entry in incoming_message['entry']:
#             for message in entry['messaging']:
#                 # Check to make sure the received call is a message call
#                 # This might be delivery, optin, postback for other events
#                 if 'message' in message:
#                     # Print the message to the terminal
#                     pprint(message)
#                     # Assuming the sender only sends text.
#                     post_facebook_message(message['sender']['id'], message['message']['text'])
#         return HttpResponse()




            # def add_url(request): # TODO: Change this and put it on the same page as home page!!
#     form = UrlForm(request.POST or None)
#     if form.is_valid():
#         instance = form.save(commit=False) # TODO: WTF IS COMMIT?
#         instance.save()
#         return HttpResponseRedirect('home')
#
#     context = {
#         'form': form
#     }
#     return render(request, )