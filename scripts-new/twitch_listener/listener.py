import pandas as pd
from socket import socket
from time import time, sleep
from twitch_listener import utils
import select
from pathlib import Path
import os
import requests
import json
from datetime import datetime
import urllib.request, json 
from datetime import date

class connect_twitch(socket):
    
    def __init__(self, nickname, oauth, client_id, oauth_api):

        self.nickname = nickname
        
        self.client_id = client_id
        if oauth.startswith('oauth:'):
            self.oauth = oauth
        else:
            self.oauth = 'oauth:' + oauth
        
        if oauth_api.startswith('Bearer'):
            self.oauth_api = oauth_api
        else:
            self.oauth_api = 'Bearer ' + oauth_api
        self.botlist = ['moobot' 'nightbot', 'ohbot',
                        'deepbot', 'ankhbot', 'vivbot',
                        'wizebot', 'coebot', 'phantombot',
                        'xanbot', 'hnlbot', 'streamlabs',
                        'stay_hydrated_bot', 'botismo', 'streamelements',
                        'slanderbot', 'fossabot']
            
        # IRC parameters
        self._server = "irc.chat.twitch.tv"
        self._port = 6667
        self._passString = f"PASS " + self.oauth + f"\n"
        self._nameString = f"NICK " + self.nickname + f"\n"
        
        self.bytes_seperator = bytes("||||", 'utf-8')
        

    def _join_channels(self, channels):

        self._sockets = {}
        self.joined = {}
        self._loggers = {}
        
        # Establish socket connections
        for channel, broadcast_id in channels.items():
            self._sockets[channel] = socket()
            self._sockets[channel].connect((self._server, self._port))
            self._sockets[channel].send(self._passString.encode('utf-8'))
            self._sockets[channel].send(self._nameString.encode('utf-8'))
            
            joinString = f"JOIN #" + channel.lower() + f"\n"
            self._sockets[channel].send(joinString.encode('utf-8'))
            #self._loggers[channel] = utils.setup_loggers(channel, os.getcwd() + '/logs/' + channel + '.log')
            self._loggers[channel] = utils.setup_sqllite_loggers(channel)
            
            self.joined[channel] = broadcast_id
        
    def listen(self, channels, duration = 1000, until_offline = False, debug = False, file_path = ''):

        """
        Method for scraping chat data from Twitch channels.

        Parameters:
            channels (string or list) 
                - Channel(s) to connect to.
            duration (int)           
                 - Length of time to listen for.
            debug (bool, optional)             
                 - Debugging feature, will likely be removed in later version.
        """

        
        self._join_channels(channels)
        print("Channels Online")
        startTime = time()
        print("start time: ", startTime)
        start_time = datetime.now()
        print("start time: ", start_time)
        start_date = date.today()
        print("start_date",start_date)
        
        if until_offline is False:
            # Collect data while duration not exceeded and channels are live
            print("Nisha until offline is false")
            while (time() - startTime) < duration: 

                if len(utils.is_live(channels)) == 0:
                    print("Channels Offline")
                    break

                now = time() # Track loop time for adaptive rate limiting
                ready_socks,_,_ = select.select(self._sockets.values(), [], [], 1)
                for channel, broadcast_id in self.joined.items():
                    sock = self._sockets[channel]
                    if sock in ready_socks:
                        response = sock.recv(16384)
                        if b"PING :tmi.twitch.tv\r\n" in response:
                            sock.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
                            if debug:
                                print("\n\n!!Look, a ping: \n")
                                print(response)
                                print("\n\n")
                        else:
                            contents_name = requests.get('https://api.twitch.tv/helix/channels?broadcaster_id=' + broadcast_id,
                                headers={"Authorization":self.oauth_api,
                                         "Client-Id": self.client_id}).content

                            followers = requests.get('https://api.twitch.tv/helix/users/follows?to_id=' + broadcast_id,
                                headers={"Authorization":self.oauth_api,
                                         "Client-Id": self.client_id}).content
                            
                            followers_count = json.loads(followers)['total']
                            
                            stream_length = datetime.now() - start_time
                            td_mins = int(round(stream_length.total_seconds() / 60))
                            
                            with urllib.request.urlopen('https://tmi.twitch.tv/group/user/{}/chatters'.format(channel)) as url:
                                chatter_count = json.loads(url.read().decode())['chatter_count']
                                
                            viewer_count = utils.view_count(chatter_count)
                            subs_count = utils.subscriber_count(followers_count)
                                  
                            self._loggers[channel].info(response + self.bytes_seperator 
                                                + contents_name + self.bytes_seperator 
                                                + followers + self.bytes_seperator
                                                + bytes(str(chatter_count),'utf-8') + self.bytes_seperator
                                                + bytes(str(viewer_count),'utf-8') + self.bytes_seperator 
                                                + bytes(str(start_time),'utf-8') + self.bytes_seperator
                                                + bytes(str(subs_count),'utf-8') + self.bytes_seperator
                                                + bytes(str(start_date),'utf-8') + self.bytes_seperator
                                                + bytes(str(td_mins), 'utf-8')) 

                            if debug:
                                print(response)
                        elapsed = time() - now
                        if elapsed < 60/800:
                            sleep( (60/800) - elapsed) # Rate limit
                    else: # if not in ready_socks
                        pass
                
        else:
            print("Nisha until offline is true")
            online = True
            while online: 
                print("Nisha while online")

                if len(utils.is_live(channels)) == 0:
                    online = False
                    print("Channels Online")
                    break

                now = time() # Track loop time for adaptive rate limiting
                ready_socks,_,_ = select.select(self._sockets.values(), [], [], 1)
                print("ready_socks: ", ready_socks)
                for channel, broadcast_id in self.joined.items():
                    print("channel: ", channel)
                    print("broadcast_id: ", broadcast_id)
                    sock = self._sockets[channel]
                    print("sock: ", sock)
                    if sock in ready_socks:
                        print("sock in ready_socks: ", sock)
                        response = sock.recv(16384)
                        print("response: ", response)
                        if b"PING :tmi.twitch.tv\r\n" in response:
                            print("PING :tmi.twitch.tv\r\n" in response)
                            sock.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
                            if debug:
                                print("\n\n!!Look, a ping: \n")
                                print(response)
                                print("\n\n")
                        else:
                            print("Nisha else")
                            contents_name = requests.get('https://api.twitch.tv/helix/channels?broadcaster_id=' + broadcast_id,
                                        headers={"Authorization":self.oauth_api,
                                                 "Client-Id": self.client_id}).content
                            print("contents_name: ", contents_name)
                            followers = requests.get('https://api.twitch.tv/helix/users/follows?to_id=' + broadcast_id,
                                        headers={"Authorization":self.oauth_api,
                                                 "Client-Id": self.client_id}).content
                            
                            followers_count = json.loads(followers)['total']

                            stream_length = datetime.now() - start_time
                            td_mins = int(round(stream_length.total_seconds() / 60))
                            print("td_mins: ", td_mins)      
                            # with urllib.request.urlopen('https://tmi.twitch.tv/group/user/{}/chatters'.format(channel)) as url:
                            #     chatter_count = json.loads(url.read().decode())['chatter_count']
                            # print("chatter_count: ", chatter_count)    
                            
                            
                            # moderator = requests.get('https://api.twitch.tv/helix/moderation/moderators?broadcaster_id=' + broadcast_id, 
                            #     headers={"Authorization":self.oauth_api,
                            #              "Client-Id": self.client_id}).content
                            # print("moderator: ", moderator)
                            
                            # chatter_count = requests.get('https://api.twitch.tv/helix/chat/chatters?broadcaster_id=' + broadcast_id, 
                            #     headers={"Authorization":self.oauth_api,
                            #              "Client-Id": self.client_id}).content
                            
                                
                            chatter_count = 12000
                            viewer_count = utils.view_count(chatter_count)
                            subs_count = utils.subscriber_count(followers_count)
                                  
                            self._loggers[channel].info(response + self.bytes_seperator 
                                                + contents_name + self.bytes_seperator 
                                                + followers + self.bytes_seperator
                                                + bytes(str(chatter_count),'utf-8') + self.bytes_seperator
                                                + bytes(str(viewer_count),'utf-8') + self.bytes_seperator 
                                                + bytes(str(start_time),'utf-8') + self.bytes_seperator
                                                + bytes(str(subs_count),'utf-8') + self.bytes_seperator
                                                + bytes(str(start_date),'utf-8') + self.bytes_seperator
                                                + bytes(str(td_mins), 'utf-8')) 

                            if debug:
                                print(response)
                        elapsed = time() - now
                        if elapsed < 60/800:
                            sleep( (60/800) - elapsed) # Rate limit
                    else: # if not in ready_socks
                        pass
        if debug:
            print("Collected for " + str(time()-startTime) + " seconds")
        # Close sockets once not collecting data
        for channel in self.joined:
            self._sockets[channel].close()
        