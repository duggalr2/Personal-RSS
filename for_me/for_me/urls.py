"""for_me URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from app_file import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # url(r'^recommend_page/', views.recommend_page, name='recommend_page'),
    url(r'^home/', views.home, name='home'),
    url(r'^reddit/', views.reddit, name='reddit'),
    url(r'^google/', views.google, name='google'),
    url(r'^hn/', views.hacker_news, name='hacker_news'),
    url(r'^python/', views.python, name='python'),
    url(r'^other/', views.other, name='other'),
    # url(r'^tweets/', views.twitter, name='twitter'),
    url(r'^(?P<new_id>\d+)/feedbm/$', views.bookmark, name='feed_bookmark'),
    # url(r'^(?P<new_id>\d+)/feedsm/$', views.article_summary, name='feed_summarize'),
    url(r'^bookmark/', views.bookmark_page, name='bookmark'),
    url(r'^feature/', views.feature_list, name='feature'),
    url(r'^(?P<id>\d+)/delete/$', views.delete_feature, name='delete_feature'),
]
