import tweepy
import os

# Twitter APIキーを環境変数から取得
consumerKey = os.environ["TW_API_Key"]
consumerSecret = os.environ["TW_API_Key_Secret"]
accessToken = os.environ["TW_Access_Token"]
accessTokenSecret = os.environ["TW_Access_Token_Secret"]
bearerToken = os.environ["TW_Bearer_Token"]

# ポストを投稿する関数
def post(tweet):
    # tweepyクライアントを作成
    client = tweepy.Client(
        bearerToken,
        consumerKey,
        consumerSecret,
        accessToken,
        accessTokenSecret
    )

    # ポストを投稿
    client.create_tweet(text=tweet)
