import nltk
import os
import json
import re
import utils.utils as utils
from nltk.tag import StanfordNERTagger
from nltk.tokenize import word_tokenize

jar = 'ner/stanford-ner/stanford-ner.jar'
model = 'ner/stanford-ner/classifiers/trained-ner-model-french-ser.giz'

st = StanfordNERTagger(model, jar, encoding='utf8')

def run_ner(text):
    # Tokenize: Split sentence into words
    tokenized_text = nltk.word_tokenize(text)
    # Run NER tagger on words
    classified_text = st.tag(tokenized_text)

    #print (highlight_tagged_text(classified_text))



def highlight_tagged_text(tagged_text):
    html_returned = ""
    span_begin = "<span title='{}' style='background-color:{}'>"
    span_end = "</span>"
    for word,tag in tagged_text:
        #print ("word = "+word+" // tag = "+tag)
        print(tag)
        if "PER" in tag:
            html_returned += span_begin.format("PERSONNE","#2fecff") + word + span_end+" "
        elif "LOC" in tag:
            html_returned += span_begin.format("LOCALISATION","#ff992f") + word + span_end+" "
        else:
            html_returned += word+ " "

    return html_returned



texte="La première Falcon Heavy de l'entreprise SpaceX, la plus puissante fusée des Etats-Unis jamais lancée depuis plus de quarante ans, devrait bien emporter le roadster de l'entrepreneur américain, mais sur une orbite bien différente. Elon Musk a le sens du spectacle"
run_ner(texte)