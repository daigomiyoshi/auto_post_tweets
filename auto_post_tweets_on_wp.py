from urllib.parse import urlencode
from urllib.parse import urljoin
from datetime import datetime
from requests_oauthlib import OAuth1
import requests
import copy
import json

from config import parameters


def main():
    params = parameters.params
    tweets = search_tweets(params, debug=True)
    popular_tweets = extract_popular_tweets(tweets)
    post_article(params, popular_tweets, debug=True)


# functions to search popular tweets I'm interested in
def search_tweets(params, debug=False):
    tweets = []
    auth = OAuth1(
        params['CONSUMER_KEY'],
        params['CONSUMER_SECRET_KEY'],
        params['ACCESS_TOKEN'],
        params['ACCESS_TOKEN_SECRET']
    )

    for lang in params['LANG']:
        for word in params['WORDS']:
            cnt = 0
            print(lang, word)
            word += ' exclude:retweets exclude:replies'

            while True:
                if cnt > params['RANGE']:
                    break

                if cnt == 0:
                    url_args = urlencode({
                        'lang': lang,
                        'q': word,
                        'count': str(params['COUNT']),
                        'result_type': params['RESULT_TYPE'],
                        'tweet_mode': params['TWEET_TYPE'],
                        'since': params['SINCE'],
                        'until': params['UNTIL'],
                    })
                    response = requests.get(
                        url=params['ROOT_URL'] + url_args, auth=auth)
                    data = response.json()['statuses']
                    if len(data) == 0:
                        break
                else:
                    for tweet in data:
                        max_id = int(tweet['id']) - 1
                        if tweet in tweets:
                            continue
                        tweets.append(tweet)
                        if debug:
                            print('For loop: {}, tweet created at: {}'.format(
                                cnt, tweet['created_at']))
                    url_args = urlencode({
                        'lang': lang,
                        'q': word,
                        'count': str(params['COUNT']),
                        'result_type': params['RESULT_TYPE'],
                        'tweet_mode': params['TWEET_TYPE'],
                        'since': params['SINCE'],
                        'until': params['UNTIL'],
                        'max_id': str(max_id),
                    })
                    response = requests.get(
                        url=params['ROOT_URL'] + url_args, auth=auth)
                    try:
                        data = response.json()['statuses']
                    except KeyError:  # if the number of requests is over the limit.
                        print('Error: the number of requests is over the limit.')
                        break

                cnt += 1

    return tweets


def prune_query_result(tweet):
    tweet_pruned = copy.copy(tweet)
    prune_keys = [
        'id_str',
        'truncated',
        'entities',
        'extended_entities',
        'metadata',
        'source',
        'in_reply_to_status_id',
        'in_reply_to_status_id_str',
        'in_reply_to_user_id',
        'in_reply_to_user_id_str',
        'in_reply_to_screen_name',
        'geo',
        'coordinates',
        'place',
        'contributors',
        'is_quote_status',
        'favorited',
        'retweeted',
        'possibly_sensitive',
        'quoted_status',
        'quoted_status_id',
        'quoted_status_id_str',
        'user',
    ]
    tweet_pruned['screen_name'] = tweet_pruned['user']['screen_name']
    for key in prune_keys:
        try:
            del tweet_pruned[key]
        except KeyError:
            pass
    return tweet_pruned


def extract_popular_tweets(tweets, threshold=100):
    popular_tweets = []
    for tweet in tweets:
        if tweet['favorite_count'] >= threshold:
            tweet_pruned = prune_query_result(tweet)
            popular_tweets.append(tweet_pruned)
    popular_tweets.sort(key=lambda x: x['favorite_count'], reverse=True)
    return popular_tweets


# functions to post infomation about tweets on Wordpress
def read_text_file(path):
    f = open(path)
    data = f.read()
    f.close()
    return data


def make_html_for_tweet_embeded(popular_tweets):
    html_format_to_embed_tweet = read_text_file(
        'text/html_format_to_embed_tweet.txt')
    html_for_tweets_ja = ''
    html_for_tweets_en = ''
    for tweet in popular_tweets:
        tweet_id = tweet['id']
        screen_name = tweet['screen_name']
        language = tweet['lang']
        html_to_be_added = html_format_to_embed_tweet.format(
            SCREEN_NAME=screen_name,
            ID=tweet_id
        ) + '\n'
        if language == 'ja':
            html_for_tweets_ja += html_to_be_added
        elif language == 'en':
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
        TWEETS_EN=html_for_tweets['en']
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
        print(
            '----------\nTitle: 「{}」の投稿リクエスト結果:{}'.format(params['TITLE'], repr(res.status_code)))
    return res


if __name__ == '__main__':
    main()
