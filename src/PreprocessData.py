# -*- coding: utf-8 -*-
from string import punctuation
import re
import os
import string
import pandas as pd
try:
    import morfeusz2
except Exception as e:
    print(e,'\nVisit http://morfeusz.sgjp.pl/ for instruction')
    exit(0)


class PreprocessData():
    def __init__(self, filename='config/stopwords.txt'):
        self.prepare_stopwords(filename)


    def clean_data(self,tweet):
        self.tweet = tweet.lower()
        self.emoji()
        self.remove_hashtag_mentions_urls()
        self.remove_punctuation()
        self.remove_numbers()
        self.tokenization()
        self.lemmatization()
        self.remove_stopwords()
        return self.tweet

    def prepare_stopwords(self, filename):
        try:
            file = open(filename,'r')
        except Exception as e:
            print("Error! Cannot open file")
            print(e)
            exit(0)

        self.stopwords = []
        for line in file:
            self.stopwords.append( line.strip('\n') )
        file.close()


    def remove_hashtag_mentions_urls(self):
        self.tweet = re.sub(r'#\w+', 'HASHTAG', self.tweet)
        self.tweet = re.sub(r'@\w+', 'MENTION', self.tweet)
        self.tweet = re.sub(r'[^\s]+[\w]\.[^\s]+[\w]', 'URL', self.tweet)


    def remove_punctuation(self):
        self.tweet = re.sub('['+punctuation+']', '', self.tweet)


    def remove_numbers(self):
        self.tweet = re.sub(r'\d+', '', self.tweet)


    def tokenization(self):
        self.tweet = self.tweet.split()


    def emoji(self):
        # https://en.wikipedia.org/wiki/Emoticons_(Unicode_block)
        positive_symbols = re.compile('['
                u'\U0001F600-\U0001F60F'
                u'\U0001F617-\U0001F61D'
                u'\U0001F638-\U0001F63D'
                u'\U0001F493-\U0001F49F'
                u'\U0001F642' u'\U0001F643' 
                u'\U0001F642' u'\U0001F64B'
                u'\U0001F44C' u'\U0001F44D'
                u'\U00002764'
                ']+', flags=re.UNICODE)
        
        negative_symbols = re.compile('['
                u'\U0001F610-\U0001F616'
                u'\U0001F61E-\U0001F61F'
                u'\U0001F620-\U0001F62F'
                u'\U0001F630-\U0001F637'
                u'\U0001F63D-\U0001F63F'
                u'\U0001F640' u'\U0001F641'
                u'\U0001F644' u'\U0001F64D'
                u'\U0001F64E' u'\U0001F44E'
                ']+', flags=re.UNICODE)

        # https://en.wikipedia.org/wiki/List_of_emoticons
        positive_icon = [':‑)', ':)', ':-]', ':]', ':-3', ':3', ':->', ':>', '8-)', '8)',
                        ':-}', ':}', ':o)', ':c)', ':^)','=]','=)', ':-))', ':‑d', ':d', 
                        '8‑d', '8d', 'x‑d', 'xd', '=d', '=3', 'b^d',  ';)',  ':p',]
        
        negative_icon = [':‑(', ':(', ':‑c', ':c',':‑<', ':<', ':‑[', ':[',':-||', '>:[', ':o',
                        ':{', ':@', '>:(', 'd‑\':', 'd:<', 'd:', 'd8', 'd;','d=', 'dx', ';(']

        for sign in positive_icon:
            if sign in self.tweet:
                self.tweet = self.tweet.replace(sign,' POSITIVE ')
        
        for sign in negative_icon:
            if sign in self.tweet:
                self.tweet = self.tweet.replace(sign,' NEGATIVE ')

        self.tweet = positive_symbols.sub(r' POSITIVE ', self.tweet)
        self.tweet = negative_symbols.sub(r' NEGATIVE ', self.tweet)
        
        # https://en.wikipedia.org/wiki/Plane_(Unicode)
        # https://www.utf8-chartable.de/unicode-utf8-table.pl?start=8192&number=128&names=-&utf8=string-literal
        symbol_to_del = re.compile('[' u'\U00010000-\U0001FAFF' 
                                       u'\U000024C2-\U0001F251'
                                       u'\U00002000-\U0000207F'
                                    ']+', flags=re.UNICODE)

        self.tweet = symbol_to_del.sub(r'', self.tweet)


    def remove_stopwords(self):
        for word in self.stopwords:
            for token in self.tweet:
                if word == token:
                    self.tweet.remove(token)


    def lemmatization(self):
        morf = morfeusz2.Morfeusz(generate=False)
        analysis = []
        for token in self.tweet:
            word = morf.analyse(token)[0]           # most probable occurrence
            
            if word[2][1] == 'URL':
                analysis.append(word[2][1])
            elif word[2][1] == 'HASHTAG':
                analysis.append(word[2][1])
            elif word[2][1] == 'POSITIVE':
                analysis.append(word[2][1])
            elif word[2][1] == 'NEGATIVE':
                analysis.append(word[2][1])
            elif word[2][1] == 'MENTION':
                analysis.append(word[2][1])


            if 'perf' in word[2][2]:                # verb (czaswonik)
                analysis.append(re.sub(r':\w+', '', word[2][1] ) )
            elif 'adj' in word[2][2]:               # adjective (przymiotnik)
                analysis.append(re.sub(r':\w+', '', word[2][1] ) )
            elif 'adv' in word[2][2]:               # adverb (przysłówek)
                analysis.append(re.sub(r':\w+', '', word[2][1] ) )
            elif 'subst' in word[2][2]:             # substantive (rzeczownik)
                if  word[2][3]:
                    if word[2][1] == 'wiktor':     # morfeusz2 treat its like 'nazwa_pospolita' 
                        continue
                    if word[2][3][0] != 'nazwa_pospolita':
                        continue
                analysis.append( re.sub(r':\w+', '', word[2][1] ) )
        self.tweet = analysis

#człon_nazwy_organizacji