import warnings
warnings.filterwarnings('ignore')

from config import parameters
from src import search_twitter, post_wordpress, translate


def main():
    params = parameters.params
    tweets = search_twitter.search_tweets(
        params=params, debug=True
    )
    popular_tweets = search_twitter.extract_popular_tweets(
        params=params, tweets=tweets, debug=True
    )
    tweet_translated = translate.translate_tweets(
        params=params, tweets=popular_tweets, debug=True
    )
    translate.save_transalted_tweets_as_csv(
        tweet_translated=tweet_translated
    )
    post_wordpress.post_article(
        params=params, tweets=tweet_translated, debug=True
    )


if __name__ == '__main__':
    main()
