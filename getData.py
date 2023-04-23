import tweepy
# from google.cloud import storage
import csv
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from datetime import datetime
import time as t

# 设置API密钥和密钥密码
api_key = 'SouuoOtKFhr36c9vCmBRI14tb'
api_secret = 'x9QhTxbBA3pc70AO7dRlbsUfNWkk3f9H2h0oKDBrRlVBVB9HxE'
access_token = '1579158480887463938-5235pDyEN1i68IhgXhmnvZHTX0pzlk'
access_secret = '12YZRR7kiCBCEK13D7fC4U3EGE0IOFtNU5PKoizit3OVn'

# 连接到Twitter API
auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_secret)
api = tweepy.API(auth)

until_date = '2023-04-22'
until_time = '23:59:59'

max_tweets = 200
query_date_time = datetime.strptime(until_date + ' ' + until_time, '%Y-%m-%d %H:%M:%S')
query_date_time_formatted = query_date_time.strftime('%Y-%m-%d_%H:%M:%S')

query_hashtags = []
# 'ClevelandCavaliers', 'NewYorkKnicks', 'Philadelphia76ers', 'BostonCeltics', 'AtlantaHawks','MilwaukeeBucks', 'MiamiHeat', 'BrooklynNets'
# '76ers', 'Nets', 'Celtics','Bucks', 'Cavaliers', 'Knicks', 'Heat', 'Hawks'
# 'Nuggets', 'Grizzles', 'Kings', 'Suns', 'Clippers','Warriors', 'Lakers', 'Timberwolves'
# 'PhoenixSuns', 'DenverNuggets', 'MemphisGrizzlies', 'SacramentoKings', 'LAClippers', 'GoldenStateWarriors', 'LosAngelesLakers', 'MinnesotaTimberwolves'

# Download the VADER lexicon data
nltk.download('vader_lexicon')

# Create a SentimentIntensityAnalyzer object
sia = SentimentIntensityAnalyzer()

for hashtag in query_hashtags:
    query = '#' + hashtag + ' until:' + query_date_time_formatted
    path = hashtag + '.csv'
    with open(path, 'a', encoding='utf-8', newline='') as f:
        csv_writer = csv.writer(f)
        # Write the header row
        # csv_writer.writerow(['Time', 'Tweet', 'Location', 'Favorite Count', 'Sentiment'])

        # 使用 Cursor 对象进行分页查询
        sum = 0
        try:
            print('Now print: ' + hashtag)
            for tweet in tweepy.Cursor(api.search_tweets, q=query, count=max_tweets).items():
                time = tweet.created_at.strftime('%Y-%m-%d %H:%M:%S')
                text = tweet.text
                if tweet.place is not None:
                    location = tweet.place.full_name + ', ' + tweet.place.country
                else:
                    location = 'No location available.'
                favorite_count = tweet.favorite_count

                # 分析推文的情感
                sentiment_scores = sia.polarity_scores(text)
                sentiment = 0  # 中性情感
                if sentiment_scores['pos'] > sentiment_scores['neg']:
                    sentiment = 1  # 积极情感
                elif sentiment_scores['pos'] < sentiment_scores['neg']:
                    sentiment = -1  # 消极情感

                # 将推文数据作为一行写入 CSV 文件
                csv_writer.writerow([hashtag, time, text, location, favorite_count, sentiment])
                sum += 1

            print(sum)
        except Exception as e:
            print(e)
            if '429' in str(e):
                print('Rate limit exceeded. Waiting for 15 minutes...')
                t.sleep(15 * 60)  # 等待 15 分钟
                continue


# 上传文件到Google Cloud Storage
# storage_client = storage.Client()
# bucket_name = '6893_data_wp2297'
# bucket = storage_client.bucket(bucket_name)
# blob = bucket.blob('stream.txt')
# blob.upload_from_filename('stream.txt')

