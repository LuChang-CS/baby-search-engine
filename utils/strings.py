from nltk.tokenize import word_tokenize
from nltk import PorterStemmer
from nltk.corpus import stopwords


def common_prefix(strp, strt):
    assert strp != '' and strt != ''
    index = 0
    for i, (x, y) in enumerate(zip(strp, strt)):
        index = i
        if x != y:
            break
    else:
        index += 1
    return index


def extract_word(text):
    words = word_tokenize(text)
    ps = PorterStemmer()
    stopwords_set = set(stopwords.words('english'))
    word_dict = dict()
    for word in words:
        word = ps.stem(word).lower()
        if word not in stopwords_set:
            count = word_dict.get(word, 0)
            word_dict[word] = count + 1
    return word_dict, len(words)
