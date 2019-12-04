import time
import os
import _pickle as pickle

from bs4 import BeautifulSoup
from goose3 import Goose

from utils.network import NetworkFetcher


def get_html_filename(html_id):
    """HTML filename
    """
    return str(html_id) + '.html'


def get_html_titlename(html_id):
    """HTML title
    """
    return str(html_id) + '.title'


def get_html_contentname(html_id):
    """HTML pure content
    """
    return str(html_id) + '.content'


def get_html_tokenname(html_id):
    """Words of HTML pure content
    """
    return str(html_id) + '.token'


def get_html_name(html_id):
    """Conbination of them
    """
    nid = str(html_id)
    return nid + '.html', nid + '.title', nid + '.content', nid + '.token'


def _retry_fetch_htmls(fetcher, url, retry, sleep):
    """Retry to fetch html after failing

    @param fetcher: NetworkFetcher
    @param url: str
    @param retry: int, retry times
    @param sleep: int, seconds between to retry

    @return str: html or None
    """
    for r in range(retry):
        print('download %s failed, retry %d/%d times' % (url, (r + 1), retry), end='\r')
        time.sleep(sleep)
        html = fetcher.fetch(url)
        if html is not None:
            return html
    else:
        return None


def fetch_htmls(urls, output_path, retry=5, sleep=1):
    """Download html webpage with specific url

    @param urls: list, a list of urls
    @param output_path: str, path to store downloaded htmls
    @param retry: int, retry times if failed
    @param sleep: int, seconds between retry

    @return url_id_map: dict
            success_urls: list, urls downloaded successfully
            fail_urls: list urls downloaded failed
    """
    url_id_map, success_urls, fail_urls = dict(), [], []
    html_fetcher = NetworkFetcher()
    for i, url in enumerate(urls):
        html = html_fetcher.fetch(url)
        if html is None:
            html = _retry_fetch_htmls(html_fetcher, url, retry, sleep)
        if html is None:
            print('download %s failed' % url)
            fail_urls.append(url)
        else:
            print('download %s successfully' % url)
            url_id_map[url] = len(success_urls)
            success_urls.append(url)
            filename = get_html_filename(i)
            path = os.path.join(output_path, filename)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(html)

    return url_id_map, success_urls, fail_urls


class HTMLExtractor:
    """Extract information from html

    Currently, it can extract title and links using bs4, and content using goose3.
    """
    def __init__(self, html):
        """
        @param html: str
        """
        self.html = html
        self.soup = BeautifulSoup(html, 'lxml')
        self.goose = Goose({'enable_image_fetching': False})

    def extract_title(self):
        """Extract title from html

        @return title: str
        """
        return self.soup.title.get_text()

    def extract_links(self):
        """Extract links from html

        @return links: list
        """
        link_elements = self.soup.find_all('a')
        return [link_element['href'] for link_element in link_elements]

    def extract_content(self):
        """Extract pure content from html

        @return conent: str
        """
        return self.goose.extract(raw_html=self.html).cleaned_text


def extract_htmls(urls, output_path):
    """Fetch, exract and store information from html

    @param urls: list
    @param output_path: str, path to store information

    @return links_relation: list, [[a1, [a11, a12...]], ...], links list [ai1, ai2, ...] contained in ai
    """
    links_relation = []
    for id, url in enumerate(urls):
        filename, titlename, contentname, _ = get_html_name(id)
        path = os.path.join(output_path, filename)
        html = open(path, 'r', encoding='utf-8').read()
        html_fetcher = HTMLExtractor(html)
        title, links, content = html_fetcher.extract_title(), html_fetcher.extract_links(),\
            html_fetcher.extract_content()
        links_relation.append([url, links])

        titlepath = os.path.join(output_path, titlename)
        with open(titlepath, 'w', encoding='utf-8') as f:
            f.writelines([title + '\n', url])
        contentpath = os.path.join(output_path, contentname)
        with open(contentpath, 'w', encoding='utf-8') as f:
            f.write(content)
    return links_relation


class WordPage:
    """Data structure to store the information of a webpage containing a given word

    Given a word w and a page p containing w, it stores the id of p,
    word count (frequency) of w in p, and a score of p calculated with other methods.
    """
    def __init__(self, page_id, count, score=0):
        """
        @param page_id: int, id of p
        @param count, float, word count (frequency) of w in p
        @param score, float
        """
        self._page_id = page_id
        self._count = count
        self._score = score

    def page_id(self):
        return self._page_id

    def count(self):
        return self._count

    def score(self):
        return self._score

    def set_score(self, score):
        self._score = score


class WordPageList:
    """Data structue to store the list of WordPages, each of which contains w

    Since we need to store the acutal webpage list on disk, we don't keep it in memory.
    We dump the actual list to a specific path using a matching rule to the filename,
    and load the list when needed.
    """
    def __init__(self, id_):
        self._id = id_
        self._filename = str(id_) + '.list'
        self._size = 0

    def word_id(self):
        return self._id

    def size(self):
        return self._size

    def new_page(self, page_id, count, path):
        """Create a new WordPage and list

        @param page_id: int
        @param count: int (float)
        @param path: str
        """
        word_page = WordPage(page_id, count, 0)
        self._size += 1
        self.dump([word_page], path)

    def append_page(self, page_id, count, path):
        """Append a WordPage to the existing list

        @param page_id: int
        @param count: int (float)
        @param path: str
        """
        if self.size() == 0:
            self.new_page(page_id, count, path)
        else:
            page_list = self.load(path)
            word_page = WordPage(page_id, count, 0)
            page_list.append(word_page)
            self._size += 1
            self.dump(page_list, path)

    def dump(self, page_list, path):
        """Dump a list to the disk

        @param page_list: list, containing the webpages and counts (frequencies)
        @param path: str
        """
        path = os.path.join(path, self._filename)
        pickle.dump(page_list, open(path, 'wb'))

    def load(self, path):
        """Load the page list from the specific path

        @param path: str
        """
        path = os.path.join(path, self._filename)
        return pickle.load(open(path, 'rb'))