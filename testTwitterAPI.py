# 本地版本
import tweepy

# 设置API密钥和密钥密码
api_key = 'SouuoOtKFhr36c9vCmBRI14tb'
api_secret = 'x9QhTxbBA3pc70AO7dRlbsUfNWkk3f9H2h0oKDBrRlVBVB9HxE'
access_token = '1579158480887463938-5235pDyEN1i68IhgXhmnvZHTX0pzlk'
access_secret = '12YZRR7kiCBCEK13D7fC4U3EGE0IOFtNU5PKoizit3OVn'

# 连接到Twitter API
auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_secret)
api = tweepy.API(auth)

# 查询包含特定hashtags的推文
query = '#machinelearning'
tweets = api.search_tweets(q=query, count=10)

# 打印查询结果和地理位置信息
for tweet in tweets:
    print(tweet.created_at, tweet.text)
    if tweet.place:
        print(tweet.place.full_name)
    else:
        print("No location available")