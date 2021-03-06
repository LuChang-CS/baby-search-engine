from django.conf import settings

from utils import WordPageList


class Query:

    @staticmethod
    def search(engine, words):
        """Search the intersection result of input words

        @param engine: Engine, specific search engine type
        @param words: list, input words
        @return result_list: list or None
        """
        page_score = dict()
        result_set = None
        for word in words:
            page_list = engine.search(word)
            if page_list is None:
                return None
            page_list = page_list.load(settings.WORDS_DIR)
            page_set = set()
            page_dict = dict()
            for page in page_list:
                nid, score = page.page_id(), page.score()
                page_set.add(nid)
                page_dict[nid] = score
            if result_set is not None:
                result_set = result_set.intersection(page_set)
                if len(result_set) == 0:
                    return None
                for nid in result_set:
                    page_score[nid] = page_dict[nid] + page_score.get(nid, 0)
            else:
                result_set = page_set
                page_score = page_dict
        if result_set is None:
            return None
        return sorted([(nid, page_score[nid]) for nid in result_set],
                        key=lambda x: x[1],
                        reverse=True)
