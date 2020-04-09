# -*- coding: utf-8 -*-
import tweepy

class AuthTwitterUser():
    def __init__(self,filename='config/credential.txt'):
        self.auth_value = { 'consumer_key':'',
                            'consumer_secret' : '',
                            'access_token' : '',
                            'access_token_secret' : ''}
        self.get_keys_from_file(filename)
        self.api = self.auth_user()

# confusion matrix coincidence
    def auth_user(self):
        if '' in self.auth_value.values():
            return None

        auth = tweepy.OAuthHandler( self.auth_value['consumer_key'],
                                    self.auth_value['consumer_secret'])
                                        
        auth.set_access_token( self.auth_value['access_token'],
                               self.auth_value['access_token_secret'])

        api = tweepy.API(auth, wait_on_rate_limit=True)
        return api


    def get_keys_from_file(self, filename):
        try:
            file = open(filename,'r')
        except Exception as e:
            print("Error! Cannot open file")
            print(e)
            exit(0)

        for line in file:
            line =  line.split(' ')
            if 'consumer_key' == line[0]:
                self.auth_value['consumer_key'] = line[2].strip('\n')
            if 'consumer_secret' == line[0]:
                self.auth_value['consumer_secret'] = line[2].strip('\n')
            if 'access_token' == line[0]:
                self.auth_value['access_token'] = line[2].strip('\n')
            if 'access_token_secret' == line[0]:
                self.auth_value['access_token_secret'] = line[2].strip('\n')

        file.close()
