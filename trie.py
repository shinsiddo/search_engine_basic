class TrieNode:

    def __init__(self):
        self.children = {}
        self.is_end = False


class Trie:

    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):

        current = self.root

        for char in word:

            if char not in current.children:
                current.children[char] = TrieNode()

            current = current.children[char]

        current.is_end = True

    def autocomplete(self, prefix):

        current = self.root

        for char in prefix:

            if char not in current.children:
                return []

            current = current.children[char]

        results = []

        self._find_words(
            current,
            prefix,
            results
        )

        return results

    def _find_words(self, node, word, results):

        if node.is_end:
            results.append(word)

        for char, child in node.children.items():

            self._find_words(
                child,
                word + char,
                results
            )
