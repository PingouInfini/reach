import nltk
from nltk.tag import StanfordNERTagger
from nltk.tokenize import word_tokenize

jar = './stanford-ner/stanford-ner.jar'
model = './stanford-ner/classifiers/eunews.fr.crf.gz'

st = StanfordNERTagger(model, jar, encoding='utf8')

text = 'Delbonis enchaîne deux passings monstrueux. Djokovic renvoie le premier de façon acrobatique mais ne peut rien sur le second. Il est breaké et, agacé, en casse sa raquette.'

tokenized_text = word_tokenize(text)
classified_text = st.tag(tokenized_text)

# print(classified_text)

# Tokenize: Split sentence into words
words = nltk.word_tokenize(text)

# Run NER tagger on words
print(st.tag(words))
