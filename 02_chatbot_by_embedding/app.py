import os
from openai import OpenAI

client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
)

# 最初にメッセージを表示する
print("質問を入力してください")

conversation_history = []

while True:
    # ユーザーの入力した文字を変数「user_input」に格納
    user_input = input()

    # ユーザーの入力した文字が「exit」の場合はループを抜ける
    if user_input == "exit":
        break

    # ユーザーの質問を会話の履歴に追加
    conversation_history.append({"role": "user", "content": user_input})

    # ChatGPTにリクエストを送信し、応答を取得
    response = client.chat.completions.create(
        model = "gpt-3.5-turbo",
        temperature = 0.5,
        messages = conversation_history,
    )

    # ChatGPTの回答を会話履歴に追加
    chatgpt_response = response.choices[0].message.content
    conversation_history.append({"role": "assistant", "content": chatgpt_response})

    print("ChatGPT:", chatgpt_response)
