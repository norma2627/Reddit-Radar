import requests
import streamlit as st
import json

# タイトル
st.title("Reddit Rader")

# URL/キーワード
topic = st.text_input("検索対象のトピック名を入力してください (例: netsec):", "netsec")
keyword = st.text_input("検索キーワードを入力してください (例: CVE-):", "CVE-")

# 検索ボタン
if st.button("検索"):
    # RedditのURL
    url = f'https://www.reddit.com/r/{topic}/new.json'

    # リクエスト送信
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)


    data = response.json()

    # 検索ワードのフィルタリング・必要なデータに絞る
    filtered_posts = [
        {
            'title': post['data']['title'],
            'url_overridden_by_dest': post['data'].get('url_overridden_by_dest', None),
            'permalink': post['data']['permalink'],
            'url': post['data']['url']
        }
        for post in data['data']['children'] if keyword in post['data']['title']
    ]

    # 結果を表示
    if filtered_posts:
        st.write(f"検索結果 ({len(filtered_posts)} 件):")
        st.json(filtered_posts)
    else:
        st.write("指定されたキーワードを含む投稿は見つかりませんでした。")
   