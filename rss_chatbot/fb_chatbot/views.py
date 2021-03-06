# from django.shortcuts import render
# from django.http.response import HttpResponse
# from django.views import generic
import json, requests, random, re
from pprint import pprint

from django.views import generic
from django.http.response import HttpResponse

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import sqlite3
from django.views.decorators.cache import cache_page

import multiprocessing
# from for_me.app_file.etweet_feed import execute_tweets
# from for_me.app_file.enew_rss import run_it
# from .etweet_feed import execute_tweets
# from .enew_rss import run_it


def post_facebook_message(fbid, recevied_message):
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=EAACBLgSkT6MBAKaKIBB9VD30ZB2uPTDfTUM2HCtzsp6vHR0WU7f7nZCjRi2NCghZAYnOgnjDMHZBf8AuM0l9MeQ1ZCwFYg5ZC4aSENTZAqKLZAVT0Xy6rBZCcZBY8OiXCdArZC9EpZADy0w7ZCnJtB4lubZC3h2w5m8HBW4KQruIoXb5Jkbkzw73kCLrdW'
    response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":recevied_message}})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"}, data=response_msg)
    pprint(status.json())


class Rss_view(generic.View):

    def get(self, request, *args, **kwargs):
        if self.request.GET['hub.verify_token'] == '2318934571':
            return HttpResponse(self.request.GET['hub.challenge'])
        else:
            return HttpResponse('Error, invalid token')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    # Post function to handle Facebook messages
    def post(self, request, *args, **kwargs):
        # Converts the text payload into a python dictionary
        incoming_message = json.loads(self.request.body.decode('utf-8'))
        # Facebook recommends going through every entry since they might send
        # multiple messages in a single call during high load
        for entry in incoming_message['entry']:
            conn = sqlite3.connect('/Users/Rahul/Desktop/Side_projects/all_in_one/for_me/db.nonsense')
            c = conn.cursor()
            for message in entry['messaging']:
                # Check to make sure the received call is a message call
                # This might be delivery, optin, postback for other events
                if 'message' in message:
                    # Print the message to the terminal
                    pprint(message)

                    if message['message']['text'] == 'latest':
                        c.execute("SELECT * FROM app_file_feeds")
                        y = c.fetchall()
                        object_list = y[(len(y)-20):len(y)]
                        for y in object_list:
                            title = y[1]
                            url = y[2]
                            m = title + ', ' + url
                            post_facebook_message(message['sender']['id'], m)

                    elif message['message']['text'] == 'hacker_news':
                        c.execute("SELECT * FROM app_file_feeds WHERE category='Hacker News'")
                        y = c.fetchall()
                        object_list = y[(len(y) - 20):len(y)]
                        for y in object_list:
                            title = y[1]
                            url = y[2]
                            m = title + ', ' + url
                            post_facebook_message(message['sender']['id'], m)

                    elif message['message']['text'] == 'reddit':
                        c.execute("SELECT * FROM app_file_feeds WHERE category='Reddit'")
                        y = c.fetchall()
                        object_list = y[(len(y) - 20):len(y)]
                        for y in object_list:
                            title = y[1]
                            url = y[2]
                            m = title + ', ' + url
                            post_facebook_message(message['sender']['id'], m)

                    elif message['message']['text'] == 'python':
                        c.execute("SELECT * FROM app_file_feeds WHERE category='Python'")
                        y = c.fetchall()
                        object_list = y[(len(y) - 20):len(y)]
                        for y in object_list:
                            title = y[1]
                            url = y[2]
                            m = title + ', ' + url
                            post_facebook_message(message['sender']['id'], m)

                    elif message['message']['text'] == 'google':
                        c.execute("SELECT * FROM app_file_feeds WHERE category='Google'")
                        y = c.fetchall()
                        object_list = y[(len(y) - 20):len(y)]
                        for y in object_list:
                            title = y[1]
                            url = y[2]
                            m = title + ', ' + url
                            post_facebook_message(message['sender']['id'], m)

                    elif message['message']['text'] == 'crypto':
                        c.execute("SELECT * FROM app_file_feeds")
                        object_list = c.fetchall()
                        for y in object_list:
                            title = y[1]
                            if 'bitcoin' in title or 'btc' in title or 'crypto' in title or 'cryptocurrency' in title or 'ethereum' in title:
                                url = y[2]
                                m = title + ', ' + url
                                post_facebook_message(message['sender']['id'], m)
                            else:
                                continue
                        # post_facebook_message(message['sender']['id'], 'hello')

                    elif message['message']['text'] == 'other':
                        c.execute("SELECT * FROM app_file_feeds WHERE category='Other'")
                        y = c.fetchall()
                        object_list = y[(len(y) - 20):len(y)]
                        for y in object_list:
                            title = y[1]
                            url = y[2]
                            m = title + ', ' + url
                            post_facebook_message(message['sender']['id'], m)
                    else:
                        post_facebook_message(message['sender']['id'], 'Do one of these commands: refresh, latest, hacker_news, reddit, python, google, other')

        return HttpResponse()

# elif message['message']['text'] == 'refresh':
#     p1 = multiprocessing.Process(target=run_it)
#     p2 = multiprocessing.Process(target=execute_tweets)
#     p1.start()
#     p2.start()
#     p1.join()
#     p2.join()
#     post_facebook_message(message['sender']['id'], 'Done')
