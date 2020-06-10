from urllib.parse import urlencode
from requests_oauthlib import OAuth1
import requests
import copy
import json
import os
import sys

this_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(this_dir)
sys.path.append(parent_dir)


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
            if debug:
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
                        if len(data) == 0:
                            break
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


def extract_popular_tweets(params, tweets, debug=False):
    popular_tweets = []
    popular_tweets_ids = []
    for tweet in tweets:
        if tweet['favorite_count'] >= params['THRESHOLD']:
            if tweet['id'] not in popular_tweets_ids:
                popular_tweets_ids.append(tweet['id'])
                tweet_pruned = prune_query_result(tweet)
                popular_tweets.append(tweet_pruned)
    popular_tweets.sort(key=lambda x: x['favorite_count'], reverse=True)
    if debug:
        print('the number of tweets:{}'.format(len(popular_tweets)))

    return popular_tweets
