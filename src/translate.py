import os
import sys
import time
import copy
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait

this_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(this_dir)
sys.path.append(parent_dir)


def initialize_chrome_driver(params):
    chrome_options = Options()
    chrome_options.add_argument('--dns-prefetch-disable')
    chrome_options.add_argument('--disable-gpu')
    driver = Chrome(executable_path=params[
                    'DRIVER_DIR'], chrome_options=chrome_options)
    driver.set_page_load_timeout(params['PAGE_LOAD_TIMEOUT'])
    driver.maximize_window()
    return driver


def delete_emoji(text):
    return text.encode('ascii', 'ignore').decode('ascii')


def modify_tweet_text(text):
    text = delete_emoji(text)
    return text.replace('\n', ' ')


def translate_text_with_deepl(params, text, driver):
    driver.get(params['DEEPL_URL'])

    input_text_xpath = '//*[@id="dl_translator"]/div[1]/div[3]/div[2]/div/textarea'
    output_text_xpath = '//*[@id="dl_translator"]/div[1]/div[4]/div[3]/div[1]/textarea'
    language_select_xpath = '//*[@id="dl_translator"]/div[1]/div[4]/div[1]/div[1]/div[1]/button/div'
    target_language_xpath = '//*[@id="dl_translator"]/div[1]/div[4]/div[1]/div[1]/div[1]/div/button[1]'

    input_box = WebDriverWait(driver, 20).until(
        lambda driver: driver.find_element_by_xpath(input_text_xpath))
    output_box = WebDriverWait(driver, 20).until(
        lambda driver: driver.find_element_by_xpath(output_text_xpath))
    driver.execute_script('arguments[0].value = arguments[1]', input_box, text)

    select = WebDriverWait(driver, 20).until(
        lambda driver: driver.find_element_by_xpath(language_select_xpath))
    select.click()
    time.sleep(0.5)

    lang = WebDriverWait(driver, 20).until(
        lambda driver: driver.find_element_by_xpath(target_language_xpath))
    lang.click()
    time.sleep(10)

    translated_text = output_box.get_attribute('value')

    return translated_text


def translate_tweets(params, tweets, debug=False):
    tweet_translated = copy.copy(tweets)
    driver = initialize_chrome_driver(params)
    for tweet in tweet_translated:
        tweet_id = tweet['id']
        screen_name = tweet['screen_name']
        language = tweet['lang']
        full_text = modify_tweet_text(tweet['full_text'])

        if language == 'ja':
            translated_text = ''
        elif language == 'en':
            translated_text = translate_text_with_deepl(
                params, full_text, driver)
        tweet['translated_full_text'] = translated_text

        if debug:
            print('lang: {}, translated text:{} '.format(
                language, translated_text))

    driver.quit()
    return tweet_translated


def save_transalted_tweets_as_csv(tweet_translated):
    tweet_translated_pd = pd.io.json.json_normalize(tweet_translated)[
        ['created_at', 'id', 'screen_name', 'lang', 'favorite_count',
         'retweet_count', 'full_text', 'translated_full_text']
    ]
    try:
        past_tweets_df = pd.read_csv('csv/translated_tweets.csv')
        tweet_translated_pd = pd.concat([tweet_translated_pd, past_tweets_df])
    except FileNotFoundError:
        pass
    tweet_translated_pd.to_csv(
        'csv/translated_tweets.csv', index=False, encoding='utf_8_sig')
