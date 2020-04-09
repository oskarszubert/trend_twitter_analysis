import pandas as pd
from datetime import datetime
from datetime import time
import collections

class TweetAnalyzer():
    def __init__(self):
        self.morning = [time(5, 0, 0), time(9, 59, 59) ]
        self.midday = [time(10, 0, 0), time(13,59, 59) ]
        self.afternoon = [time(14, 0, 0 ), time(17, 59, 59) ]
        self.evening = [time(18, 0, 0), time(23, 59, 59) ]
        self.night = [time(0, 0, 0), time(4, 59, 59) ]
        
        self.source_dict = {'Twitter for iPhone': 0, 
                            'Twitter for Android': 0, 
                            'Twitter Web App': 0,
                            'TweetDeck': 0, 
                            'Twitter Web Client': 0,
                            'OTHER' : 0
        }

    def analise(self,
                df,
                sentinent,
                day_parts):

        tweet_counter = 0
        location_counter = 0

        location_dict = {}
        day_parts_counter_dict = {'morning':0,'midday':0,'afternoon':0,'evening':0,'night':0}
        time_period = []

        date_switch = True
        for i in range( df.shape[0] ):
            if df.loc[i,'sentient'] in sentinent:
                created_at = df.loc[i,'created_at'].to_pydatetime()     # convert to datetime format
                part_of_day = self.get_part_of_day(created_at.time())
                if part_of_day in day_parts:
                    tweet_counter += 1
                    if date_switch:
                        time_period.append( created_at )
                        time_period.append( created_at )
                        date_switch = False

                    time_period[0] = created_at
                    
                    location = df.loc[i,'location']
                    if df.loc[i,'location'] != 'None':
                        location_counter += 1
                        if location in location_dict:
                            location_dict[location] += 1
                        else:
                            location_dict[location] = 1

                    source = df.loc[i,'source']
                    if source in self.source_dict:
                        self.source_dict[source] += 1
                    else:
                        self.source_dict['OTHER'] += 1
                        # self.source_dict[source] = 1 # just in case to include all names of other apps

                    if part_of_day in day_parts_counter_dict:
                        day_parts_counter_dict[part_of_day] += 1
                    else:
                        day_parts_counter_dict[part_of_day] = 1

        day_parts_counter_dict = collections.OrderedDict(sorted(day_parts_counter_dict.items()))
        day_parts_counter_dict = list(day_parts_counter_dict.items())
        self.source_dict = list(self.source_dict.items())
        location_dict = list(location_dict.items())
        
        location_list = []
        for loc in location_dict:
            tmp = [ float(loc[0][:5]), float(loc[0][6:]) , loc[1]  ]
            location_list.append(tmp)

        return tweet_counter, time_period, self.source_dict, day_parts_counter_dict, location_counter, location_list


    def get_part_of_day(self, tweet_time):
        if self.morning[0] <= tweet_time <= self.morning[1]:
            return 'morning'
        elif self.midday[0] <= tweet_time <= self.midday[1]:
            return 'midday'
        elif self.afternoon[0] <= tweet_time <= self.afternoon[1]:
            return 'afternoon'
        elif self.evening[0] <= tweet_time <= self.evening[1]:
            return 'evening'
        elif self.night[0] <= tweet_time <= self.night[1]:
            return 'night'


    def save_raport_to_file(self, data_from_raport):
        print('\nFound: ',data_from_raport[0],' tweets.')

        print('\nFrom date: ',str(data_from_raport[1][0]),'to date: ',str(data_from_raport[1][1]) )

        print('\nTweet from device: ')
        for device in data_from_raport[2]:
            print('\t',device, str((device[1]/data_from_raport[0])*100))

        print('\nTweet on Parts Of a day')
        for part in data_from_raport[3]:
            print('\t',part, str((part[1]/data_from_raport[0])*100))

        print('\n',data_from_raport[4], 'tweets with location.')
        if data_from_raport[5]:
            print('User location: ')
            for coord in data_from_raport[5]:
                print('\t',coord[0], coord[1])
