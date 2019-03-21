import os
import re
import json
import time
import dataviz.wordcloud
import dataviz.foliummap
import dataviz.geographics
import utils.utils as utils
from collections import Counter


def draw_wordcloud_from_tweet(user):
    all_tweets = ""
    languages = Counter()

    for file in os.listdir(utils.get_directory_from_property('Twitter', 'twitter.timeline.outputtweet')):
        with open(utils.get_directory_from_property('Twitter', 'twitter.timeline.outputtweet') + file,
                  encoding='utf-8') as f:
            tweet = json.load(f)
            all_tweets += ''.join(
                re.sub(r'(https|http)?:\/\/(\w|\.|\/|\?|\=|\&|\%)*\b', '', tweet['text'], flags=re.MULTILINE))
            languages.update([tweet['lang']])

    for file in os.listdir(utils.get_directory_from_property('Twitter', 'twitter.keywords.outputtweet')):
        with open(utils.get_directory_from_property('Twitter', 'twitter.keywords.outputtweet') + file,
                  encoding='utf-8') as f:
            tweet = json.load(f)
            all_tweets += ''.join(
                re.sub(r'(https|http)?:\/\/(\w|\.|\/|\?|\=|\&|\%)*\b', '', tweet['text'], flags=re.MULTILINE))
            languages.update([tweet['lang']])

    most_used_lang = [x[0] for x in languages.most_common(1)][0]

    dataviz.wordcloud.drawn_wordcloud_from_data(all_tweets, most_used_lang, user)


def plot_data_in_map(user):
    map, group_sub_group = dataviz.foliummap.create_map([user, "others"])

    for file in os.listdir(utils.get_directory_from_property('Twitter', 'twitter.timeline.outputtweet')):
        with open(utils.get_directory_from_property('Twitter', 'twitter.timeline.outputtweet') + file,
                  encoding='utf-8') as f:
            extract_coord_from_tweet(f, group_sub_group.get(user, "none"), map)

    for file in os.listdir(utils.get_directory_from_property('Twitter', 'twitter.keywords.outputtweet')):
        with open(utils.get_directory_from_property('Twitter', 'twitter.keywords.outputtweet') + file,
                  encoding='utf-8') as f:
            extract_coord_from_tweet(f, group_sub_group.get('others', "none"), map)

    dataviz.foliummap.save_map(map, utils.get_directory_from_property('FoliumMap', 'foliummap.outputdirectory'), user + ".html")


def extract_coord_from_tweet(f, sub_group, map):
    tweet = json.load(f)
    if tweet['coordinates'] is not None:
        lng = tweet['coordinates']['coordinates'][0]
        lat = tweet['coordinates']['coordinates'][1]
        # prepare popup to show for each marker (content = tweet)
        html_popup = create_html_popup(lat, lng, tweet)
        # create markers and add them to the map
        dataviz.foliummap.plot_markers(sub_group, [lat, lng], html_popup)
    elif tweet['place'] is not None:
        # relevance-based search by location and name
        (lat, lng) = dataviz.geographics.geodecode(tweet['place']['full_name'])
        if lat == 0 and lng == 0:
            # relevance-based search by different location and name values
            (lat, lng) = dataviz.geographics.geodecode(tweet['contributors'], ['coordinates'])
            if lat == 0 and lng == 0:
                pass

        # prepare popup to show for each marker (content = tweet)
        html_popup = create_html_popup(lat, lng, tweet)
        # create markers and add them to the map
        dataviz.foliummap.plot_markers(sub_group, [lat, lng], html_popup)
    else:
        pass


def create_html_popup(lat, lng, tweet):
    html = """
    <div class="content" style="font-family:Segoe UI,Arial,sans-serif">
        <div style="padding-bottom: 10px">
            <strong>{}</strong><span>&nbsp;</span><span style="color:#657786;">@{} - {}</span></a>
            <br/>{}
        </div>
        {}
        <div>
            <span style="color:#657786;">depuis </span> <span style="color:#0084b4;">{}{}</span>
        </div>
        <div style="margin-bottom:10px">
            <a rel="nofollow noopener" href="http://twitter.com/findtweetbyid/status/{}" target="_blank" style="float: right;position: relative;">
                <span style="background: url(data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz4KPCEtLSBHZW5lcmF0b3I6IEFkb2JlIElsbHVzdHJhdG9yIDE2LjAuMCwgU1ZHIEV4cG9ydCBQbHVnLUluIC4gU1ZHIFZlcnNpb246IDYuMDAgQnVpbGQgMCkgIC0tPgo8IURPQ1RZUEUgc3ZnIFBVQkxJQyAiLS8vVzNDLy9EVEQgU1ZHIDEuMS8vRU4iICJodHRwOi8vd3d3LnczLm9yZy9HcmFwaGljcy9TVkcvMS4xL0RURC9zdmcxMS5kdGQiPgo8c3ZnIHZlcnNpb249IjEuMSIgaWQ9IkxheWVyXzEiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIgeG1sbnM6eGxpbms9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkveGxpbmsiIHg9IjBweCIgeT0iMHB4IiB3aWR0aD0iMTAwcHgiIGhlaWdodD0iMTAwcHgiIHZpZXdCb3g9IjAgMCAxMDAgMTAwIiBlbmFibGUtYmFja2dyb3VuZD0ibmV3IDAgMCAxMDAgMTAwIiB4bWw6c3BhY2U9InByZXNlcnZlIj4KPGcgaWQ9IkxheWVyXzMiPgo8L2c+CjxnPgoJPHBhdGggZmlsbD0iIzAxMDEwMSIgZD0iTTgyLjY4Niw1My43NTRjLTIuMzI2LDAtNC4yMiwxLjg5LTQuMjIsNC4yMTZ2MjguMzYyYzAsMi44OTctMi4zNTUsNS4yNTYtNS4yNTIsNS4yNTZIMTMuODEyICAgYy0yLjg5NSwwLTUuMjUyLTIuMzU4LTUuMjUyLTUuMjU2VjI2LjkzNGMwLTIuODk2LDIuMzU3LTUuMjUyLDUuMjUyLTUuMjUyaDI4LjM2NGMyLjMyNiwwLDQuMjE3LTEuODkyLDQuMjE3LTQuMjE4ICAgYzAtMi4zMjQtMS44OTItNC4yMTYtNC4yMTctNC4yMTZIMTMuODEyYy0zLjY0OSwwLTcuMDg1LDEuNDI1LTkuNjczLDQuMDE0Yy0yLjU4NywyLjU4Ny00LjAxNCw2LjAyMi00LjAxNCw5LjY3MnY1OS4zOTggICBjMCw3LjU0OCw2LjE0LDEzLjY4OCwxMy42ODcsMTMuNjg4aDU5LjQwMmM3LjU0NywwLDEzLjY4Ny02LjE0LDEzLjY4Ny0xMy42ODhWNTcuOTdDODYuOSw1NS42NDQsODUuMDEyLDUzLjc1NCw4Mi42ODYsNTMuNzU0eiIvPgoJPHBhdGggZmlsbD0iIzAxMDEwMSIgZD0iTTg2LjI3NS0wLjA3aC0yNy42Yy0yLjMxOCwwLTQuMjAyLDEuODg1LTQuMjAyLDQuMjAzYzAsMi4zMTcsMS44ODQsNC4yMDMsNC4yMDIsNC4yMDNoMjYuODk2ICAgbC00OC4zOCw0OC4zNzVjLTAuNzk0LDAuNzk3LTEuMjMxLDEuODUxLTEuMjMxLDIuOTdjMCwxLjEyNiwwLjQzOCwyLjE4MiwxLjIzMSwyLjk3NmMxLjU4MywxLjU4Miw0LjM1NSwxLjU4NSw1Ljk0NCwwICAgbDQ4LjM3Ni00OC4zNzd2MjYuODljMCwyLjMxNywxLjg4Miw0LjIwMSw0LjIsNC4yMDFjMi4zMTcsMCw0LjIwMi0xLjg4NCw0LjIwMi00LjIwMXYtMjcuNkM5OS45MTUsNi4wNDgsOTMuNzk1LTAuMDcsODYuMjc1LTAuMDd6ICAgIi8+CjwvZz4KPC9zdmc+) no-repeat 0 0;background-size: 10px;width: 10px;height: 10px;display: block;float: left;position: relative;top: 3px;left: -4px;"></span>
            source
            </a>
        </div>
    </div>
    """

    html_popup = html.format(tweet['user']['name'], tweet['user']['screen_name'], date_beautifier(tweet['created_at']),
                             tweet['text'],
                             add_media_if_exists(tweet), tweet['place']['full_name'],
                             " [" + str(lng) + "," + str(lat) + "]", tweet['id'])
    return html_popup


def date_beautifier(created_at):
    return time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(created_at, '%a %b %d %H:%M:%S +0000 %Y'))


def add_media_if_exists(tweet):
    medias = ""

    media_div = """
    <div style="padding-bottom: 10px">
        <img style="width:250px;"
        src="{}"
        alt="img" />
    </div>
    """

    try:
        index = 0
        for media in tweet['entities']['media']:
            index += 1
            media_url = media['media_url']
            medias += media_div.format(media_url)

        return medias
    except:
        # pas de media...
        return ""
