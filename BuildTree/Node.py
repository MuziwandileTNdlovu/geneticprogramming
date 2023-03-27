import random

import numpy as np

from Config.Config import Config


class Node:
    def __init__(self, name, parent=None, children=None):
        self.config = Config()
        self.name = name
        self.parent = parent
        self.children = children if children is not None else []
        self.root = None
        self.depth = self.config.MAX_DEPTH

        self.random = random.Random(self.config.getSeed())

    def getName(self):
        return self.name

    def printTree(self, prefix=""):
        print(prefix + '|-- ' + self.name)
        for i, child in enumerate(self.children):
            is_last = i == len(self.children) - 1
            prefix += '    ' if is_last else '|   '
            child.printTree(prefix)
            prefix = prefix[:-4]

    def printTreeEq(self, is_last=False, prefix=""):
        prefix += ''
        if len(self.children) == 0:
            print(prefix + '' + self.name, end='')
        else:
            print(prefix + '' + self.name + '(', end='')
            for i, child in enumerate(self.children):
                is_last_child = i == len(self.children) - 1
                child.printTreeEq(is_last_child, prefix + "")
            print(')', end='')

    def get_random_subtree(self, node, restnode):
        self.depth = self.config.MAX_DEPTH
        if node.children:
            subtree = self.random.choice(node.children)
            if self.random.random() < 0.5:
                if subtree.is_under_min_depth(subtree, self.config.MIN_DEPTH) or subtree.is_over_max_depth(subtree,
                                                                                                           self.config.MAX_DEPTH - 1):
                    return self.generateFull()
                return subtree
            else:
                return self.get_random_subtree(subtree, restnode)
        else:
            return self.get_random_subtree(restnode, restnode)

    def generateFull(self):
        if self.depth == 0:
            return Node(random.choice(list(self.config.TERMINAL_SET.keys())))
        else:
            self.depth -= 1
            left_child = self.generateFullWithDepth(self.depth)
            right_child = self.generateFullWithDepth(self.depth)
            return Node(self.random.choice(list(self.config.FUNCTION_SET.keys())),
                        children=[left_child, right_child])

    def generateFullWithDepth(self, depth):
        if depth == 0:
            return Node(self.random.choice(list(self.config.TERMINAL_SET.keys())))
        else:
            depth -= 1
            left_child = self.generateFullWithDepth(depth)
            right_child = self.generateFullWithDepth(depth)
            return Node(self.random.choice(list(self.config.FUNCTION_SET.keys())),
                        children=[left_child, right_child])

    def getTreeDepth(self):
        if not self.children:
            return 0
        return 1 + max(child.getTreeDepth() for child in self.children)

    def is_over_max_depth(self, node, max_depth):
        if max_depth == 0:
            return True
        elif node.children:
            return any(self.is_over_max_depth(child, max_depth - 1) for child in node.children)
        else:
            return False

    def is_under_min_depth(self, node, min_depth):
        if min_depth == 0:
            return False
        elif node.children:
            return all(self.is_under_min_depth(child, min_depth - 1) for child in node.children)
        else:
            return True

    def evaluate(self):
        # If the node is a terminal node, return its name
        if self.name in self.config.TERMINAL_SET:
            return self.name

        # Otherwise, recursively evaluate the children and apply the function at the root node
        child_results = [child.evaluate() for child in self.children]
        function = self.config.FUNCTION_SET[self.name]
        return function(*child_results)
