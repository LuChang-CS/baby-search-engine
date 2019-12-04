import os
import json

from utils import CompressedTrie
from utils import fetch_htmls, extract_htmls, WordPageList
from utils import get_html_filename, get_html_tokenname, get_html_contentname
from utils import Configuration
from utils import pagerank
from utils.algorithm.pagerank import preprocess
from utils import extract_word


class PreprocessConfiguration(Configuration):
    input_path = None
    output_path = None
    use_pagerank = True
    use_tfidf = True

    def __init__(self, config=None):
        super().__init__(config)


def load_content(path, html_id):
    filename = get_html_contentname(html_id)
    path = os.path.join(path, filename)
    return open(path, encoding='utf-8').read()


def dump_html_words(path, html_id, word_dict):
    tokenname = get_html_tokenname(html_id)
    path = os.path.join(path, tokenname)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(word_dict, f)


def standardize_bbc_link(urls, links):
    domain = 'https://www.bbc.com'
    alter_domain = 'https://www.bbc.co.uk'
    result = []
    for i, link in enumerate(links):
        if link[0] == '/':
            std_link = domain + link
        elif link.startswith(alter_domain):
            std_link = link.replace(alter_domain, domain)
        if std_link in urls:
            result.append(std_link)
    return list(set(result))


if __name__ == '__main__':
    preprocess_config = {
        'input_path': 'data/input/urls',
        'output_path': 'data/output/',
        'use_pagerank': True
    }
    config = PreprocessConfiguration(preprocess_config)
    output_path = config.output_path
    html_path = os.path.join(output_path, 'htmls')
    word_path = os.path.join(output_path, 'words')
    trie_path = os.path.join(output_path, 'trie')

    # calculate links relation (url and links that this url links to), like
    # [
    #     url: [link1, link2, ...],
    #     ...
    # ]
    urls = [url.strip() for url in open(config.input_path, 'r').readlines()]
    url_id_map, success_urls, fail_urls = fetch_htmls(urls, html_path)
    links_relation = extract_htmls(success_urls, html_path)
    for i, (url, links) in enumerate(links_relation):
        links_relation[i] = [url, standardize_bbc_link(urls, links)]

    trie = CompressedTrie()

    # inserting words in each html to trie and store their frequencies and current url to the occurence list.
    print('inserting words to trie...')
    for nid, url in enumerate(success_urls):
        print('processing %d / %d pages...' % (nid + 1, len(success_urls)))
        content = load_content(html_path, nid)
        word_dict, total_count = extract_word(content)
        dump_html_words(html_path, nid, word_dict)
        for word, count in word_dict.items():
            value = trie.search(word)
            if value is None:
                id_ = trie.size()
                value = WordPageList(id_)
                value.new_page(nid, count / total_count, word_path)
                trie.insert(word, value)
            else:
                value.append_page(nid, count / total_count, word_path)

    # calculate page rank.
    print('calculating page rank...')
    if config.use_pagerank:
        reversed_links_relation = preprocess(links_relation, url_id_map)
        ranks = pagerank(reversed_links_relation)
        # use page rank and frequency to sort the links
        for value in trie.value_list():
            page_list = value.load(word_path)
            for word_page in page_list:
                nid, count, score = word_page.page_id(), word_page.count(), word_page.score()
                word_page.set_score(count * ranks[nid])
            page_list.sort(key=lambda t: -t.score())
            value.dump(page_list, word_path)

    CompressedTrie.dump(trie, trie_path)
