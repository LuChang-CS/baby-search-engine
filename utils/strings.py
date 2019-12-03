import re

from nltk.tokenize import word_tokenize
from nltk import PorterStemmer
from nltk.corpus import stopwords


ps = PorterStemmer()


def common_prefix(strp, strt):
    """Calculate the index of the first character not being
    prefix of two strings.

    @param strp: str
    @param strt: str
    @return: index, the first character not being prefix of two strings.
             If two string are the same, index is the length of strings.
             If one string is the prefix of the other, index is the length of the shortter one.
    """
    assert strp != '' and strt != ''
    index = 0
    for i, (x, y) in enumerate(zip(strp, strt)):
        index = i
        if x != y:
            break
    else:
        index += 1
    return index


def extract_word(text, max_len=None):
    """Extract words from a text

    @param: text, str
    @param: max_len, the maximum length of text we want to extract, default None
    @return: dict, contains all distinct words and their count, like
             {
                 word: count
             }
    """
    # replace non-word-character with space
    text = re.sub(r'[^\w\s]', ' ', text.strip().lower())
    if max_len is not None:
        text = text[:max_len]
    # tokenize text using NLTK
    words = word_tokenize(text)
    stopwords_set = set(stopwords.words('english'))
    word_dict = dict()
    for word in words:
        p = word
        # word stem
        word = ps.stem(word).lower()
        # remove stopwords
        if word not in stopwords_set:
            count = word_dict.get(word, 0)
            word_dict[word] = count + 1
    return word_dict, len(words)
