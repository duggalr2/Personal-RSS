from django import forms
from .models import Url, Feeds, Tweet


class UrlForm(forms.ModelForm):
    class Meta:
        model = Url
        fields = [
            'url'
        ]


class FeedBookMark(forms.ModelForm):
    class Meta:
        model = Feeds
        fields = []


class TweetBookMark(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = []


