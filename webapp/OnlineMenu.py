from src.TweetCollector import *
from src.Vectorization import *
from src.NetworkModel import *
from src.TweetAnalyzer import *

def twitter_flask(query, source, retweet, numbers_of_tweets, from_date, to_date):
    api = AuthTwitterUser()
    tt_collector = TweetCollector(api.api)

    if source == 'hashtag':
        df = tt_collector.get_tweets_from_topic(query=query,
                                                retweet=False,
                                                hashtag=True,
                                                numbers_of_tweets=numbers_of_tweets,
                                                from_date=from_date,
                                                to_date=to_date,
                                                )
    elif source == 'word':
        df = tt_collector.get_tweets_from_topic(query=query,
                                                retweet=retweet,
                                                hashtag=False,
                                                numbers_of_tweets=numbers_of_tweets,
                                                from_date=from_date,
                                                to_date=to_date
                                                )
    elif source == 'user':
        df = tt_collector.get_tweets_from_user_timeline(username=query,
                                                        numbers_of_tweets=numbers_of_tweets,
                                                        from_date=from_date,
                                                        to_date=to_date
                                                        )
    filename = ''
    if  df[0].shape[0]:
        vect = Vectorization()
        df = vect.df_vectorization(df)
        filename = df[1]
        mod = NetworkModel()
        mod.predict_tweets(df, 'config/model.h5',save_to_file_switch=True)

    return filename.lower(), df[0].shape[0]


def generate_raport(form, filename, path_to_file='collected_data/tagged/'):
    sentinent = []
    day_parts = []
    if form.data['positive']:
        sentinent.append(1)
    if form.data['negative']:
        sentinent.append(-1)
    if form.data['neutral']:
        sentinent.append(0)

    if form.data['morning']:
        day_parts.append('morning')
    if form.data['midday']:
        day_parts.append('midday')
    if form.data['afternoon']:
        day_parts.append('afternoon')
    if form.data['evening']:
        day_parts.append('evening')
    if form.data['night']:
        day_parts.append('night')

    if len(sentinent) == 0:
        sentinent = [1, -1, 0]
        
    if len(day_parts) == 0:
        day_parts = ['morning', 'midday', 'afternoon', 'evening', 'night']

    raport = TweetAnalyzer()
    df = pd.read_excel(path_to_file+filename+'.xlsx')
    data_from_raport = raport.analise(df,sentinent,day_parts)

    return data_from_raport
