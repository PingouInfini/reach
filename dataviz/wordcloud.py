import time
import os
import matplotlib.pyplot as plt
import utils.utils as utils
from wordcloud import WordCloud
from stop_words import get_stop_words

def drawn_wordcloud_from_data(data, language, user):
    # Generate a word cloud image
    wordcloud = WordCloud(background_color="white",
                          height=800,
                          width=1600,
                          max_words=100,
                          stopwords=get_stop_words(language)) \
        .generate(data)

    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")

    output = utils.get_directory_from_property('Wordcloud', 'wordcloud.outputdirectory')
    if not os.path.exists(output):
        os.makedirs(output)
    plt.savefig(output + "/" + user + "_" + str(time.time()) + ".png")
    # plt.show()