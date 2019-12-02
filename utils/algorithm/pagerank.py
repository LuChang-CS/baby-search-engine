def preprocess(links_relation, url_id_map):
    reversed_links_relation = [[len(links), []] for nid, (url, links) in enumerate(links_relation)]
    for nid, (url, links) in enumerate(links_relation):
        for link in links:
            link_id = url_id_map.get(link, None)
            if link_id is not None:
                reversed_links_relation[link_id][1].append(nid)
    return reversed_links_relation


def pagerank(links_relation, alpha=0.85, max_iter=100):
    length = len(links_relation)
    ranks = [1 / length] * length
    for i in range(max_iter):
        for nid, (_, links) in enumerate(links_relation):
            ranks[nid] = (1 - alpha) / length + alpha * sum((ranks[link] / links_relation[link][0]) for link in links)
    return ranks
