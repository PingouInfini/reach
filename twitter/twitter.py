import twitter.twitter_authentication
import twitter.twitter_acquisition
import twitter.twitter_treatment


def get_user_tweet(user):
    api = twitter.twitter_authentication.get_api()
    twitter.twitter_acquisition.get_user_tweet(api, user)

def get_tweet_from_keywords(keywords):
    api = twitter.twitter_authentication.get_api()
    twitter.twitter_acquisition.get_tweet_from_keywords(api, keywords)

def draw_wordcloud_from_tweet(user):
    twitter.twitter_treatment.draw_wordcloud_from_tweet(user)

def plot_data_in_map(user):
    twitter.twitter_treatment.plot_data_in_map(user)