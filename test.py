from utils import CompressedTrie


if __name__ == '__main__':
    a = [
        ['bear', 'sell', 'stock', 'bull'],
        ['bid', 'stock', 'bear', 'bull'],
        ['buy', 'bull', 'stop', 'sell'],
        ['be', 'se', 'bu']
    ]

    trie = CompressedTrie()

    for i, words in enumerate(a):
        for word in words:
            value = trie.search(word)
            if value is not None:
                value.append(i)
            else:
                trie.insert(word, [i])

    for i, words in enumerate(a):
        for word in words:
            value = trie.search(word)
            print(word, value)
