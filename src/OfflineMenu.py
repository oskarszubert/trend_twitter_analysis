# -*- coding: utf-8 -*-
import shutil
from TweetCollector import *
from SiteScrapper import *
from PreprocessData import *
from CreateVocabulary import *
from Vectorization import *
from NetworkModel import *
from TweetAnalyzer import *
import pandas as pd

class OfflineMenu():
    @staticmethod
    def twitter_ui(save_to_file_switch):
        api = AuthTwitterUser()
        tt_collector = TweetCollector(api.api)
        try:
            tt_source = int( input('------------Collect tweets from: \
                            \n\t[ 1 ]  #hashtag.\
                            \n\t[ 2 ]  word.\
                            \n\t[ 3 ]  user.\
                            \n\t[ 4 ]  your timeline.\
                            \n\t ------------------------------- \
                            \n\t[ 0 ] Exit \
                            \nYour choice: ')
                            )

        except Exception:
            print('*** Something went wrong! ***')
            exit(-1)

        if tt_source not in range(1,5):
            print('*** Something went wrong! ***')
            exit()

        print('*** Type period of searching. If FULL posible time press [ENTER] *** ')
        print('*** Date format: YEAR-MONTH-DAY *** ')
        from_date = input('From date: ')
        to_date = input('To date: ')
        print('--------------------')
        try:
            numbers_of_tweets = int(input('How many tweets:' ))
        except Exception:
            print('*** Something went wrong! but ok lets be 1000 ***')
            numbers_of_tweets = 1000

        if tt_source in range(1,3):
            retweet = input('Include retweets: [y/n]: ')
            retweet = True if retweet=='y' else False

            if tt_source ==  1:
                query = input('#hastag: ')
            elif tt_source ==  2:
                query = input('Word: ')

            df = tt_collector.get_tweets_from_topic(    query,
                                                        retweet=retweet,
                                                        hashtag=False,
                                                        numbers_of_tweets=numbers_of_tweets,
                                                        from_date=from_date,
                                                        to_date=to_date,
                                                        save_to_file_switch=save_to_file_switch
                                                    )

        elif tt_source ==  3:
            username = input('User name: ')
            df = tt_collector.get_tweets_from_user_timeline( username=username,
                                                        numbers_of_tweets=numbers_of_tweets,
                                                        from_date=from_date,
                                                        to_date=to_date,
                                                        save_to_file_switch=save_to_file_switch
                                                    )
        elif tt_source ==  4:
            df = tt_collector.get_tweets_from_home_timeline( numbers_of_tweets=numbers_of_tweets,
                                                        from_date=from_date,
                                                        to_date=to_date,
                                                        save_to_file_switch=save_to_file_switch
                                                    )
        return df


    # @staticmethod
    def create_vocab_ui(self):
        try:
            what_vocab_create = int( input('------------Create Vocabulary: \
                            \n\t[ 1 ]  NEW  [previous will be deleted].\
                            \n\t[ 2 ]  Append existing.\
                            \n\t path to vocabulary: config\\vocabulary\\ \
                            \n\t ------------------------------- \
                            \n\t[ 0 ] Exit \
                            \nYour choice: ')
                            )

        except Exception:
            print('*** Something went wrong! ***')
            exit(-1)

        if what_vocab_create not in range(1,3):
            print('*** Something went wrong! ***')
            exit()

        filename = self.get_file_from_dir('model_train_data/tagged/')

        try:
            vocab_size = int(input('Size of Vocabulary: '))
        except Exception:
            print('*** Something went wrong! ***')
            exit(-1)

        vocab = CreateVocabulary()
        if what_vocab_create == 1:
            path = 'config/vocabulary'
            shutil.rmtree(path, ignore_errors=True)

        vocab.create(filename=filename,size=vocab_size)


    @staticmethod
    def scrapper_ui():
        scrapper = SiteScrapper()
        try:
            site_source = int(input('------------Scrap from: \
                                        \n\t[ 1 ]  ceneo.pl/\
                                        \n\t[ 2 ]  yelp.pl\
                                        \n\t ------------------------------- \
                                        \n\t[ 0 ] Exit \
                                        \nYour choice: '))
        except Exception:
            print('*** Something went wrong! ***')
            exit(-1)

        if site_source not in range(1,3):
            print('*** Something went wrong! ***')
            exit()

        try:
            single_or_url = int(input('------------How many : \
                                        \n\t[ 1 ]  single url\
                                        \n\t[ 2 ]  from urls in file\
                                        \n\t ------------------------------- \
                                        \n\t[ 0 ] Exit \
                                        \nYour choice: '))
        except Exception:
            print('*** Something went wrong! ***')
            exit(-1)

        if single_or_url not in range(1,3) :
            print('*** Something went wrong! ***')
            exit()

        if single_or_url == 1:
            single_url =  input('Type your url: ')

        if site_source == 1:
            if single_or_url == 1:
                scrapper.scrape_ceneo_url(single_url)
            elif single_or_url == 2:
                print('ulr(s) should be in: model_train_data/urls/ceneo_urls.txt')
                scrapper.scrape_multiple_ceneo_urls()

        elif site_source == 2:
            if single_or_url == 1:
                scrapper.scrape_yelp_url(single_url)
            elif single_or_url == 2:
                print('ulr(s) should be in: model_train_data/urls/yelp_urls.txt')
                scrapper.scrape_multiple_yelp_urls()


    @staticmethod
    def clean_single_sentence_ui():
        cleaner = PreprocessData()
        sentence = input('Sentence: ')
        print( cleaner.clean_data(sentence) )


    def get_dataframe(self):
        try:
            df_from = int(input('------------Get data from: \
                                        \n\t[ 1 ]  from Twitter\
                                        \n\t[ 2 ]  from directory: \'collected_data/clean\'\
                                        \n\t ------------------------------- \
                                        \n\t[ 0 ] Exit \
                                        \nYour choice: '))
        except Exception:
            print('*** Something went wrong! ***')
            exit(-1)

        if df_from not in range(1,3):
            print('*** Something went wrong! ***')
            exit()

        if df_from == 1:
            df = self.twitter_ui(save_to_file_switch=False)
        elif df_from == 2:
            path_to_files = 'collected_data/clean/'
            selected_file = self.get_file_from_dir(path_to_files)
            df_from_file = pd.read_excel( path_to_files + selected_file )
            
            df = [df_from_file, selected_file.split('.')[0]]
        return df


    @staticmethod
    def get_sentinent_option():
        print('------------Look for Tweets : \
            \n\t[ 1 ]  ALL.\
            \n\t[ 2 ]  POSITIVE.\
            \n\t[ 3 ]  NEUTRAL.\
            \n\t[ 4 ]  NEGATIVE.\
            \n\t ------------------------------- \
            \n\t[ 0 ] end'
            )
        sentinent = []
        while True:
            try:
                sentinent_choice = int(input('Your choice: '))
            except Exception:
                print('*** Something went wrong! ***')
                exit(-1)

            print('Add more option? ',end='')
            if sentinent_choice not in range(4):
                print('*** Something went wrong! ***')
                exit()

            if sentinent_choice == 0:
                if len(sentinent) == 0:
                    sentinent = [-1,0,1]
                break
            elif sentinent_choice == 1:
                sentinent = [-1,0,1]
                break
            if sentinent_choice == 2:
                if 1 in sentinent:
                    continue
                sentinent.append(1)
            elif sentinent_choice == 3:
                if 0 in sentinent:
                    continue
                sentinent.append(0)
            elif sentinent_choice == 4:
                if 0 in sentinent:
                    continue
                sentinent.append(-1)

            if len(sentinent) == 3:
                break
        return sentinent


    @staticmethod
    def get_part_day_option():
        print('------------Look for Tweets added: \
            \n\t[ 1 ]  ALL day.\
            \n\t[ 2 ]  morning.\
            \n\t[ 3 ]  midday.\
            \n\t[ 4 ]  afternoon.\
            \n\t[ 5 ]  evening.\
            \n\t[ 6 ]  night.\
            \n\t ------------------------------- \
            \n\t[ 0 ] end'
            )
            
        day_parts = []
        while True:
            try:
                dayparts_choice = int(input('Your choice: '))
            except Exception:
                print('*** Something went wrong! ***')
                exit(-1)
            print('Add more option? ',end='')

            if dayparts_choice not in range(7):
                print('*** Something went wrong! ***')
                exit()

            if dayparts_choice == 0:
                if len(day_parts) == 0:
                    day_parts = ['morning', 'midday', 'afternoon', 'evening', 'night']
                break
            elif dayparts_choice == 1:
                day_parts = ['morning', 'midday', 'afternoon', 'evening', 'night']
                break
            elif dayparts_choice == 2:
                if 'morning' in day_parts:
                    continue
                day_parts.append('morning')
            elif dayparts_choice == 3:
                if 'midday' in day_parts:
                    continue
                day_parts.append('midday')
            elif dayparts_choice == 4:
                if 'afternoon' in day_parts:
                    continue
                day_parts.append('afternoon')
            elif dayparts_choice == 5:
                if 'evening' in day_parts:
                    continue
                day_parts.append('evening')
            elif dayparts_choice == 6:
                if 'night' in day_parts:
                    continue
                day_parts.append('night')

            if len(day_parts) == 5:
                break
        return day_parts


    def predic_and_raport_ui(self):
        sentinent = self.get_sentinent_option()
        day_parts = self.get_part_day_option()
        df = self.get_dataframe()
        self.network_model(df, sentinent, day_parts)


    @staticmethod
    def network_model(df,sentinent,day_parts):
        vect = Vectorization()
        df = vect.df_vectorization(df)
        mod = NetworkModel()
        df = mod.predict_tweets(df, 'config/model.h5',save_to_file_switch=False)

        raport = TweetAnalyzer()

        data_from_raport = raport.analise(df,sentinent,day_parts)
        raport.save_raport_to_file(data_from_raport)


    def create_dataset_ui(self,path='model_train_data/tagged/'):
        model_obj = NetworkModel()
        file_list = os.listdir( path )
        dataset_df = pd.DataFrame()

        choice_counter = 0
        add_file = True

        print('------------Choose file from dir: ')
        for i in range(len(file_list)):
            print( '\t[',i,']',file_list[i])

        while add_file:
            try:
                file_choice = int(input('Your choice: '))
                choice_counter += 1
            except Exception:
                print('*** Something went wrong! ***')
                exit(-1)

            if file_choice not in range(len(file_list)):
                print('*** Something went wrong! ***')
                exit()
            filename = file_list[ file_choice ]

            df = pd.read_excel(path + filename)
            try:
                df = df.drop(columns=['id',
                                      'created_at',
                                      'author',
                                      'favorite_count',
                                      'retweet_count',
                                      'lang',
                                      'source',
                                      'location'
                                      ])
            except:
                pass
            dataset_df = dataset_df.append(df, ignore_index=True)
            print('Read file with number of rows: ', dataset_df.shape[0])

            try:
                create_test_dataset = input('Create TEST dataset? [y/n]: ')
            except Exception:
                print('*** Something went wrong! ***')
                exit(-1)

            if create_test_dataset == 'y':
                try:
                    percent = int(input('Number of test data[0-100%]: '))
                except Exception:
                    print('*** Something went wrong! ***')
                    exit(-1)
                dataset_df = model_obj.save_dataset_to_dir(percent, df=dataset_df)
                create_test_dataset = None

            try:
                add_file = input('Add more file to TRAIN dataset? [y/n]: ')
            except Exception:
                print('*** Something went wrong! ***')
                exit(-1)
            add_file = True if add_file=='y' else False

        dataset_df = shuffle(dataset_df)
        dataset_df.to_excel('model_train_data/dataset/train_dataset.xlsx',index=False)
        
        try:
            do_vectorization = input('Vectorize datasets? [y/n]: ')
        except Exception:
            print('*** Something went wrong! ***')
            exit(-1)

        if do_vectorization == 'y':
            self.vectorize_ui()


    @staticmethod
    def vectorize_ui():
        path_to_file = 'model_train_data/dataset/'
        vect = Vectorization()
        try:
            algo_choice = int(input('------------Choose algorithm: \
                                        \n\t[ 1 ]  TF-IDF\
                                        \n\t[ 2 ]  Term frequency\
                                        \n\t[ 3 ]  Bag of Words\
                                        \n\t[ 4 ]  Binary\
                                        \n\t ------------------------------- \
                                        \n\t[ 0 ] Exit \
                                        \nYour choice: '))
        except Exception:
            print('*** Something went wrong! ***')
            algo_choice = 'tf-idf'
        if algo_choice not in range(1,5):
            print('*** Something went wrong! ***')
            exit()
        elif algo_choice == 1:
            algo = 'tf-idf'
        elif algo_choice == 2:
            algo = 'tf'
        elif algo_choice == 3:
            algo = 'bow'
        elif algo_choice == 4:
            algo = 'binary'

        vect.df_vectorization_from_file(read_file = 'train_dataset.xlsx', path_to_file=path_to_file,algo=algo)
        vect.df_vectorization_from_file(read_file = 'test_dataset.xlsx', path_to_file=path_to_file,algo=algo)



    @staticmethod
    def vectorize_twitter_test_ui():
        path_to_file = 'model_train_data/dataset/'
        vect = Vectorization()
        try:
            algo_choice = int(input('------------Choose algorithm: \
                                        \n\t[ 1 ]  TF-IDF\
                                        \n\t[ 2 ]  Term frequency\
                                        \n\t[ 3 ]  Bag of Words\
                                        \n\t[ 4 ]  Binary\
                                        \n\t ------------------------------- \
                                        \n\t[ 0 ] Exit \
                                        \nYour choice: '))
        except Exception:
            print('*** Something went wrong! ***')
            algo_choice = 'tf-idf'
        if algo_choice not in range(1,5):
            print('*** Something went wrong! ***')
            exit()
        elif algo_choice == 1:
            algo = 'tf-idf'
        elif algo_choice == 2:
            algo = 'tf'
        elif algo_choice == 3:
            algo = 'bow'
        elif algo_choice == 4:
            algo = 'binary'

        vect.df_vectorization_twitter_test(algo=algo)


    @staticmethod
    def get_file_from_dir(path):
        file_list = os.listdir( path )
        print('------------Choose file from dir: ')
        for i in range(len(file_list)):
            print( '\t[',i,']',file_list[i])

        try:
            file_choice = int(input('Your choice: '))
        except Exception:
            print('*** Something went wrong! ***')
            exit(-1)

        if file_choice not in range(len(file_list)):
            print('*** Something went wrong! ***')
            exit()
        filename = file_list[ file_choice ]
        return filename


    def create_model_ui(self):
        layers = []
        try:
            epochs = int(input('How many epochs: '))
        except Exception:
                print('*** Something went wrong! let be 60 epochs***')
                epochs = 60
        try:
            vocabulary_size = int(input('Vocabulary size: '))
        except Exception:
                print('*** Something went wrong! ***')
                vocabulary_size = 300

        while True:
            try:
                print('Number of neurons in {} layer: '.format( len(layers) + 1 ), end='')
                neurons = int(input())
                if neurons == 0:
                    break
                layers.append(neurons)
            except Exception:
                print('*** Something went wrong! ***')

        model = NetworkModel()
        model.create_model(vocabulary_size, layers, epochs)



    def model_test_ui(self):
        model = NetworkModel()
        epochs = 50


# 1 test:
        # vocabulary_size = 100
        # for i in [2,5,7,10,12,15,20,30]:
        #     model.create_model(vocabulary_size, [i], epochs)


# # 2 test:
        # vocabulary_size = 300 #10,30,50,70,100,150,300
        # model.create_model(vocabulary_size, [20], epochs)
        # model.create_confusion_matrix(model_name='config/model.h5',vocabulary_size=vocabulary_size)

# 3 test:
        # vocabulary_size = 70
        # for i in [5,10,20,50,100]:

# # 4 test:
        # model.create_model(70, [20], 50)
# # 5 test:
#         vocabulary_size = 70
#         model.create_model(vocabulary_size, [12,3], 50)
#         model.create_model(vocabulary_size, [12,5], 50)
#         model.create_model(vocabulary_size, [20,12], 50)
#         model.create_model(vocabulary_size, [50,20], 50)