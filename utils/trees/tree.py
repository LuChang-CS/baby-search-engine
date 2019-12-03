class Node:
    """Tree node

    A tree node contains a key, a value and it's children list.
    """
    def __init__(self, key, value):
        self._key = key
        self._value = value
        self._children = []

    def set_key(self, key):
        self._key = key
    
    def key(self):
        return self._key

    def set_value(self, value):
        self._value = value

    def value(self):
        return self._value
    
    def is_external(self):
        return len(self._children) == 0

    def children(self):
        return self._children

    def set_children(self, children):
        self._children = children

    def append_child(self, node):
        self._children.append(node)
        return self


class Tree:
    """Tree data structure

    A tree contains a root node (Node)
    """
    def __init__(self, root_key=None, root_value=None):
        """Initialize a tree using a key and value for the root node.

        @param root_key: default None
        @param root_value: default None
        """
        self._root = Node(root_key, root_value)
        self._size = 0

    def root(self):
        return self._root

    def size(self):
        return self._size

    def __len__(self):
        return self._size
