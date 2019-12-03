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
                return None
            page_list = page_list.load(settings.WORDS_DIR)
            page_set = set()
            for page in page_list:
                nid, score = page.page_id(), page.score()
                page_set.add(nid)
                page_score[nid] = score + page_score.get(nid, 0)
            print(word, page_set)
            if result_set is not None:
                result_set = result_set.intersection(page_set)
                if len(result_set) == 0:
                    return None
            else:
                result_set = page_set
        if result_set is None:
            return None
        return sorted([(nid, page_score[nid]) for nid in result_set],
                        key=lambda x: x[1],
                        reverse=True)
