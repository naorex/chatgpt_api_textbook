import pandas as pd
import re

def remove_newlines(text):
    '''
    文字列内の改行と空白を削除する関数
    '''
    text = re.sub(r'\n', ' ', text)
    text = re.sub(r' +', ' ', text)
    return text

def text_to_df(data_file):
    '''
    テキストファイルを処理してDataFrameを返す関数
    '''
    texts = []

    # 指定されたファイルを読み込み、変数fileに格納
    with open(data_file, 'r', encoding='utf-8') as file:
        # ファイルの内容を文字列として読み込む
        text = file.read()
        # print(text)
        # 改行2つで文字列を分割
        sections = text.split('\n\n')
        # print(sections)

        # 各セクションに対して処理を行う
        for section in sections:
            # セクションを改行で分割する
            lines = section.split('\n')
            # print(lines)
            # linesリストの最初の要素を取得
            fname = lines[0]
            # print(fname)
            # linesリストの2番目以降の要素を取得
            content = ' '.join(lines[1:])
            # print(content)
            # fnameとcontentをリストに格納
            texts.append([fname, content])
            # print(texts)

    # リストからDataFrameを作成
    df = pd.DataFrame(texts, columns=['fname','text'])
    # print(df.iloc[1][1])
    # texts列内の改行を削除
    df['text'] = df['text'].apply(remove_newlines)
    # print(df.iloc[1][1])

    return df

df = text_to_df(r'./data.txt')
# scraped.csvファイルに書き込む
df.to_csv('./scraped.csv',index=False, encoding='utf-8')
