import pandas as pd
import numpy as np
import os
from openai import OpenAI
from scipy.spatial.distance import cosine


def create_context(question, df, max_len=1800):
    """
    質問と学習データを比較して、コンテキストを作成する関数
    """

    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
    )

    # 質問をベクトル化
    model = "text-embedding-3-small"
    q_embeddings = client.embeddings.create(input=question,
                                            model=model).data[0].embedding

    # q_embeddingsを１次配列に変換
    np_array = np.array(q_embeddings)
    flat_array = np_array.flatten()

    # 文字列を数値リストに変換する関数
    def convert_string_to_list(str_emb):
        # 文字列をカンマで分割し、数値に変換
        return [float(num) for num in str_emb.strip('[]').split(',')]

    # embeddings列の各要素を数値リストに変換
    df['embeddings'] = df['embeddings'].apply(convert_string_to_list)



    # 質問と学習データと比較してコサイン類似度を計算し、
    # 「distances」という列に類似度を格納
    df['distances'] = df['embeddings'].apply(lambda x: cosine(np.squeeze(flat_array), np.squeeze(np.array(x))))

    # コンテキストを格納するためのリスト
    returns = []
    # コンテキストの現在の長さ
    cur_len = 0

    # 学習データを類似度順にソートし、トークン数の上限までコンテキストに
    # 追加する
    for _, row in df.sort_values('distances', ascending=True).iterrows():
        # テキストの長さを現在の長さに加える
        cur_len += row['n_tokens'] + 4

        # テキストが長すぎる場合はループを終了
        if cur_len > max_len:
            break

        # コンテキストのリストにテキストを追加する
        returns.append(row["text"])

    # コンテキストを結合して返す
    return "\n\n###\n\n".join(returns)


def answer_question(question, conversation_history):
    """
    コンテキストに基づいて質問に答える関数
    """

    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
    )

    # 学習データを読み込む
    df = pd.read_csv('embeddings.csv', encoding="utf-8")

    # 質問と学習データを比較してコンテキストを作成
    context = create_context(question, df, max_len=200)
    # プロンプトを作成し、会話の履歴に追加
    prompt = f"あなたはとあるホテルのスタッフです。コンテキストに基づいて、お客様からの質問に丁寧に答えてください。コンテキストが質問に対して回答できない場合は「わかりません」と答えてください。\n\nコンテキスト: {context}\n\n---\n\n質問: {question}\n回答:"
    conversation_history.append({"role": "user", "content": prompt})

    try:
        # ChatGPTからの回答を生成
        response = client.chat.completions.create(
            model = "gpt-3.5-turbo",
            temperature = 0.5,
            messages = conversation_history,
        )

        # ChatGPTからの回答を返す
        return response.choices[0].message.content.strip()

    except Exception as e:
        # エラーが発生した場合は空の文字列を返す
        print(e)
        return ""
