import string
import re
import os
import time

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
    overflow = 0
    # preprocess for the input text
    words_str_p = request.GET.get('q', '')
    # we have limitation to the length of text
    if len(words_str_p) > MAX_WORDS_LEN:
        words_str_p = words_str_p[:MAX_WORDS_LEN]
        overflow = 1
    if len(words_str_p) == 0:
        return HttpResponseRedirect('/')
    word_dict, _ = extract_word(words_str_p)
    print(word_dict)

    engine = get_engine()

    start_time = time.time()
    page_score = Query.search(engine, word_dict.keys())
    end_time = time.time()
    pages = []
    if page_score is not None:
        for page, score in page_score:
            title_path = os.path.join(settings.HTML_DIR, get_html_titlename(page))
            title, link = open(title_path, 'r', encoding='utf-8').readlines()
            pages.append([title[:-1], link, score])
    context = {
        'word': words_str_p,
        'length': len(pages),
        'pages': pages,
        'time': '%.8f' % (end_time - start_time),
        'overflow': overflow
    }
    return render(request, 'search.html', context)
