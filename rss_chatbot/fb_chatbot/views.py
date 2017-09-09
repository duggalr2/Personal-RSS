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


def post_facebook_message(fbid, recevied_message):
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=EAACBLgSkT6MBAFPCVH4fIsASNNnH22iXWZAWqn5QBo99jhE402Ap5O4EZBlJ61mgv3uzScpKs1Dhn8c9Oop7SKMT2z8YjXeQujRTSlkwSKa7pin2BlJzxcJb94q4486G19CX7lR47wSbfkW6rcPyZAisJiv3Tne7RuH9ccuORlKdvCQL2Es'
    response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":recevied_message}})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"}, data=response_msg)
    pprint(status.json())


class Rss_view(generic.View):

    def get(self, request, *args, **kwargs):
        if self.request.GET['hub.verify_token'] == '2314':
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
            conn = sqlite3.connect('/Users/Rahul/Desktop/Main/Side_projects/all_in_one/for_me/db.nonsense')
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
                        post_facebook_message(message['sender']['id'], 'Do one of these commands: latest, hacker_news, reddit, python, google, other')
        return HttpResponse()

