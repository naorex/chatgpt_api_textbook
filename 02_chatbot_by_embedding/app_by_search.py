import os
from openai import OpenAI
from search import answer_question

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

    # 別の関数から回答を取得
    answer = answer_question(user_input, conversation_history)

    # ChatGPTの回答を会話履歴に追加
    conversation_history.append({"role": "assistant", "content": answer})

    print("ChatGPT:", answer)
