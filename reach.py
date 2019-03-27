import configparser
import sys
import logging
import google.googleimages
import twitter.twitter
import ner.stanford
import utils.utils as utils

def usage():
    print("Usage:")
    print("python {} <username>".format(sys.argv[0]))


if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage()
        sys.exit(1)

    user = sys.argv[1]

    config = configparser.RawConfigParser()
    config.read('properties.config')
    logging.basicConfig(stream=sys.stderr, level=logging.INFO)
    if utils.get_boolean_from_property('Debug', 'verbose.active') == True:
        logging.getLogger().setLevel(logging.DEBUG)


    ### GOOGLE IMAGES
    if (config['ActiveComponents'].getboolean('component.googleimages.activate') == True):
        google.googleimages.treatment(user)
    else:
        logging.debug("component.googleimages.activate = FALSE")

    ### TWITTER
    if (config['ActiveComponents'].getboolean('component.twitter.activate') == True):
        twitter.twitter.get_user_tweet(user)
        twitter.twitter.get_tweet_from_keywords(user)
        twitter.twitter.draw_wordcloud_from_tweet(user)
        twitter.twitter.plot_data_in_map(user)
    else:
        logging.debug("component.twitter.activate = FALSE")

    ### NER
    if (config['ActiveComponents'].getboolean('component.ner.activate') == True):
        ner.stanford.process(user)
    else:
        logging.debug("component.ner.activate = FALSE")