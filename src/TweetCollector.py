# -*- coding: utf-8 -*-
import tweepy
import os
import pandas as pd
import numpy as np
import re
from datetime import datetime
try:
    from src.AuthTwitterUser import *
except:
    from AuthTwitterUser import *

class TweetCollector():
    def __init__(self, api):
        self.create_coord_from_file()
        self.api = api


    def get_tweets_from_topic(self,
                              query,
                              retweet=False,
                              lang="pl", 
                              numbers_of_tweets=1000,
                              hashtag=True,
                              from_date=None,
                              to_date=None,
                              save_to_file_switch=False):
        filename = query
        if hashtag:
            if not '#' in query:
                query = '#' + query
                filename = 'h_' + filename
            else:
                filename = 'h_' + filename[1:]
        else:
            filename = 'w_' + filename

        if not retweet:
            query += " -filter:retweets"
        try:
            collected_tweets = tweepy.Cursor(   self.api.search,
                                                q=query,
                                                tweet_mode="extended",
                                                lang=lang).items(numbers_of_tweets)
        except Exception as e:
            print(e)
            exit(-1)
        time_range = self.prepare_datetime(from_date,to_date)
        return self.data_to_file(filename,collected_tweets,time_range,save_to_file_switch)


    def get_tweets_from_user_timeline(self,
                                      username='',
                                      numbers_of_tweets=200,
                                      from_date=None,
                                      to_date=None,
                                      save_to_file_switch=False):
        try:
            collected_tweets = self.api.user_timeline(  screen_name=username,
                                                        tweet_mode='extended',
                                                        count=numbers_of_tweets)
        except Exception as e:
            print(e)
            exit(-1)

        filename = 'timeline'
        if username != '':
             filename = 'u_' + username
        time_range = self.prepare_datetime(from_date,to_date)
        return self.data_to_file(filename,collected_tweets,time_range,save_to_file_switch)


    def get_tweets_from_home_timeline(self,
                                      numbers_of_tweets=200,
                                      from_date=None,
                                      to_date=None,
                                      save_to_file_switch=False):
        try:
            collected_tweets = self.api.home_timeline(  tweet_mode='extended',
                                                        count=numbers_of_tweets)
        except Exception as e:
            print(e)
            exit(-1)

        time_range = self.prepare_datetime(from_date,to_date)
        return self.data_to_file('home_timeline',collected_tweets,time_range,save_to_file_switch)


    def data_to_file(self, filename, collected_tweets, time_range, save_to_file_switch):
        if (time_range[0] or time_range[1] ) is None:
            tweets_data = [[
                            '5', 
                            tweet.id,
                            tweet.created_at,
                            tweet.full_text,
                            tweet.author.screen_name,
                            tweet.source,
                            self.change_to_coord(tweet.user.location),
                            tweet.favorite_count,
                            tweet.retweet_count,
                            tweet.lang,
                            ''
                            ] for tweet in collected_tweets]
        else:
            tweets_data = []
            for tweet in collected_tweets:
                if tweet.created_at > time_range[0] and tweet.created_at < time_range[1]:
                    tweets_data.append( [
                                        '5',
                                        tweet.id,
                                        tweet.created_at,
                                        tweet.full_text,
                                        tweet.author.screen_name,
                                        tweet.source,
                                        self.change_to_coord(tweet.user.location),
                                        tweet.favorite_count,
                                        tweet.retweet_count,
                                        tweet.lang,
                                        ''
                                        ])

        twitter_df = pd.DataFrame(data=tweets_data, 
                                  columns=[
                                        'sentient',
                                        'id',
                                        'created_at',
                                        'text',
                                        'author',
                                        'source',
                                        'location',
                                        'favorite_count',
                                        'retweet_count',
                                        'lang',
                                        'vector'
                                        ])

        filename += '_'+datetime.now().strftime('%Y%m%d_%H%M%S')
        if save_to_file_switch:
            path_to_file = 'collected_data/clean/'
            if not os.path.exists( path_to_file ):
                os.makedirs(path_to_file)    
            try:
                twitter_df.to_excel(path_to_file + filename.lower()+'.xlsx',index=False)
                # twitter_df.to_csv(path_to_file + filename.lower()+'.csv',sep=';',index=False,encoding='utf-8')
                print('File: \'' + path_to_file + filename.lower() + '\' saved!')
            except Exception as e:
                print("Error! while saving file.")
                print(e)
                exit(0)
        else:
            return (twitter_df,filename)


    def prepare_datetime(self, from_date, to_date):
        if (from_date or to_date) is (None or ''):
            return (None,None)
        # else:
            # if isinstance(type(from_date), str):
        from_date = from_date.split('-')
        from_date = [int(x) for x in from_date]
        from_date = datetime(from_date[0],from_date[1],from_date[2]) #,to_date[3],to_date[4],to_date[5] # if HOUR-MIN-SEC
        to_date = to_date.split('-')
        to_date = [int(x) for x in to_date]
        to_date = datetime(to_date[0],to_date[1],to_date[2]+1) #,to_date[3],to_date[4],to_date[5] # if HOUR-MIN-SEC
        return (from_date,to_date)


    def create_coord_from_file(self,filename='config/polish_cities_coord.csv'):
        try:
            file = open(filename,"r")
        except Exception as e:
            print("Error! Cannot open file")
            print(e)
            exit(0)
        self.coordinates = {}

        for line in file:
            line = line.strip('\n').split(';')
            self.coordinates[ line[0] ] = ( line[1],line[2] )


    def change_to_coord(self, location):
        location = location.split(',')

        if location[0] in self.coordinates:
            return re.sub(r'\'|\(|\)','',str(self.coordinates[ location[0] ] ) )
        else:
            return 'None'
