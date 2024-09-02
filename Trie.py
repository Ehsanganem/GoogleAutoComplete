class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False
        self.documents = set()

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word, document):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
            node.documents.add(document)
        node.is_end_of_word = True

    def search_prefix(self, prefix):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return set()
            node = node.children[char]
        return node.documents
