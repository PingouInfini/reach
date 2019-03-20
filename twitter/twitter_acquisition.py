import os
import io
import json
import configparser
import requests
from tweepy import Cursor

config = configparser.RawConfigParser()
config.read('properties.config')


def get_user_tweet(api, user):
    if user != "":
        pages= (config['Twitter'].getint('twitter.timeline.limit') // 200) +1
        for page in Cursor(api.user_timeline, screen_name=user, count=200).pages(pages):
            for status in page:
                tweet = status._json
                save_1_tweet(config.get('Twitter', 'twitter.timeline.outputtweet'),
                             config.get('Twitter', 'twitter.timeline.outputmedia'),
                             tweet, tweet['id_str'])
        # new_tweets = api.user_timeline(screen_name=user, count=config.get('Twitter', 'twitter.timeline.limit'))
        # save_tweets_as_json(config.get('Twitter', 'twitter.timeline.outputtweet'),
        #                     config.get('Twitter', 'twitter.timeline.outputmedia'),
        #                     new_tweets)


def get_tweet_from_keywords(api, keywords):
    if keywords != "":
        pages= (config['Twitter'].getint('twitter.keywords.limit') // 200) +1
        for page in Cursor(api.search, q=keywords, count=200).pages(pages):
            for status in page:
                tweet = status._json
                save_1_tweet(config.get('Twitter', 'twitter.keywords.outputtweet'),
                             config.get('Twitter', 'twitter.keywords.outputmedia'),
                             tweet, tweet['id_str'])
        # new_tweets = api.search(q=keywords, count=config.get('Twitter', 'twitter.keywords.limit'))
        # save_tweets_as_json(config.get('Twitter', 'twitter.keywords.outputtweet'),
        #                     config.get('Twitter', 'twitter.keywords.outputmedia'),
        #                     new_tweets)




def save_tweets_as_json(jsonoutput, mediaoutput, tweetslist):
    if not os.path.exists(jsonoutput):
        os.makedirs(jsonoutput)

    for eachtweet in tweetslist:
        tweet = eachtweet._json
        save_1_tweet(jsonoutput, mediaoutput, tweet, eachtweet.id_str)


def save_1_tweet(jsonoutput, mediaoutput, tweet, id_str):
    if not os.path.exists(jsonoutput):
        os.makedirs(jsonoutput)
    with io.open(jsonoutput + '/' + id_str + '.json', 'w', encoding='utf-8') as jfile:
        jfile.write(json.dumps(tweet, ensure_ascii=False))
    if (config['Twitter'].getboolean('twitter.savemedia') == True):
        if not os.path.exists(mediaoutput):
            os.makedirs(mediaoutput)
        save_tweet_media(tweet, mediaoutput)


def save_tweet_media(tweet, mediaoutput):
    try:
        index = 0
        for media in tweet['entities']['media']:
            index += 1

            r = requests.get(media['media_url'], allow_redirects=True)
            filename = mediaoutput + "/" + str(tweet['id']) + "_" + str(index)
            if (media['type'] == "photo"):
                filename += ".jpg"
                io.open(filename, 'wb').write(r.content)
            elif (media['type'] == "video" or media['type'] == "animated_gif"):
                filename += ".mp4"
                io.open(filename, 'wb').write(r.content)
    except:
        pass


def save_media_from_url(media, tweet_id, index):
    r = requests.get(media['media_url'], allow_redirects=True)
    filename = "media/" + str(tweet_id) + "_" + str(index)
    if (media['type'] == "photo"):
        filename += ".jpg"
        io.open(filename, 'wb').write(r.content)
    elif (media['type'] == "video" or media['type'] == "animated_gif"):
        filename += ".mp4"
        io.open(filename, 'wb').write(r.content)
