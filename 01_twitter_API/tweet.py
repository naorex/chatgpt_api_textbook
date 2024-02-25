import gpt_api
import twitter_api

# ChatGPTからツイート内容を取得
tweet = gpt_api.make_tweet()
print(tweet)

# Twitterにツイートを投稿
# 2024/1/20 UnAuthorizedErrorが出るのでコメントオフ
# twitter_api.post(tweet)
