import spacy
from spacy import displacy
import xx_ent_wiki_sm
import en_core_web_sm
from bs4 import BeautifulSoup
import requests
import re
import os
import utils.utils as utils
import json

def ner_tweet():
    #nlp = xx_ent_wiki_sm.load()
    nlp = en_core_web_sm.load()
    nlp.add_pipe(nlp.create_pipe('sentencizer'))


    def url_to_string(url):
        res = requests.get(url)
        html = res.text
        soup = BeautifulSoup(html, 'html5lib')
        for script in soup(["script", "style", 'aside']):
            script.extract()
        return " ".join(re.split(r'[\n\t]+', soup.get_text()))

    #ny_bb = url_to_string('https://www.nytimes.com/2018/08/13/us/politics/peter-strzok-fired-fbi.html?hp&action=click&pgtype=Homepage&clickSource=story-heading&module=first-column-region&region=top-news&WT.nav=top-news')
    all_tweets =""
    for file in os.listdir(utils.get_directory_from_property('Twitter', 'twitter.timeline.outputtweet')):
        with open(utils.get_directory_from_property('Twitter', 'twitter.timeline.outputtweet') + file,
                  encoding='utf-8') as f:
            tweet = json.load(f)
            all_tweets += ''.join(
                re.sub(r'(https|http)?:\/\/(\w|\.|\/|\?|\=|\&|\%)*\b', '', tweet['text'], flags=re.MULTILINE))


    print (all_tweets)
    article = nlp(all_tweets)


    displacy.serve(article, style="ent")




