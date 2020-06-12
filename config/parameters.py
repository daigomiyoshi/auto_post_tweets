params_to_be_set = {
    'YEAR': '2020',
    'S_MONTH': '06',
    'S_DATE': '11',
    'E_MONTH': '06',
    'E_DATE': '12',
}

params = {
    'YEAR': params_to_be_set['YEAR'],
    'S_MONTH': params_to_be_set['S_MONTH'],
    'S_DATE': params_to_be_set['S_DATE'],
    'E_MONTH': params_to_be_set['E_MONTH'],
    'E_DATE': params_to_be_set['E_DATE'],

    # Secret key of Twitter API
    'CONSUMER_KEY': 'foLsfclN3YXISSrstIqdzGmri',
    'CONSUMER_SECRET_KEY': 'D5EoS9E6eQRUdhHBQSCv6rVgutu9EhunnCww6iNJfoyrtvPYMG',
    'ACCESS_TOKEN': '4096685054-24InfHUvJzq14IYz8g7wCXmVaQwLDxzyzYDtKQ1',
    'ACCESS_TOKEN_SECRET': 'V3Q1q5MTStmHBUTiHYBFftEBXLXxWe7LnaJnUlLZ5eVPH',

    # Request parameters for Twitter API
    'ROOT_URL': 'https://api.twitter.com/1.1/search/tweets.json?',
    'LANG': ['ja', 'en'],
    'TWEET_TYPE': 'extended',
    # the number of response per one request (max 100, default is 15)
    'COUNT': 100,
    # the number of request (max 180/15minutes)
    'RANGE': 10,
    'SINCE': '{}-{}-{}'.format(params_to_be_set['YEAR'], params_to_be_set['S_MONTH'], params_to_be_set['S_DATE']),
    'UNTIL': '{}-{}-{}'.format(params_to_be_set['YEAR'], params_to_be_set['E_MONTH'], params_to_be_set['E_DATE']),
    'RESULT_TYPE': 'mixed',  # popular or mixed or recent
    'WORDS':  ['\"データサイエンス\"', '\"機械学習\"', '\"data science\"', '\"machine learning\"'],
    'THRESHOLD': 200,

    # parameters for Wordpress
    'WP_URL': 'https://hophead-ds.com',
    'WP_USERNAME': 'user',
    'WP_PASSWORD': 'oAVL oteM IlaB cTdi gmF6 5MMP',
    'STATUS': 'draft',
    'CATEGORY': [5],
    'SLUG': '{}-{}-{}-twitter-auto-post'.format(params_to_be_set['YEAR'], params_to_be_set['E_MONTH'], params_to_be_set['E_DATE']),
    'TITLE': 'データサイエンス・機械学習 Twitter 投稿まとめ {}/{}/{}-{}/{}/{}'.format(
        params_to_be_set['YEAR'], params_to_be_set[
            'S_MONTH'], params_to_be_set['S_DATE'],
        params_to_be_set['YEAR'], params_to_be_set[
            'E_MONTH'], params_to_be_set['E_DATE']
    ),
    'TAG_IDS': [],
    'MEDIA_ID': None,

    # parameters for selenium with chromedriver
    'DRIVER_DIR': 'config/chromedriver_v83',
    'DEEPL_URL': 'https://www.deepl.com/ja/translator',
    'PAGE_LOAD_TIMEOUT': 10,

}
