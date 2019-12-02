from django.conf import settings

from utils import WordPageList


class Query:

    @staticmethod
    def search(engine, words):
        page_score = dict()
        result_set = None
        for word in words:
            page_list = engine.search(word)
            if page_list is None:
                continue
            page_list = engine.search(word).load(settings.WORDS_DIR)
            page_set = set()
            for page in page_list:
                nid, score = page[0]
                page_set.add(nid)
                if nid in page_score:
                    page_score[nid] += score
            if result_set is not None:
                result_set = result_set.intersection(page_set)
            else:
                result_set = page_set
        if len(result_set) == 0:
            return None
        return sorted(iterable=[(nid, page_score[nid]) for nid in result_set],
                        key=lambda x: x[1],
                        reverse=True)
