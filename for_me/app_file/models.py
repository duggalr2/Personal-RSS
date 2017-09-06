from django.db import models

# Create your models here.


class Feeds(models.Model):
    title = models.CharField(max_length=500)
    link = models.CharField(max_length=500)
    category = models.CharField(max_length=500, blank=True)
    # keyword = models.CharField(max_length=1000)  # it must be for that particular id!


class Url(models.Model):
    url = models.URLField()


class Tweet(models.Model):
    tweet = models.CharField(max_length=500)
    url = models.CharField(max_length=500, default='https://twitter.com/')


class BookMark(models.Model):
    title = models.CharField(max_length=500)
    link = models.URLField(blank=True)


# class ArticleSummary(models.Model):
#     summary = models.CharField(max_length=)