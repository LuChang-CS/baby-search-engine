import os
import _pickle as pickle

from utils.strings import common_prefix
from utils.trees import Node, Tree


class Trie(Tree):
    """Trie data structure

    Trie is a subclass of Tree.
    """
    NAME = 'trie'

    def __init__(self):
        super().__init__(root_key=None, root_value=None)
        # _value_list stores all values inserted into this trie.
        self._value_list = []

    def value_list(self):
        return self._value_list

    def insert(self, word, value):
        pass

    def search(self, word):
        return None

    @staticmethod
    def dump(trie, path):
        """Store a trie object to the specific path on the disk

        The filename of trie on the disk is the same as Trie.NAME.

        @param path: str, the path to save on the disk
        """
        path = os.path.join(path, Trie.NAME)
        pickle.dump(trie, open(path, 'wb'))

    @staticmethod
    def load(path):
        """Load the trie file stored on the disk into memory.

        The filename of trie on the disk is the same as Trie.NAME.

        @param path: str, the path to load on the disk
        @return: a trie object
        """
        path = os.path.join(path, Trie.NAME)
        return pickle.load(open(path, 'rb'))


class CompressedTrie(Trie):
    """Compress trie structure

    The CompressTrie is a subclass of Trie.
    Here, we allow a word to be the prefix of other words.
    """
    def __init__(self):
        super().__init__()

    def insert(self, word, value):
        """Inserting a word with its value into trie.

        @param word: str
        @param value
        """
        result = True
        # if root is an external node, we directly append the new node to root.
        if self._root.is_external():
            node = Node(word, value)
            self._root.append_child(node)
        # else, we recursively find a node to insert the word.
        else:
            for child in self._root.children():
                result = self._insert(child, word, value)
                if result is not False:
                    break
            # if no child has a common prefix with word, we need to append a new node.
            else:
                node = Node(word, value)
                self._root.append_child(node)
                result = True
        self._value_list.append(value)
        if result is True:
            self._size += 1

    def _insert(self, node, word, value):
        """Recursively insert the word to the trie.

        @param node: Node, the current node to compare
        @param word: str
        @param value
        @return: False, no common prefix;
                 True, success to insert;
                 2, word exists.
        """
        key = node.key()
        index = common_prefix(key, word)
        # no common prefix.
        if index == 0:
            return False

        len_key, len_word = len(key), len(word)
        # Key and word have common prefix, we split the key and word
        # and append the remaining part of key and word to the current node.
        #
        # Or word is the prefix of key, we split the key, and append
        # the remaining key and a space node to the current node,
        # to satisfy a word being a prefix of other words.
        if index < len_key and index <= len_word:
            key_remaining = key[index:]
            word_remaining = word[index:] if index < len_word else ' '
            node1 = Node(key_remaining, node.value()) if node.is_external() else Node(key_remaining, None)
            node2 = Node(word_remaining, value)
            node1.set_children(node.children())
            node.set_key(key[:index])
            node.set_value(None)
            node.set_children([node1, node2])
            return True
        # Key is the prefix of word
        elif index == len_key and index < len_word:
            # Previous word is the prefix of current word,
            # we split the word, and append the remaining
            # word and a space node to the current node.
            if node.is_external():
                key_remaining, word_remaining = ' ', word[index:]
                node1, node2 = Node(key_remaining, node.value()), Node(word_remaining, value)
                node.append_child(node1).append_child(node2)
                return True
            # else, we continue to insert the remaining part of word to the children.
            else:
                word_remaining = word[index:]
                for child in node.children():
                    result = self._insert(child, word_remaining, value)
                    if result is not False:
                        return result
                # If all children cannot be inserted,
                # we append a new node.
                node1 = Node(word_remaining, value)
                node.append_child(node1)
                return True
        # Key matches the word.
        elif index == len_key and index == len_word:
            # Key is just the word, which mean word has already exists.
            # We remove the previous value and update the value.
            if node.is_external():
                self._value_list.remove(node.value())
                node.set_value(value)
                return 2
            # Word is a prefix of other words.
            for child in node.children():
                # Word has already exists.
                if child.key() == ' ':
                    self._value_list.remove(child.value())
                    child.set_value(value)
                    return 2
            # We insert a space node.
            word_remaining = ' '
            node1 = Node(word_remaining, value)
            node.append_child(node1)
            return True

    def search(self, word):
        """Search a word in the trie and return its value

        @param word: str
        @return: None, if word not exists;
                 value of word, if word exists.
        """
        for child in self._root.children():
            value = self._search(child, word)
            if value is not None:
                return value
        return None

    def _search(self, node, word):
        """Search a word recursively

        @param node: Node, the current node to compare
        @param word: str
        @return None, if word not exists in current node;
                value of word, if word exists.
        """
        key = node.key()
        index = common_prefix(key, word)
        if index == 0:
            return None

        len_key, len_word = len(key), len(word)
        # Key and word have common prefix or word is the prefix of key, not exist.
        if index < len_key and index <= len_word:
            return None
        # Key is the prefix of word, maybe exist.
        elif index == len_key and index < len_word:
            # Current node is external, not exist.
            if node.is_external():
                return None
            else:
                # Continue to search.
                word_remaining = word[index:]
                for child in node.children():
                    value = self._search(child, word_remaining)
                    if value is not None:
                        return value
                # All children don't have this word, not exist.
                return None
        # Key and word match perfectly, maybe exist.
        elif index == len_key and index == len_word:
            # Key is exactly the word, exist.
            if node.is_external():
                return node.value()
            else:
                for child in node.children():
                    # Key is the word, although word is also a prefix of other words, exist.
                    if child.key() == ' ':
                        return child.value()
                # Word is only a prefix of other words, not exist.
                return None
