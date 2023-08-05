# -*- coding: utf-8 -*-
import time
import traceback

import tweepy
from googletrans import Translator

from twitter2discord.discord_hooks import Webhook
from twitter2discord.utils import (DELAY, MAX_CONTENT_DISCORD_LENGTH,
                                   MAX_RE_TRY, fix_max_length, get_logger)

logger = get_logger('twitter2discord')


class TwitterStreamListener(tweepy.StreamListener):
    translator = Translator()
    follow_ids = []
    config = []

    skip_retweets = False
    skip_comments = True

    enabled_translation = True
    config_translation = {'src': 'auto', 'dest': 'en'}

    def custom_translation(self, text):
        return text

    def __init__(self, api=None, follow_ids=[], config=[]):
        super().__init__(api)
        self.follow_ids = follow_ids
        self.config = config

    def send_tweet_to_discord(self, tweet=dict, webhook_url=None):
        screen_name = tweet.get('user', {}).get('screen_name', None)
        tweet_url = 'https://twitter.com/{}/status/{}'.format(screen_name, tweet.get('id_str', None))
        embed = Webhook(webhook_url)
        # if not enabled translation
        if not self.enabled_translation:
            embed.msg = tweet_url
            embed.post()
            return
        # if the language is the same with destination translation, only send the tweet url
        if tweet.get('lang', 'en') == self.config_translation.get('dest', 'en'):
            embed.msg = tweet_url
            embed.post()
        else:
            # get full text
            if 'extended_tweet' in tweet:
                text = tweet['extended_tweet']['full_text']
            else:
                text = tweet['text']
            # custom translation
            text_content = self.custom_translation(text)
            re_try = 0
            # split text to text array by MAX_CONTENT_GG_LENGTH
            text_to_trans = fix_max_length(text_content)
            while re_try < MAX_RE_TRY:
                text_to_send = ''
                try:
                    for _text in text_to_trans:
                        logger.debug('sendToDiscord _text {}'.format(len(_text)))
                        translation = self.translator.translate(
                            _text,
                            src=self.config_translation.get('src', 'auto'),
                            dest=self.config_translation.get('dest', 'en')
                        )
                        text_to_send += translation.text + '\n'

                    text_to_send = fix_max_length(text_to_send, MAX_CONTENT_DISCORD_LENGTH - 6)
                    for _text in text_to_send:
                        msg = """```{}```""".format(_text)
                        embed.msg = msg
                        embed.post()
                    embed.msg = tweet_url
                    embed.post()
                    logger.debug('sendToDiscord ' + tweet_url)
                    break
                except AttributeError:
                    logger.error('sendToDiscord AttributeError {}'.format(traceback.format_exc()))
                    re_try += 1
                    time.sleep(DELAY)
                except Exception:
                    logger.error('sendToDiscord {}'.format(traceback.format_exc()))
                    logger.error('sendToDiscord {} {}'.format(text_content[:10], len(text_content)))
                    break

    def is_valid_status(self, status):
        # skip retweet
        if self.skip_retweets is True and status['text'].startswith('RT @'):  # or status['retweeted']:
            return False
        # skip comment
        if self.skip_comments is True:
            if status['in_reply_to_screen_name'] is not None:
                return False
            twitter_id = status.get('user', {}).get('id_str', None)
            if twitter_id not in self.follow_ids:
                return False
        return True

    def on_status(self, status):
        tweet = status._json
        twitter_id = tweet.get('user', {}).get('id_str', None)
        _config = [c for c in self.config if c['twitter_id'] == twitter_id]
        if self.is_valid_status(tweet) and len(_config) == 1:
            self.send_tweet_to_discord(tweet, _config[0]['webhook_url'])

    def on_error(self, status):
        logger.error('{}'.format(status))
        return True


class Twitter2Discord:
    config = []
    skip_retweets = True
    skip_comments = True

    enabled_translation = True
    config_translation = {'src': 'auto', 'dest': 'en'}

    def custom_translation(self, text):
        return text

    def __init__(self, config=dict, twitter_credential=dict):
        consumer_key = twitter_credential.get('consumer_key', None)
        consumer_secret = twitter_credential.get('consumer_secret', None)
        access_token = twitter_credential.get('access_token', None)
        access_secret = twitter_credential.get('access_secret', None)

        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_secret)

        self.config = config
        self._tweepyApi = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

    def _twitter_follow_ids(self):
        if self.config:
            return [c['twitter_id'] for c in self.config if 'twitter_id' in c]
        return None

    def run(self):
        TWITTER_FOLLOWS = self._twitter_follow_ids()
        streamListener = TwitterStreamListener(follow_ids=TWITTER_FOLLOWS, config=self.config)
        streamListener.skip_retweets = self.skip_retweets
        streamListener.skip_comments = self.skip_comments
        streamListener.enabled_translation = self.enabled_translation
        streamListener.custom_translation = self.custom_translation
        streamListener.config_translation = self.config_translation

        me = self._tweepyApi.me()
        logger.info('me: {} {}'.format(me['name'], me['screen_name']))
        tweepyStream = tweepy.Stream(auth=self._tweepyApi.auth, listener=streamListener)
        tweepyStream.filter(follow=TWITTER_FOLLOWS)

    def loop(self):
        while True:
            try:
                self.run()
            except Exception:
                pass
