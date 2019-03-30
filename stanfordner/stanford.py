import nltk
import os
import json
import re
import utils.utils as utils
from nltk.tag import StanfordNERTagger
from nltk.tokenize import word_tokenize

jar = 'stanfordner/stanford-ner/stanford-ner.jar'
model = 'stanfordner/stanford-ner/classifiers/trained-ner-model-french-ser.giz'

st = StanfordNERTagger(model, jar, encoding='utf8')

def run_ner(text):
    # Tokenize: Split sentence into words
    tokenized_text = nltk.word_tokenize(text)
    # Run NER tagger on words
    classified_text = st.tag(tokenized_text)

    print(classified_text)


def process(user):
    all_tweets =""
    for file in os.listdir(utils.get_directory_from_property('Twitter', 'twitter.timeline.outputtweet')):
        with open(utils.get_directory_from_property('Twitter', 'twitter.timeline.outputtweet') + file,
                  encoding='utf-8') as f:
            tweet = json.load(f)
            all_tweets += ''.join(
                re.sub(r'(https|http)?:\/\/(\w|\.|\/|\?|\=|\&|\%)*\b', '', tweet['text'], flags=re.MULTILINE))

    run_ner(all_tweets)