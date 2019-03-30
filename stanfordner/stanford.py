import nltk
import os
import json
import re
import io
import utils.utils as utils
from nltk.tag import StanfordNERTagger
from nltk.tokenize import word_tokenize

jar = 'stanfordner/stanford-ner/stanford-ner.jar'
model = 'stanfordner/stanford-ner/classifiers/trained-ner-model-french-ser.giz'

st = StanfordNERTagger(model, jar, encoding='utf8')

def run_ner(text,user):
    # Tokenize: Split sentence into words
    tokenized_text = nltk.word_tokenize(text)
    # Run NER tagger on words
    classified_text = st.tag(tokenized_text)

    highlighted_text = highlight_tagged_text(classified_text)

    save_text_as_html_file(highlighted_text,user)

def highlight_tagged_text(tagged_text):
    html_returned = ""
    twitter_account=False
    span_begin = "<span title='{}' style='background-color:{}'>"
    span_end = "</span>"


    for word,tag in tagged_text:
        if twitter_account:
            twitter_account = False
            html_returned += span_begin.format("Twitter account","#af2fff45") + word + span_end+" "

        if "PER" in tag:
            html_returned += span_begin.format("PERSONNE","#2fecff") + word + span_end+" "
        elif "LOC" in tag:
            html_returned += span_begin.format("LOCALISATION","#ff992f") + word + span_end+" "
        elif "ORG" in tag:
            html_returned += span_begin.format("ORGANISATION","#2fff5c") + word + span_end+" "
        elif word.startswith('@'):
            html_returned += span_begin.format("Twitter account","#af2fff45") + word + span_end+""
            twitter_account = True
        else:
            html_returned += word+ " "

    return html_returned

def save_text_as_html_file(text, filename):
    with io.open("stanfordner/"+filename + '-ner.html', 'w', encoding='utf-8') as jfile:
        jfile.write(text)

def process(user):
    all_tweets =""
    for file in os.listdir(utils.get_directory_from_property('Twitter', 'twitter.timeline.outputtweet')):
        with open(utils.get_directory_from_property('Twitter', 'twitter.timeline.outputtweet') + file,
                  encoding='utf-8') as f:
            tweet = json.load(f)
            all_tweets += ''.join(
                re.sub(r'(https|http)?:\/\/(\w|\.|\/|\?|\=|\&|\%)*\b', '', tweet['text'], flags=re.MULTILINE))

    run_ner(all_tweets,user)