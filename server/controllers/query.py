import string
import re

from django.http import HttpResponseRedirect
from django.shortcuts import render
from nltk import PorterStemmer

from server.models.query import Query
from server.controllers import index

from engine import get_engine


MAX_WORDS_LEN = 64

def query(request):
    words_str = request.GET.get('q', '')
    words_str = re.sub(r'[^\w\s]', '%20', words_str.strip())
    if len(words_str) == 0:
        return HttpResponseRedirect('/')
    words = [word.strip() for word in words_str.split(' ')]
    words = [word for word in words if len(words) > 0]
    words = words[:MAX_WORDS_LEN]

    engine = get_engine()
    pages = Query.search(engine, words)
