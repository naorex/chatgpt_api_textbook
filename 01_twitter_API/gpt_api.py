from openai import OpenAI
import os

client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
)

# ChatGPTにリクエストを送信する関数
def make_tweet():
    # ChatGPTへの命令文を設定
    request = "あなたはPythonを学習し始めた女子大学生です。\
               Twitterに投稿するツイートを140文字以内で作成してください。\
               ツイートを作成する際は、入力した例文を参考に、新たな文章を作成してください。\
               あなたは非常に楽観的な性格で、語尾は「なのだ」で終える口癖があります。"
    # 例文として与える投稿文を設定
    tweet1 = "Pythonを自分のパソコンに導入するの結構大変だった～\
              Hello Worldとか書く前以前の問題すぎん？\n\n"
    tweet2 = "やっとPython導入できた～これから色々作ってみたいけど、まずは何からやろうかな\n\n"

    # 文を連結して1つの命令文にする
    content = tweet1 + tweet2

    # ChatGPTにリクエストを送信
    response = client.chat.completions.create(
        model = "gpt-3.5-turbo",
        temperature = 0.5,
        messages = [
            {"role": "system", "content": request},
            {"role": "user", "content": content},
        ],
    )

    res = response.choices[0].message.content

    # 投稿文の内容を返却
    return res
