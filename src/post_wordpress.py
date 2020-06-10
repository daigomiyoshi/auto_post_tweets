import os
import sys
from urllib.parse import urljoin
from datetime import datetime
import requests
import json

this_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(this_dir)
sys.path.append(parent_dir)


def read_text_file(path):
    f = open(path)
    data = f.read()
    f.close()
    return data


def make_html_for_tweet_embeded(popular_tweets):
    html_format_for_tweet_ja = read_text_file(
        'text/html_format_for_tweet_ja.txt')
    html_format_for_tweet_en = read_text_file(
        'text/html_format_for_tweet_en.txt')
    html_for_tweets_ja = ''
    html_for_tweets_en = ''
    for tweet in popular_tweets:
        tweet_id = tweet['id']
        screen_name = tweet['screen_name']
        language = tweet['lang']
        translated_full_text = tweet['translated_full_text']
        if language == 'ja':
            html_to_be_added = html_format_for_tweet_ja.format(
                SCREEN_NAME=screen_name,
                ID=tweet_id
            ) + '\n'
            html_for_tweets_ja += html_to_be_added
        elif language == 'en':
            html_to_be_added = html_format_for_tweet_en.format(
                SCREEN_NAME=screen_name,
                ID=tweet_id,
                TRANSLATED_TEXT=translated_full_text
            ) + '\n'
            html_for_tweets_en += html_to_be_added
    return {
        'ja': html_for_tweets_ja,
        'en': html_for_tweets_en
    }


def make_content_as_html_for_wp(params, popular_tweets):
    html_for_tweets = make_html_for_tweet_embeded(popular_tweets)
    body_for_wp_post = read_text_file('text/body_for_wp_post.txt')
    body_for_wp_post = body_for_wp_post.format(
        YEAR=params['YEAR'],
        S_MONTH=params['S_MONTH'],
        S_DATE=params['S_DATE'],
        E_MONTH=params['E_MONTH'],
        E_DATE=params['E_DATE'],
        TWEETS_JA=html_for_tweets['ja'],
        TWEETS_EN=html_for_tweets['en'],

    )
    return body_for_wp_post


def post_article(params, tweets, debug=False):
    user_name = params['WP_USERNAME']
    pass_word = params['WP_PASSWORD']
    payload = {
        "status": params['STATUS'],
        "slug": params['SLUG'],
        "title": params['TITLE'],
        "content": make_content_as_html_for_wp(params, tweets),
        "date": datetime.now().isoformat(),
        "categories": params['CATEGORY'],
    }
    if params['MEDIA_ID'] is not None:
        payload['featured_media'] = params['MEDIA_ID']
    res = requests.post(
        urljoin(params['WP_URL'], "wp-json/wp/v2/posts"),
        data=json.dumps(payload),
        headers={'Content-type': "application/json"},
        auth=(user_name, pass_word)
    )
    if debug:
        print('Title:「{}」の投稿リクエスト結果:{}\n'.format(
            params['TITLE'], repr(res.status_code))
        )
    return res
