import os

from utils import CompressedTrie

__all__ = ['init_engine', 'get_engine']
engine = dict()


class Engine:

    def __init__(self, path, engine_type):
        self._engine = engine_type.load(path)

    def search(self, word):
        return self._engine.search(word)


def init_engine(path, engine_type=CompressedTrie):
    engine[engine_type.NAME] = Engine(path, engine_type)


def get_engine(name):
    return engine[name]
