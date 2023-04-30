import tweepy
from google.cloud import storage

# 设置API密钥和密钥密码
api_key = 'SouuoOtKFhr36c9vCmBRI14tb'
api_secret = 'x9QhTxbBA3pc70AO7dRlbsUfNWkk3f9H2h0oKDBrRlVBVB9HxE'
access_token = '1579158480887463938-5235pDyEN1i68IhgXhmnvZHTX0pzlk'
access_secret = '12YZRR7kiCBCEK13D7fC4U3EGE0IOFtNU5PKoizit3OVn'

# 连接到Twitter API
auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_secret)
api = tweepy.API(auth)

# 查询包含特定hashtags的推文
until_date = '2023-04-21'
max_tweets = 100
query = '#championsleague OR #milan OR #Inter OR #ManCity OR #FCBayern' + ' until:' + until_date
tweets = api.search_tweets(q=query, count=max_tweets)

sum = 0
# 将推文保存到文件中
with open('stream.txt', 'w', encoding='utf-8') as f:
    for tweet in tweets:
        f.write(tweet.created_at.strftime('%Y-%m-%d %H:%M:%S'))
        f.write('\n')
        f.write(tweet.text)
        f.write('\n')
        if tweet.place is not None:
            f.write('Location: ' + tweet.place.full_name + ', ' + tweet.place.country)
            f.write('\n')
        else:
            f.write('No location available.')
            f.write('\n')
        f.write('Favorite count: ' + str(tweet.favorite_count))
        f.write('\n\n')
        sum += 1
print(sum)

# 上传文件到Google Cloud Storage
storage_client = storage.Client()
bucket_name = '6893_data_wp2297'
bucket = storage_client.bucket(bucket_name)
blob = bucket.blob('stream.txt')
blob.upload_from_filename('stream.txt')

