from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, HttpResponseRedirect, HttpResponse, get_object_or_404, redirect
from .models import Feeds, Tweet, BookMark, Feature
from .rss_feed import add_url
from .enew_rss import run_it
from .forms import UrlForm, FeedBookMark, TweetBookMark, FeatureForm
from django.views.decorators.csrf import csrf_exempt
from sklearn.feature_extraction.text import TfidfVectorizer


def pag(a, request):
    paginator = Paginator(a, 30)
    page = request.GET.get('page')
    try:
        blog_post = paginator.page(page)
    except PageNotAnInteger:
        blog_post = paginator.page(1)
    except EmptyPage:
        blog_post = paginator.page(paginator.num_pages)
    return blog_post


def similarity(new_header):
    filepath = '/Users/Rahul/Desktop/Side_projects/all_in_one/for_me/app_file/track_headers'
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
    b = Feeds.objects.all().order_by('-pk')
    if request.POST.get('url'):
        url = request.POST.get('url')
        add_url(url, '/Users/Rahul/Desktop/Side_projects/all_in_one/for_me/app_file/urls')
        messages.success(request, 'Form submission successful')

    if request.method == 'POST' and 'refresh' in request.POST:
        run_it()
        return render(request, 'te.html', {'object_list': pag(b, request)})

    if request.POST.get('search'):
        search_word = request.POST.get('search')
        object_list = Feeds.objects.filter(title__contains=search_word)
        return render(request, 'te.html', {'object_list': pag(object_list, request)})

    return render(request, 'te.html', {'object_list': pag(b, request)})


def feature_list(request):
    feature_feed = Feature.objects.all().order_by('-pk')
    feature_form = FeatureForm(request.POST or None)
    if request.method == 'POST':
        if feature_form.is_valid():
            print('asdjasnd')
            feature_form.save()
            # feature.save()
            return redirect('feature')
    return render(request, 'feature.html', {'object_list': pag(feature_feed, request), 'form': feature_form})


def delete_feature(request, id=None):
    instance = get_object_or_404(Feature, id=id)
    instance.delete()
    return redirect("feature")


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


# def twitter(request):
#     """Twitter Page"""
#     tweets = Tweet.objects.all().order_by('-pk')
#     if request.POST.get('search_word'):
#         word = request.POST.get('search_word')
#         add_url(word, '/Users/Rahul/Desktop/Side_projects/all_in_one/for_me/app_file/twitter_search_words')
#     return render(request, 'twitter.html', {'object_list': pag(tweets, request)})


def bookmark(request, new_id):
    """Handle's the bookmarking"""
    if request.method == 'GET' and 'feed_bookmark' in request.GET:
        instance = get_object_or_404(Feeds, id=new_id)
        form = FeedBookMark(request.GET, instance=instance)
        if form.is_valid():
            b = BookMark.objects.create(title=instance.title, link=instance.link)
            b.save()
            # print(request.path)
            previous_url = request.META.get('HTTP_REFERER')
            # return HttpResponseRedirect()
            return redirect(previous_url)

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
