import string
import re
import os

from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render
from nltk import PorterStemmer
from nltk.corpus import stopwords

from server.models.query import Query
from server.controllers import index

from engine import get_engine
from utils import get_html_titlename
from utils import extract_word


MAX_WORDS_LEN = 64
STOPWORDS_SET = set(stopwords.words('english'))

def query(request):
    words_str_p = request.GET.get('q', '')
    word_dict, _ = extract_word(words_str_p, MAX_WORDS_LEN)
    if len(word_dict) == 0:
        return HttpResponseRedirect('/')
    print(word_dict)

    engine = get_engine()
    page_score = Query.search(engine, word_dict.keys())
    pages = []
    if page_score is not None:
        for page, score in page_score:
            title_path = os.path.join(settings.HTML_DIR, get_html_titlename(page))
            title, link = open(title_path, 'r', encoding='utf-8').readlines()
            pages.append([title[:-1], link])
    context = {
        'word': words_str_p,
        'length': len(pages),
        'pages': pages
    }
    return render(request, 'search.html', context)
