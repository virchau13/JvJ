from os import path
from wordcloud import WordCloud

d = path.dirname(__file__)

text = open(path.join(d, 'test.txt')).read()

wordcloud = WordCloud().generate

