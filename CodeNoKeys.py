import json
import requests
import urllib
import time
from time import sleep
import wx
from wx.adv import Animation, AnimationCtrl
import tweepy
from trello import TrelloClient
import random

consumer_key = '**********************'
consumer_secret = '**********************'
access_token = '**********************'
access_token_secret = '**********************'
TRELLO_API_TOKEN = '**********************'
TRELLO_API_KEY = '**********************'
#Keys and secrects could have been stored on a seperate file but due to limiting dependencies they have not been removed.

auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token,access_token_secret)
api = tweepy.API(auth)

client = TrelloClient(api_key= TRELLO_API_KEY, token= TRELLO_API_TOKEN )
all_boards= client.list_boards()
DCR_board = all_boards[0]
all_lists = DCR_board.all_lists()



class TestFrame(wx.Frame):

    failed_attemps = 0
    old_mention = None
    current_nw_len = 0
    current_ip_len = 0
    current_c_len = 0

    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, -1, title)

        self.animation = AnimationCtrl(self, pos=(300,40), size=(50000,5000), name="AnimationCtrl")
        self.animation.LoadFile("/Users/glynellis/Desktop/Dissertation/gifs/face prototype blink.gif")
        self.animation.Play()
        self.animation.Center()
        self.Show()


    def default_animation(self):
        random_animation = random.randint(1,7)
        self.animation.Center()

        if random_animation == 1:
            self.animation.LoadFile("/Users/glynellis/Desktop/Dissertation/gifs/face spin prototype moderate.gif")
            self.animation.Play()

        elif random_animation == 2:
            self.animation.LoadFile("/Users/glynellis/Desktop/Dissertation/gifs/face spin prototype fast.gif")
            self.animation.Play()

        elif random_animation == 3:
            self.animation.LoadFile("/Users/glynellis/Desktop/Dissertation/gifs/looking around prototype.gif")
            self.animation.Play()

        elif random_animation == 4:
            self.animation.LoadFile("/Users/glynellis/Desktop/Dissertation/gifs/up and down prototype.gif")
            self.animation.Play()

        elif random_animation == 5:
            self.animation.LoadFile("/Users/glynellis/Desktop/Dissertation/gifs/head bob fast.gif")
            self.animation.Play()

        else:
            self.animation.LoadFile("/Users/glynellis/Desktop/Dissertation/gifs/face prototype blink.gif")
            self.animation.Play()
        self.animation.Center()

        wx.CallLater(10000, self.check_wifi)


    def sleep_animation(self):
        self.animation.LoadFile("/Users/glynellis/Desktop/Dissertation/gifs/face prototype sleep.gif")
        self.animation.Play()
        wx.CallLater(10000, self.default_animation)


    def check_wifi(self):
        connection_status = False
        url = "https://www.google.com"
        try:
            urllib.urlopen(url)
            connection_status = True
        except:
            connection_status = False

        if connection_status == True:
            self.animation.LoadFile("/Users/glynellis/Desktop/Dissertation/gifs/Face prototype connection conformation.gif")
            self.animation.Play()
            wx.CallLater(3000, self.check_weather)
        elif connection_status == False:
            self.animation.LoadFile("/Users/glynellis/Desktop/Dissertation/gifs/Face prototype connection error.gif")
            self.animation.Play()

            if self.failed_attemps <3:
                self.failed_attemps += 1
                wx.CallLater(4000, self.default_animation)
            else:
                self.failed_attemps = 0
                wx.CallLater(10000, self.sleep_animation)


    def check_weather(self):
        try:
            r = requests.get("http://api.openweathermap.org/data/2.5/weather?q=Cardiff&APPID=76852765b5d0777aa3af09938f379342")

            if 'main":"Clouds' in r.text:
                self.animation.LoadFile("/Users/glynellis/Desktop/Dissertation/gifs/cloudy prototype.gif")
                self.animation.Play()

            if 'main":"Rain' in r.text:
                self.animation.LoadFile("/Users/glynellis/Desktop/Dissertation/gifs/rainfall prototype.gif")
                self.animation.Play()

            if 'main":"Clear' in r.text:
                self.animation.LoadFile("/Users/glynellis/Desktop/Dissertation/gifs/sunny prototype.gif")
                self.animation.Play()

            if 'main":"Mist' in r.text:
                self.animation.LoadFile("/Users/glynellis/Desktop/Dissertation/gifs/mist prototype 2.gif")
                self.animation.Play()

            if 'main":"Haze' in r.text:
                self.animation.LoadFile("/Users/glynellis/Desktop/Dissertation/gifs/haze prototype.gif")
                self.animation.Play()

            if 'main":"Snow' in r.text:
                self.animation.LoadFile("/Users/glynellis/Desktop/Dissertation/gifs/snow prototype.gif")
                self.animation.Play()

            if 'main":"Fog' in r.text:
                self.animation.LoadFile("/Users/glynellis/Desktop/Dissertation/gifs/fog prototype.gif")
                self.animation.Play()
        except:
            self.animation.LoadFile("/Users/glynellis/Desktop/Dissertation/gifs/Face prototype error dead.gif")
            self.animation.Play()

        self.Show()
        wx.CallLater(5000, self.check_twitter)


    def check_twitter(self):
        self.my_mentions = api.mentions_timeline(count = 1)
        self.new_mention = str(self.my_mentions)

        if self.new_mention != self.old_mention:
            self.old_mention = self.new_mention
            self.animation.LoadFile("/Users/glynellis/Desktop/Dissertation/gifs/twitter mention prototype.gif")
            self.animation.Play()
        else:
            self.animation.LoadFile("/Users/glynellis/Desktop/Dissertation/gifs/no Twitter.gif")
            self.animation.Play()
        wx.CallLater(5000, self.check_trello_not_working)


    def check_trello_not_working(self):
        list_not_working_on = all_lists[0]
        lnw_cards = list_not_working_on.list_cards()
        if len(lnw_cards) > self.current_nw_len:
            self.animation.LoadFile("/Users/glynellis/Desktop/Dissertation/gifs/trello to do list prototype.gif")
            self.animation.Play()
        else:
            self.animation.LoadFile("/Users/glynellis/Desktop/Dissertation/gifs/no Trello working on.gif")
            self.animation.Play()
        self.current_nw_len = len(lnw_cards)
        wx.CallLater(2000, self.check_working_on)

    def check_working_on(self):
        list_in_progress = all_lists[1]
        lip_cards = list_in_progress.list_cards()
        if len(lip_cards) > self.current_ip_len:
            self.animation.LoadFile("/Users/glynellis/Desktop/Dissertation/gifs/trello doing list prototype .gif")
            self.animation.Play()
        else:
            self.animation.LoadFile("/Users/glynellis/Desktop/Dissertation/gifs/no Trello working on-2.gif")
            self.animation.Play()
        self.current_ip_len = len(lip_cards)
        wx.CallLater(2000, self.check_completed)

    def check_completed(self):
        list_completed = all_lists[2]
        lc_cards = list_completed.list_cards()
        if len(lc_cards) > self.current_c_len:
            self.animation.LoadFile("/Users/glynellis/Desktop/Dissertation/gifs/trello complete list prototype.gif")
            self.animation.Play()
        else:
            self.animation.LoadFile("/Users/glynellis/Desktop/Dissertation/gifs/no Trello completed.gif")
            self.animation.Play()
        self.current_c_len = len(lc_cards)
        wx.CallLater(2000, self.default_animation)


if __name__ == '__main__':
    app = wx.App()
    frame = TestFrame(None, -1, "Desktop Combanion Robot")
    frame.default_animation()
    app.MainLoop()
