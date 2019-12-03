import os
import _pickle as pickle

from utils.strings import common_prefix
from utils.trees import Node, Tree


class Trie(Tree):
    NAME = 'trie'

    def __init__(self):
        super().__init__(root_key=None, root_value=None)
        self._value_list = []

    def value_list(self):
        return self._value_list

    def insert(self, word, value):
        pass

    def search(self, word):
        return None

    @staticmethod
    def dump(trie, path):
        path = os.path.join(path, Trie.NAME)
        pickle.dump(trie, open(path, 'wb'))

    @staticmethod
    def load(path):
        path = os.path.join(path, Trie.NAME)
        return pickle.load(open(path, 'rb'))


class CompressedTrie(Trie):
    def __init__(self):
        super().__init__()

    def insert(self, word, value):
        result = True
        if self._root.is_external():
            node = Node(word, value)
            self._root.append_child(node)
        else:
            for child in self._root.children():
                result = self._insert(child, word, value)
                if result is not False:
                    break
            else:
                node = Node(word, value)
                self._root.append_child(node)
                result = True
        self._value_list.append(value)
        if result is True:
            self._size += 1

    def _insert(self, node, word, value):
        key = node.key()
        index = common_prefix(key, word)
        if index == 0:
            return False

        len_key, len_word = len(key), len(word)
        if index < len_key and index <= len_word:  # common prefix or word is the prefix of key
            key_remaining = key[index:]
            word_remaining = word[index:] if index < len_word else ' '
            node1 = Node(key_remaining, node.value()) if node.is_external() else Node(key_remaining, None)
            node2 = Node(word_remaining, value)
            node1.set_children(node.children())
            node.set_key(key[:index])
            node.set_value(None)
            node.set_children([node1, node2])
            return True
        elif index == len_key and index < len_word:  # key is the prefix of word
            if node.is_external():  # previous word is the prefix of current word
                key_remaining, word_remaining = ' ', word[index:]
                node1, node2 = Node(key_remaining, node.value()), Node(word_remaining, value)
                node.append_child(node1).append_child(node2)
                return True
            else:
                word_remaining = word[index:]
                for child in node.children():
                    result = self._insert(child, word_remaining, value)
                    if result is not False:
                        return result
                node1 = Node(word_remaining, value)
                node.append_child(node1)
                return True
        elif index == len_key and index == len_word:
            if node.is_external():
                self._value_list.remove(node.value())
                node.set_value(value)
                return 2
            for child in node.children():
                if child.key() == ' ':
                    self._value_list.remove(child.value())
                    child.set_value(value)
                    return 2
            word_remaining = ' '
            node1 = Node(word_remaining, value)
            node.append_child(node1)
            return True

    def search(self, word):
        for child in self._root.children():
            value = self._search(child, word)
            if value is not None:
                return value
        return None

    def _search(self, node, word):
        key = node.key()
        index = common_prefix(key, word)
        if index == 0:
            return None

        len_key, len_word = len(key), len(word)
        if index < len_key and index <= len_word:
            return None
        elif index == len_key and index < len_word:
            if node.is_external():
                return None
            else:
                word_remaining = word[index:]
                for child in node.children():
                    value = self._search(child, word_remaining)
                    if value is not None:
                        return value
                return None
        elif index == len_key and index == len_word:
            if node.is_external():
                return node.value()
            else:
                for child in node.children():
                    if child.key() == ' ':
                        return child.value()
                return None
